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
from testing_utils import find_free_port, get_usable_test_urls, rotate_urls, median_of, managed_process, wait_for_port

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SingBoxTester:
    def __init__(self, singbox_path: str = 'sing-box', timeout: int = 10, test_urls: List[str] = None):
        self.singbox_path = singbox_path
        self.timeout = timeout
        initial_urls = test_urls if test_urls else ['https://www.youtube.com/generate_204']
        self.test_url = initial_urls[0]
        self._verify_singbox()
    
    def _verify_singbox(self):
        try:
            result = subprocess.run(
                [self.singbox_path, 'version'],
                capture_output=True,
                timeout=5
            )
            if result.returncode != 0:
                raise RuntimeError(f"sing-box verification failed: {result.stderr.decode()}")
        except FileNotFoundError:
            raise RuntimeError(f"sing-box not found at: {self.singbox_path}")
        except Exception as e:
            raise RuntimeError(f"sing-box verification error: {e}")
        
    def create_minimal_config(self, outbound: Dict, mixed_port: int) -> Dict:
        return {
            "log": {
                "level": "panic",
                "timestamp": False
            },
            "inbounds": [
                {
                    "type": "mixed",
                    "listen": "127.0.0.1",
                    "listen_port": mixed_port
                }
            ],
            "outbounds": [outbound],
            "route": {
                "final": outbound.get('tag', 'proxy')
            }
        }
    
    def test_config(self, outbound: Dict) -> Tuple[bool, Optional[int], str]:
        tag = outbound.get('tag', 'unknown')
        config_file = None
        
        try:
            mixed_port = find_free_port()
        except RuntimeError as e:
            logger.error(f"✗ {tag} - Port allocation failed: {e}")
            return False, None, tag
        
        try:
            config = self.create_minimal_config(outbound, mixed_port)
            
            fd, config_file = tempfile.mkstemp(suffix='.json', text=True, prefix='singbox_')
            try:
                with os.fdopen(fd, 'w') as f:
                    json.dump(config, f, indent=2)
            except Exception as e:
                os.close(fd)
                raise
            
            with managed_process(
                [self.singbox_path, 'run', '-c', config_file]
            ) as process:
                if not wait_for_port(process, mixed_port, max_wait=3.0):
                    stderr = process.stderr.read().decode('utf-8', errors='ignore') if process.stderr else ''
                    logger.warning(f"✗ {tag} - Process crashed or never started listening: {stderr[:200]}")
                    return False, None, tag
                
                proxies = {
                    'http': f'http://127.0.0.1:{mixed_port}',
                    'https': f'http://127.0.0.1:{mixed_port}'
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
                        logger.info(f"✓ {tag} - OK ({delay}ms via {domain})")
                        return True, delay, tag
                    else:
                        logger.warning(f"✗ {tag} - HTTP {response.status_code} on {domain}")
                        return False, None, tag
                        
                except requests.exceptions.ProxyError as e:
                    logger.warning(f"✗ {tag} - Proxy error: {str(e)[:100]}")
                    return False, None, tag
                except requests.exceptions.Timeout:
                    logger.warning(f"✗ {tag} - Timeout on {domain}")
                    return False, None, tag
                except requests.exceptions.ConnectionError as e:
                    logger.warning(f"✗ {tag} - Connection error on {domain}: {str(e)[:100]}")
                    return False, None, tag
                except Exception as e:
                    logger.warning(f"✗ {tag} - {type(e).__name__} on {domain}: {str(e)[:100]}")
                    return False, None, tag
                
        except Exception as e:
            logger.error(f"✗ {tag} - Setup error: {str(e)}")
            return False, None, tag
            
        finally:
            if config_file and os.path.exists(config_file):
                try:
                    os.unlink(config_file)
                except Exception as e:
                    logger.debug(f"Failed to remove temp file {config_file}: {e}")
            
            time.sleep(0.05)


class ParallelConfigTester:
    def __init__(self, singbox_path: str = 'sing-box', max_workers: int = 8, timeout: int = 10,
                 test_urls: List[str] = None, rounds: int = 2):
        self.base_test_urls = test_urls if test_urls else ['https://www.youtube.com/generate_204']
        self.tester = SingBoxTester(singbox_path, timeout, self.base_test_urls)
        self.max_workers = max(1, min(max_workers, os.cpu_count() or 4))
        self.rounds = max(1, rounds)
        
    def _run_single_round(self, outbounds: List[Dict]) -> Dict[str, int]:
        round_results: Dict[str, int] = {}
        tested = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.tester.test_config, ob): ob for ob in outbounds}
            
            for future in as_completed(futures):
                outbound = futures[future]
                tested += 1
                
                try:
                    success, delay, tag = future.result(timeout=self.tester.timeout + 10)
                    if success and delay is not None:
                        round_results[tag] = delay
                    
                    if tested % 25 == 0 or tested == len(outbounds):
                        logger.info(f"Progress: {tested}/{len(outbounds)} ({len(round_results)} working so far)")
                
                except Exception as e:
                    logger.error(f"Test error for {outbound.get('tag', 'unknown')}: {str(e)}")
        
        return round_results
        
    def test_all(self, outbounds: List[Dict]) -> List[Dict]:
        total = len(outbounds)
        logger.info(f"Testing {total} configs with {self.max_workers} workers over {self.rounds} round(s)...")
        logger.info(f"Base test URLs: {self.base_test_urls}")
        
        candidates = list(outbounds)
        delays_by_tag: Dict[str, List[int]] = {}
        
        for round_num in range(1, self.rounds + 1):
            if not candidates:
                break
            
            round_urls = rotate_urls(self.base_test_urls, round_num - 1)
            self.tester.test_url = round_urls[0]
            logger.info(f"--- Round {round_num}/{self.rounds}: {len(candidates)} configs, endpoint {self.tester.test_url} ---")
            
            round_results = self._run_single_round(candidates)
            candidates = [ob for ob in candidates if ob.get('tag') in round_results]
            for ob in candidates:
                delays_by_tag.setdefault(ob['tag'], []).append(round_results[ob['tag']])
            
            success_rate = (len(candidates) * 100) // max(1, total)
            logger.info(f"Round {round_num} result: {len(candidates)}/{total} survive ({success_rate}%)")
        
        working = []
        for ob in candidates:
            ob_copy = ob.copy()
            ob_copy['_test_delay'] = median_of(delays_by_tag.get(ob['tag'], []))
            working.append(ob_copy)
        
        working.sort(key=lambda x: x.get('_test_delay', 999999))
        
        for ob in working:
            ob.pop('_test_delay', None)
        
        success_rate = (len(working) * 100) // max(1, total)
        logger.info(f"Final results after {self.rounds} round(s): {len(working)}/{total} working ({success_rate}%)")
        return working


