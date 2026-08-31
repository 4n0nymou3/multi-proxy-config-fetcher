import socket
import threading
import time


class FakeProcess:
    def __init__(self, alive_for=None):
        self._alive = True
        self._alive_for = alive_for
        self._start = time.time()

    def poll(self):
        if self._alive_for is not None and (time.time() - self._start) > self._alive_for:
            self._alive = False
        return None if self._alive else 1

    def kill(self):
        self._alive = False


class DeadProcess:
    def poll(self):
        return 1


class SlowListenerServer:
    def __init__(self, port, delay_seconds):
        self.port = port
        self.delay_seconds = delay_seconds
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        time.sleep(self.delay_seconds)
        if self._stop.is_set():
            return
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('127.0.0.1', self.port))
            s.listen(1)
            s.settimeout(2.0)
            try:
                conn, _ = s.accept()
                conn.close()
            except socket.timeout:
                pass

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop.set()
        self._thread.join(timeout=1)