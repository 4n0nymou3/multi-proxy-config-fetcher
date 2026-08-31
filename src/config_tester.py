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
from testing_utils import find_free_port, get_usable_test_urls, rotate_urls, median_of, managed_process, wait_for_port

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SingBoxBatchTester:
    def __init__(self, singbox_path: str = 'sing-box', timeout: int = 10, test_url: str = None, concurrency: int = 16):
        self.singbox_path = singbox_path
        self.timeout = timeout
        self.test_url = test_url if test_url else 'https://www.youtube.com/generate_204'
        self.concurrency = max(1, concurrency)
        self._verify_singbox()

    def _verify_singbox(self):
        import subprocess
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

    def build_batch_config(self, items: List[Tuple[int, int, Dict]]) -> Dict:
        inbounds = []
        outbounds = []
        rules = []
        for idx, port, outbound in items:
            in_tag = f"in-{idx}"
            real_tag = outbound.get('tag', f'proxy-{idx}')
            inbounds.append({
                "type": "mixed",
                "listen": "127.0.0.1",
                "listen_port": port,
                "tag": in_tag
            })
            outbounds.append(outbound)
            rules.append({
                "inbound": [in_tag],
                "outbound": real_tag
            })
        return {
            "log": {"level": "error"},
            "inbounds": inbounds,
            "outbounds": outbounds,
            "route": {"rules": rules}
        }

    def _test_one(self, port: int, tag: str) -> Tuple[str, bool, Optional[int]]:
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
                return tag, True, delay
            return tag, False, None
        except Exception:
            return tag, False, None

    def run_batch(self, outbounds: List[Dict]) -> Dict[str, Tuple[bool, Optional[int]]]:
        results: Dict[str, Tuple[bool, Optional[int]]] = {}
        if not outbounds:
            return results

        prepared = []
        for idx, outbound in enumerate(outbounds):
            tag = outbound.get('tag', f'unknown-{idx}')
            try:
                port = find_free_port()
            except Exception as e:
                logger.error(f"Port allocation failed for {tag}: {e}")
                results[tag] = (False, None)
                continue
            prepared.append((idx, port, outbound, tag))

        if not prepared:
            return results

        batch_config = self.build_batch_config([(i, p, o) for i, p, o, _ in prepared])

        fd, config_file = tempfile.mkstemp(suffix='.json', text=True, prefix='singbox_batch_')
        try:
            with os.fdopen(fd, 'w') as f:
                json.dump(batch_config, f)
        except Exception as e:
            os.close(fd)
            logger.error(f"Failed to write batch config: {e}")
            for _, _, _, tag in prepared:
                results[tag] = (False, None)
            return results

        try:
            with managed_process([self.singbox_path, 'run', '-c', config_file]) as process:
                probe_port = prepared[0][1]
                if not wait_for_port(process, probe_port, max_wait=5.0):
                    stderr = process.stderr.read().decode('utf-8', errors='ignore') if process.stderr else ''
                    logger.warning(f"Batch of {len(prepared)} failed to start ({stderr[:150]}), bisecting")
                    if len(prepared) == 1:
                        results[prepared[0][3]] = (False, None)
                        return results
                    mid = len(prepared) // 2
                    first_half = [ob for _, _, ob, _ in prepared[:mid]]
                    second_half = [ob for _, _, ob, _ in prepared[mid:]]
                    results.update(self.run_batch(first_half))
                    results.update(self.run_batch(second_half))
                    return results

                with ThreadPoolExecutor(max_workers=min(len(prepared), self.concurrency)) as executor:
                    futures = [executor.submit(self._test_one, port, tag) for _, port, _, tag in prepared]
                    for future in as_completed(futures):
                        tag, ok, delay = future.result()
                        results[tag] = (ok, delay)
        finally:
            if os.path.exists(config_file):
                try:
                    os.unlink(config_file)
                except Exception as e:
                    logger.debug(f"Failed to remove temp batch file {config_file}: {e}")

        for _, _, _, tag in prepared:
            if tag not in results:
                results[tag] = (False, None)

        return results


class ParallelConfigTester:
    def __init__(self, singbox_path: str = 'sing-box', max_workers: int = 8, timeout: int = 10,
                 test_urls: List[str] = None, rounds: int = 2, batch_size: int = 200):
        self.base_test_urls = test_urls if test_urls else ['https://www.youtube.com/generate_204']
        self.tester = SingBoxBatchTester(singbox_path, timeout, self.base_test_urls[0], concurrency=max_workers)
        self.rounds = max(1, rounds)
        self.batch_size = max(1, batch_size)

    def _run_single_round(self, outbounds: List[Dict]) -> Dict[str, Tuple[bool, Optional[int]]]:
        results: Dict[str, Tuple[bool, Optional[int]]] = {}
        total_batches = (len(outbounds) + self.batch_size - 1) // self.batch_size

        for batch_num, i in enumerate(range(0, len(outbounds), self.batch_size), 1):
            chunk = outbounds[i:i + self.batch_size]
            batch_results = self.tester.run_batch(chunk)
            results.update(batch_results)
            working_in_batch = sum(1 for ok, _ in batch_results.values() if ok)
            logger.info(f"Batch {batch_num}/{total_batches}: {working_in_batch}/{len(chunk)} working")

        return results

    def test_all(self, outbounds: List[Dict]) -> List[Dict]:
        total = len(outbounds)
        logger.info(f"Testing {total} configs with batch size {self.batch_size} over {self.rounds} round(s)...")
        logger.info(f"Base test URLs: {self.base_test_urls}")

        candidates = list(outbounds)
        delays_by_tag: Dict[str, List[int]] = {}

        for round_num in range(1, self.rounds + 1):
            if not candidates:
                break

            round_url = rotate_urls(self.base_test_urls, round_num - 1)[0]
            self.tester.test_url = round_url
            logger.info(f"--- Round {round_num}/{self.rounds}: {len(candidates)} configs, endpoint {round_url} ---")

            round_results = self._run_single_round(candidates)
            candidates = [ob for ob in candidates if round_results.get(ob.get('tag'), (False, None))[0]]
            for ob in candidates:
                tag = ob.get('tag')
                ok, delay = round_results[tag]
                delays_by_tag.setdefault(tag, []).append(delay if delay is not None else 0)

            success_rate = (len(candidates) * 100) // max(1, total)
            logger.info(f"Round {round_num} result: {len(candidates)}/{total} survive ({success_rate}%)")

        working = []
        for ob in candidates:
            ob_copy = ob.copy()
            ob_copy['_test_delay'] = median_of(delays_by_tag.get(ob.get('tag'), []))
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
    batch_size = getattr(config_settings, 'TESTER_BATCH_SIZE', 200)
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

    tester = ParallelConfigTester(max_workers=max_workers, timeout=timeout, test_urls=test_urls, rounds=rounds, batch_size=batch_size)
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