def update_config_with_working_outbounds(config: Dict, working_outbounds: List[Dict]) -> Dict:
    if not working_outbounds:
        logger.warning("No working outbounds - keeping original config")
        return config
    
    working_tags = {ob['tag'] for ob in working_outbounds}
    
    new_outbounds = []
    
    for ob in config.get('outbounds', []):
        ob_type = ob.get('type')
        
        if ob_type == 'selector':
            new_list = []
            for tag in ob.get('outbounds', []):
                if tag in working_tags or tag in ['👽 Best Ping 🚀', 'auto', 'direct', 'block']:
                    new_list.append(tag)
            if new_list:
                ob['outbounds'] = new_list
                new_outbounds.append(ob)
            else:
                logger.warning(f"Selector '{ob.get('tag')}' has no working outbounds, skipping")
            
        elif ob_type == 'urltest':
            new_list = [tag for tag in ob.get('outbounds', []) if tag in working_tags]
            if new_list:
                ob['outbounds'] = new_list
                new_outbounds.append(ob)
            else:
                logger.warning(f"URLTest '{ob.get('tag')}' has no working outbounds, skipping")
            
        elif ob_type in ['direct', 'block', 'dns']:
            new_outbounds.append(ob)
            
        elif ob.get('tag') in working_tags:
            new_outbounds.append(ob)
    
    config['outbounds'] = new_outbounds
    return config


def main():
    config_settings = ProxyConfig()

    if len(sys.argv) < 3:
        print("Usage: python config_tester.py <input.json> <output.json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not config_settings.ENABLE_CONFIG_TESTER:
        logger.info("Config testing is disabled in user_settings.py. Skipping.")
        try:
            with open(input_file, 'r', encoding='utf-8') as f_in:
                config_data = json.load(f_in)
            os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f_out:
                json.dump(config_data, f_out, indent=4, ensure_ascii=False)
            logger.info(f"Copied {input_file} to {output_file} as testing is disabled.")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Failed to copy {input_file} to {output_file}: {str(e)}")
            sys.exit(1)

    max_workers = config_settings.TESTER_MAX_WORKERS
    timeout = config_settings.TESTER_TIMEOUT_SECONDS
    rounds = config_settings.TESTER_ROUNDS
    test_urls = get_usable_test_urls(config_settings.TESTER_URLS)
    
    logger.info(f"Loading config from {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        logger.error(f"Input file not found: {input_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {input_file}: {e}")
        sys.exit(1)
    
    proxy_outbounds = [
        ob for ob in config.get('outbounds', [])
        if ob.get('type') not in ['selector', 'urltest', 'direct', 'block', 'dns']
    ]
    
    if not proxy_outbounds:
        logger.error("No proxy outbounds found")
        sys.exit(1)
    
    logger.info(f"Found {len(proxy_outbounds)} proxy outbounds")
    
    tester = ParallelConfigTester(max_workers=max_workers, timeout=timeout, test_urls=test_urls, rounds=rounds)
    working = tester.test_all(proxy_outbounds)
    
    if working:
        config = update_config_with_working_outbounds(config, working)
        
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        logger.info(f"Saved {len(working)} working configs to {output_file}")
        sys.exit(0)
    else:
        logger.error("No working configs found - saving original config")
        
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        sys.exit(0)


if __name__ == '__main__':
    main()