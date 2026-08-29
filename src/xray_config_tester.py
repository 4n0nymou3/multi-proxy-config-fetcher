import os
import json
import subprocess
import tempfile
import logging
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import requests
import sys
from config import ProxyConfig
import config_parser as parser
import transport_builder
from testing_utils import find_free_port, get_usable_test_urls, rotate_urls, managed_process, wait_for_port

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class XrayTester:
    def __init__(self, xray_path: str = 'xray', timeout: int = 10, test_urls: List[str] = None):
        self.xray_path = xray_path
        self.timeout = timeout
        initial_urls = test_urls if test_urls else ['https://www.youtube.com/generate_204']
        self.test_url = initial_urls[0]
        self.unsupported_protocols = ['tuic://', 'wireguard://']
        self._verify_xray()
    
    def _verify_xray(self):
        try:
            result = subprocess.run(
                [self.xray_path, 'version'],
                capture_output=True,
                timeout=5
            )
            if result.returncode != 0:
                raise RuntimeError(f"xray verification failed: {result.stderr.decode()}")
        except FileNotFoundError:
            raise RuntimeError(f"xray not found at: {self.xray_path}")
        except Exception as e:
            raise RuntimeError(f"xray verification error: {e}")
        
    def is_supported_protocol(self, config_str: str) -> bool:
        config_lower = config_str.lower()
        for protocol in self.unsupported_protocols:
            if config_lower.startswith(protocol):
                return False
        return True
        
    def parse_config_string(self, config_str: str) -> Optional[Dict]:
        try:
            config_lower = config_str.lower()
            data = None
            outbound = None
            
            if config_lower.startswith('vmess://'):
                data = parser.decode_vmess(config_str)
                if not data: return None
                outbound = {
                    "protocol": "vmess",
                    "settings": {
                        "vnext": [{
                            "address": data.get('add'),
                            "port": int(data.get('port')),
                            "users": [{
                                "id": data.get('id'),
                                "alterId": int(data.get('aid', 0)),
                                "security": data.get('scy', 'auto')
                            }]
                        }]
                    },
                    "streamSettings": transport_builder.build_xray_settings(data)
                }
            
            elif config_lower.startswith('vless://'):
                data = parser.parse_vless(config_str)
                if not data: return None
                outbound = {
                    "protocol": "vless",
                    "settings": {
                        "vnext": [{
                            "address": data['address'],
                            "port": data['port'],
                            "users": [{
                                "id": data['uuid'],
                                "encryption": "none",
                                "flow": data.get('flow', '')
                            }]
                        }]
                    },
                    "streamSettings": transport_builder.build_xray_settings(data)
                }
                
            elif config_lower.startswith('trojan://'):
                data = parser.parse_trojan(config_str)
                if not data: return None
                outbound = {
                    "protocol": "trojan",
                    "settings": {
                        "servers": [{
                            "address": data['address'],
                            "port": data['port'],
                            "password": data['password']
                        }]
                    },
                    "streamSettings": transport_builder.build_xray_settings(data)
                }
                
            elif config_lower.startswith('ss://'):
                data = parser.parse_shadowsocks(config_str)
                if not data: return None
                outbound = {
                    "protocol": "shadowsocks",
                    "settings": {
                        "servers": [{
                            "address": data['address'],
                            "port": data['port'],
                            "method": data['method'],
                            "password": data['password']
                        }]
                    }
                }
            
            return outbound
            
        except Exception as e:
            logger.debug(f"Failed to parse config: {str(e)}")
            return None
    
    def create_xray_config(self, outbound: Dict, socks_port: int, http_port: int) -> Dict:
        return {
            "log": {
                "loglevel": "error"
            },
            "inbounds": [
                {
                    "port": socks_port,
                    "protocol": "socks",
                    "settings": {
                        "auth": "noauth",
                        "udp": False
                    }
                },
                {
                    "port": http_port,
                    "protocol": "http"
                }
            ],
            "outbounds": [outbound]
        }
    
    def test_config(self, config_str: str) -> Tuple[bool, Optional[int], str]:
        if not self.is_supported_protocol(config_str):
            protocol = config_str.split('://')[0].upper()
            logger.info(f"⊘ Skipping {protocol} (not supported by Xray core)")
            return True, 0, config_str
        
        config_file = None
        
        try:
            outbound = self.parse_config_string(config_str)
            if not outbound:
                logger.warning(f"✗ Failed to parse config")
                return False, None, config_str
            
            socks_port = find_free_port()
            http_port = find_free_port()
            
            xray_config = self.create_xray_config(outbound, socks_port, http_port)
            
            fd, config_file = tempfile.mkstemp(suffix='.json', text=True, prefix='xray_')
            try:
                with os.fdopen(fd, 'w') as f:
                    json.dump(xray_config, f, indent=2)
            except Exception as e:
                os.close(fd)
                raise
            
            with managed_process(
                [self.xray_path, 'run', '-c', config_file]
            ) as process:
                if not wait_for_port(process, http_port, max_wait=3.0):
                    stderr = process.stderr.read().decode('utf-8', errors='ignore') if process.stderr else ''
                    logger.warning(f"✗ Process crashed or never started listening: {stderr[:200]}")
                    return False, None, config_str
                
                proxies = {
                    'http': f'http://127.0.0.1:{http_port}',
                    'https': f'http://127.0.0.1:{http_port}'
                }
                
                session = requests.Session()
                session.proxies.update(proxies)
                
                url = self.test_url
                domain = url.split('/')[2] if '/' in url[8:] else 'unknown'
                start_time = time.time()
                try:
                    response = session.get(
                        url,
                        timeout=self.timeout
                    )
                    delay = int((time.time() - start_time) * 1000)
                    
                    if response.status_code in [200, 204]:
                        logger.info(f"✓ OK ({delay}ms via {domain})")
                        return True, delay, config_str
                    else:
                        logger.warning(f"✗ HTTP {response.status_code} on {domain}")
                        return False, None, config_str
                        
                except requests.exceptions.ProxyError as e:
                    logger.warning(f"✗ Proxy error: {str(e)[:100]}")
                    return False, None, config_str
                except requests.exceptions.Timeout:
                    logger.warning(f"✗ Timeout on {domain}")
                    return False, None, config_str
                except requests.exceptions.ConnectionError as e:
                    logger.warning(f"✗ Connection error on {domain}: {str(e)[:100]}")
                    return False, None, config_str
                except Exception as e:
                    logger.warning(f"✗ {type(e).__name__} on {domain}: {str(e)[:100]}")
                    return False, None, config_str
                
        except Exception as e:
            logger.error(f"✗ Setup error: {str(e)}")
            return False, None, config_str
            
        finally:
            if config_file and os.path.exists(config_file):
                try:
                    os.unlink(config_file)
                except Exception as e:
                    logger.debug(f"Failed to remove temp file {config_file}: {e}")
            
            time.sleep(0.1)


