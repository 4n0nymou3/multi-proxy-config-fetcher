import os
import json
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


class XrayBatchTester:
    def __init__(self, xray_path: str = 'xray', timeout: int = 10, test_url: str = None, concurrency: int = 16):
        self.xray_path = xray_path
        self.timeout = timeout
        self.test_url = test_url if test_url else 'https://www.youtube.com/generate_204'
        self.concurrency = max(1, concurrency)
        self.unsupported_protocols = ['tuic://', 'wireguard://']
        self._verify_xray()

    def _verify_xray(self):
        import subprocess
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
                if not data:
                    return None
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
                if not data:
                    return None
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
                if not data:
                    return None
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
                if not data:
                    return None
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

    def build_batch_config(self, items: List[Tuple[int, int, Dict]]) -> Dict:
        inbounds = []
        outbounds = []
        rules = []
        for tag_id, port, outbound in items:
            inbounds.append({
                "port": port,
                "listen": "127.0.0.1",
                "protocol": "http",
                "tag": f"in-{tag_id}"
            })
            ob = dict(outbound)
            ob["tag"] = f"out-{tag_id}"
            outbounds.append(ob)
            rules.append({
                "type": "field",
                "inboundTag": [f"in-{tag_id}"],
                "outboundTag": f"out-{tag_id}"
            })
        return {
            "log": {"loglevel": "error"},
            "inbounds": inbounds,
            "outbounds": outbounds,
            "routing": {"rules": rules}
        }

    def _test_one(self, port: int, config_str: str) -> Tuple[str, bool, Optional[int]]:
        proxies = {
            'http': f'http://127.0.0.1:{port}',
            'https': f'http://127.0.0.1:{port}'
        }
        session = requests.Session()
        session.proxies.update(proxies)
        start_time = time.time()
        try:
            response = session.get(self.test_url, timeout=self.timeout)
            delay = int((time.time() - start_time) * 1000)
            if response.status_code in (200, 204):
                return config_str, True, delay
            return config_str, False, None
        except Exception:
            return config_str, False, None

    def run_batch(self, entries: List[Tuple[str, Dict]]) -> Dict[str, Tuple[bool, Optional[int]]]:
        results: Dict[str, Tuple[bool, Optional[int]]] = {}
        if not entries:
            return results

        prepared = []
        for tag_id, (config_str, outbound) in enumerate(entries):
            try:
                port = find_free_port()
            except Exception as e:
                logger.error(f"Port allocation failed: {e}")
                results[config_str] = (False, None)
                continue
            prepared.append((tag_id, port, outbound, config_str))

        if not prepared:
            return results

        batch_config = self.build_batch_config([(t, p, o) for t, p, o, _ in prepared])

        fd, config_file = tempfile.mkstemp(suffix='.json', text=True, prefix='xray_batch_')
        try:
            with os.fdopen(fd, 'w') as f:
                json.dump(batch_config, f)
        except Exception as e:
            os.close(fd)
            logger.error(f"Failed to write batch config: {e}")
            for _, _, _, cs in prepared:
                results[cs] = (False, None)
            return results

        try:
            with managed_process([self.xray_path, 'run', '-c', config_file]) as process:
                probe_port = prepared[0][1]
                if not wait_for_port(process, probe_port, max_wait=5.0):
                    stderr = process.stderr.read().decode('utf-8', errors='ignore') if process.stderr else ''
                    logger.warning(f"Batch of {len(prepared)} failed to start ({stderr[:150]}), bisecting")
                    if len(prepared) == 1:
                        results[prepared[0][3]] = (False, None)
                        return results
                    mid = len(prepared) // 2
                    first_half = [(cs, ob) for _, _, ob, cs in prepared[:mid]]
                    second_half = [(cs, ob) for _, _, ob, cs in prepared[mid:]]
                    results.update(self.run_batch(first_half))
                    results.update(self.run_batch(second_half))
                    return results

                with ThreadPoolExecutor(max_workers=min(len(prepared), self.concurrency)) as executor:
                    futures = [executor.submit(self._test_one, port, cs) for _, port, _, cs in prepared]
                    for future in as_completed(futures):
                        cs, ok, delay = future.result()
                        results[cs] = (ok, delay)
        finally:
            if os.path.exists(config_file):
                try:
                    os.unlink(config_file)
                except Exception as e:
                    logger.debug(f"Failed to remove temp batch file {config_file}: {e}")

        for _, _, _, cs in prepared:
            if cs not in results:
                results[cs] = (False, None)

        return results


class ParallelXrayTester:
    def __init__(self, xray_path: str = 'xray', max_workers: int = 8, timeout: int = 10,
                 test_urls: List[str] = None, rounds: int = 2, batch_size: int = 200):
        self.base_test_urls = test_urls if test_urls else ['https://www.youtube.com/generate_204']
        self.tester = XrayBatchTester(xray_path, timeout, self.base_test_urls[0], concurrency=max_workers)
        self.rounds = max(1, rounds)
        self.batch_size = max(1, batch_size)

    def _run_single_round(self, configs: List[str]) -> Dict[str, Tuple[bool, Optional[int]]]:
        results: Dict[str, Tuple[bool, Optional[int]]] = {}
        supported_entries = []

        for cfg in configs:
            if not self.tester.is_supported_protocol(cfg):
                results[cfg] = (True, 0)
                continue
            outbound = self.tester.parse_config_string(cfg)
            if not outbound:
                results[cfg] = (False, None)
                continue
            supported_entries.append((cfg, outbound))

        total_batches = (len(supported_entries) + self.batch_size - 1) // self.batch_size
        for batch_num, i in enumerate(range(0, len(supported_entries), self.batch_size), 1):
            chunk = supported_entries[i:i + self.batch_size]
            batch_results = self.tester.run_batch(chunk)
            results.update(batch_results)
            working_in_batch = sum(1 for ok, _ in batch_results.values() if ok)
            logger.info(f"Batch {batch_num}/{total_batches}: {working_in_batch}/{len(chunk)} working")

        return results

    def test_all(self, configs: List[str]) -> List[str]:
        total = len(configs)
        logger.info(f"Testing {total} configs with batch size {self.batch_size} over {self.rounds} round(s)...")
        logger.info(f"Base test URLs: {self.base_test_urls}")

        candidates = list(configs)

        for round_num in range(1, self.rounds + 1):
            if not candidates:
                break

            round_url = rotate_urls(self.base_test_urls, round_num - 1)[0]
            self.tester.test_url = round_url
            logger.info(f"--- Round {round_num}/{self.rounds}: {len(candidates)} configs, endpoint {round_url} ---")

            round_results = self._run_single_round(candidates)
            candidates = [cfg for cfg in candidates if round_results.get(cfg, (False, None))[0]]

            success_rate = (len(candidates) * 100) // max(1, total)
            logger.info(f"Round {round_num} result: {len(candidates)}/{total} survive ({success_rate}%)")

        working = candidates
        success_rate = (len(working) * 100) // max(1, total)
        logger.info(f"Final results after {self.rounds} round(s): {len(working)}/{total} working ({success_rate}%)")
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
    batch_size = getattr(config_settings, 'XRAY_TESTER_BATCH_SIZE', 200)
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

    tester = ParallelXrayTester(max_workers=max_workers, timeout=timeout, test_urls=test_urls, rounds=rounds, batch_size=batch_size)
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