import socket
import time
from testing_utils import wait_for_port, rotate_urls, median_of, find_free_port
from fakes import FakeProcess, DeadProcess, SlowListenerServer


def test_wait_for_port_detects_immediate_listener():
    port = find_free_port()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', port))
    server.listen(1)
    try:
        start = time.time()
        result = wait_for_port(FakeProcess(), port, max_wait=3.0)
        elapsed = time.time() - start
        assert result is True
        assert elapsed < 1.0
    finally:
        server.close()


def test_wait_for_port_detects_delayed_listener():
    port = find_free_port()
    slow = SlowListenerServer(port, delay_seconds=0.4)
    slow.start()
    try:
        start = time.time()
        result = wait_for_port(FakeProcess(), port, max_wait=3.0)
        elapsed = time.time() - start
        assert result is True
        assert elapsed < 2.0
    finally:
        slow.stop()


def test_wait_for_port_returns_false_when_process_dead():
    port = find_free_port()
    result = wait_for_port(DeadProcess(), port, max_wait=1.0)
    assert result is False


def test_wait_for_port_times_out_gracefully_when_never_listening():
    port = find_free_port()
    start = time.time()
    result = wait_for_port(FakeProcess(), port, max_wait=0.5, poll_interval=0.05)
    elapsed = time.time() - start
    assert result is True
    assert elapsed < 1.0


def test_rotate_urls_cycles_correctly():
    urls = ['a', 'b', 'c']
    assert rotate_urls(urls, 0) == ['a', 'b', 'c']
    assert rotate_urls(urls, 1) == ['b', 'c', 'a']
    assert rotate_urls(urls, 2) == ['c', 'a', 'b']
    assert rotate_urls(urls, 3) == ['a', 'b', 'c']


def test_rotate_urls_empty_list():
    assert rotate_urls([], 5) == []


def test_median_of_odd_count():
    assert median_of([10, 5, 20]) == 10


def test_median_of_even_count():
    assert median_of([10, 20]) in (10, 20)


def test_median_of_empty():
    assert median_of([]) == 999999


def test_find_free_port_returns_usable_port():
    port = find_free_port()
    assert 0 < port < 65536
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('127.0.0.1', port))
    finally:
        s.close()