class ParallelXrayTester:
    def __init__(self, xray_path: str = 'xray', max_workers: int = 8, timeout: int = 10,
                 test_urls: List[str] = None, rounds: int = 2):
        self.base_test_urls = test_urls if test_urls else ['https://www.youtube.com/generate_204']
        self.tester = XrayTester(xray_path, timeout, self.base_test_urls)
        self.max_workers = max(1, min(max_workers, os.cpu_count() or 4))
        self.rounds = max(1, rounds)
        
    def _run_single_round(self, configs: List[str]) -> Dict[str, int]:
        round_results: Dict[str, int] = {}
        tested = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.tester.test_config, cfg): cfg for cfg in configs}
            
            for future in as_completed(futures):
                config = futures[future]
                tested += 1
                
                try:
                    success, delay, config_str = future.result(timeout=self.tester.timeout + 10)
                    if success:
                        round_results[config_str] = delay if delay else 0
                    
                    if tested % 25 == 0 or tested == len(configs):
                        logger.info(f"Progress: {tested}/{len(configs)} ({len(round_results)} working so far)")
                
                except Exception as e:
                    logger.error(f"Test error: {str(e)}")
        
        return round_results
        
    def test_all(self, configs: List[str]) -> List[str]:
        total = len(configs)
        logger.info(f"Testing {total} configs with {self.max_workers} workers over {self.rounds} round(s)...")
        logger.info(f"Base test URLs: {self.base_test_urls}")
        
        candidates = list(configs)
        skipped = 0
        
        for round_num in range(1, self.rounds + 1):
            if not candidates:
                break
            
            round_urls = rotate_urls(self.base_test_urls, round_num - 1)
            self.tester.test_url = round_urls[0]
            logger.info(f"--- Round {round_num}/{self.rounds}: {len(candidates)} configs, endpoint {self.tester.test_url} ---")
            
            round_results = self._run_single_round(candidates)
            skipped = sum(1 for cfg in candidates if cfg in round_results and round_results[cfg] == 0)
            candidates = [cfg for cfg in candidates if cfg in round_results]
            
            success_rate = (len(candidates) * 100) // max(1, total)
            logger.info(f"Round {round_num} result: {len(candidates)}/{total} survive ({success_rate}%)")
        
        working = candidates
        success_rate = (len(working) * 100) // max(1, total)
        logger.info(f"Final results after {self.rounds} round(s): {len(working)}/{total} working ({success_rate}%) - {skipped} skipped (unsupported)")
        return working


def main():
    config_settings = ProxyConfig()

    if len(sys.argv) < 3:
        print("Usage: python xray_config_tester.py <input.txt> <output.txt>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not config_settings.ENABLE_XRAY_TESTER:
        logger.info("Xray testing is disabled in user_settings.py. Skipping.")
        try:
            with open(input_file, 'r', encoding='utf-8') as f_in:
                content = f_in.read()
            os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f_out:
                f_out.write(content)
            logger.info(f"Copied {input_file} to {output_file} as testing is disabled.")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Failed to copy {input_file} to {output_file}: {str(e)}")
            sys.exit(1)

    max_workers = config_settings.XRAY_TESTER_MAX_WORKERS
    timeout = config_settings.XRAY_TESTER_TIMEOUT_SECONDS
    rounds = config_settings.XRAY_TESTER_ROUNDS
    test_urls = get_usable_test_urls(config_settings.XRAY_TESTER_URLS)
    
    logger.info(f"Loading configs from {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        logger.error(f"Input file not found: {input_file}")
        sys.exit(1)
    
    configs = []
    header_lines = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('//') or not line:
            if not configs:
                header_lines.append(line)
        else:
            configs.append(line)
    
    if not configs:
        logger.error("No configs found")
        sys.exit(1)
    
    logger.info(f"Found {len(configs)} configs")
    
    tester = ParallelXrayTester(max_workers=max_workers, timeout=timeout, test_urls=test_urls, rounds=rounds)
    working = tester.test_all(configs)
    
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        for header in header_lines:
            f.write(header + '\n')
        if header_lines:
            f.write('\n')
        for config in working:
            f.write(config + '\n\n')
    
    if working:
        logger.info(f"Saved {len(working)} working configs to {output_file}")
        sys.exit(0)
    else:
        logger.error("No working configs found")
        sys.exit(0)


if __name__ == '__main__':
    main()