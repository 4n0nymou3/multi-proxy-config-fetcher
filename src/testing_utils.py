import os
import time
import socket
import signal
import subprocess
import logging
import requests
from typing import List
from contextlib import closing, contextmanager

logger = logging.getLogger(__name__)

def find_free_port() -> int:
    max_attempts = 10
    for attempt in range(max_attempts):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            try:
                s.bind(('127.0.0.1', 0))
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                port = s.getsockname()[1]
                
                with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as test_sock:
                    test_sock.settimeout(0.1)
                    try:
                        test_sock.connect(('127.0.0.1', port))
                        continue
                    except (socket.error, socket.timeout):
                        return port
            except OSError as e:
                if attempt == max_attempts - 1:
                    logger.error(f"Failed to find free port after {max_attempts} attempts: {e}")
                    raise
                time.sleep(0.1)
                continue
    raise RuntimeError("Could not find a free port")

def get_usable_test_urls(candidate_urls: List[str], timeout: int = 6) -> List[str]:
    usable = []
    for url in candidate_urls:
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code in (200, 204):
                usable.append(url)
        except Exception as e:
            logger.warning(f"Test endpoint unreachable, skipping: {url} ({str(e)[:80]})")
    if not usable:
        logger.warning("No test endpoints passed preflight check, falling back to full configured list")
        return list(candidate_urls)
    return usable

def rotate_urls(urls: List[str], offset: int) -> List[str]:
    if not urls:
        return urls
    offset = offset % len(urls)
    return urls[offset:] + urls[:offset]

def median_of(values: List[int]) -> int:
    if not values:
        return 999999
    ordered = sorted(values)
    return ordered[len(ordered) // 2]

@contextmanager
def managed_process(command: List[str]):
    process = None
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )
        yield process
    finally:
        if process:
            try:
                if process.poll() is None:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    try:
                        process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                        process.wait(timeout=1)
            except (ProcessLookupError, OSError) as e:
                logger.debug(f"Process cleanup error (ignorable): {e}")
            except Exception as e:
                logger.warning(f"Unexpected error during process cleanup: {e}")
