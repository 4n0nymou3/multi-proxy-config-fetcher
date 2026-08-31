from xray_config_tester import XrayBatchTester, ParallelXrayTester


class DummyTester(XrayBatchTester):
    def _verify_xray(self):
        pass


def make_tester():
    return DummyTester(xray_path='xray', timeout=5, test_url='https://example.com', concurrency=4)


def test_build_batch_config_structure():
    tester = make_tester()
    outbound1 = {"protocol": "vless", "settings": {}, "streamSettings": {}}
    outbound2 = {"protocol": "trojan", "settings": {}, "streamSettings": {}}
    items = [(0, 10001, outbound1), (1, 10002, outbound2)]
    batch = tester.build_batch_config(items)

    assert len(batch['inbounds']) == 2
    assert len(batch['outbounds']) == 2
    assert len(batch['routing']['rules']) == 2
    assert batch['inbounds'][0]['tag'] == 'in-0'
    assert batch['inbounds'][0]['port'] == 10001
    assert batch['inbounds'][1]['tag'] == 'in-1'
    assert batch['inbounds'][1]['port'] == 10002
    assert batch['outbounds'][0]['tag'] == 'out-0'
    assert batch['outbounds'][0]['protocol'] == 'vless'
    assert batch['routing']['rules'][0]['inboundTag'] == ['in-0']
    assert batch['routing']['rules'][0]['outboundTag'] == 'out-0'


def test_build_batch_config_does_not_mutate_original_outbound():
    tester = make_tester()
    outbound = {"protocol": "vless", "settings": {}}
    tester.build_batch_config([(0, 10001, outbound)])
    assert 'tag' not in outbound


def test_is_supported_protocol():
    tester = make_tester()
    assert tester.is_supported_protocol('vless://x@a:1') is True
    assert tester.is_supported_protocol('tuic://x@a:1') is False
    assert tester.is_supported_protocol('wireguard://x@a:1') is False


def test_parse_config_string_vless_has_no_allow_insecure():
    tester = make_tester()
    ob = tester.parse_config_string('vless://11111111-1111-1111-1111-111111111111@1.2.3.4:443?security=tls')
    assert ob is not None
    assert ob['protocol'] == 'vless'
    assert 'allowInsecure' not in str(ob)


def test_parse_config_string_returns_none_for_garbage():
    tester = make_tester()
    assert tester.parse_config_string('vless://') is None


def test_multi_round_intersection_keeps_only_configs_passing_every_round(monkeypatch):
    call_count = {'n': 0}

    def fake_run_batch(self, entries):
        call_count['n'] += 1
        results = {}
        for cs, ob in entries:
            if 'alwaysgood' in cs:
                results[cs] = (True, 10)
            elif 'onlyround1' in cs:
                results[cs] = (True, 10) if call_count['n'] == 1 else (False, None)
            else:
                results[cs] = (False, None)
        return results

    monkeypatch.setattr(XrayBatchTester, 'run_batch', fake_run_batch)
    monkeypatch.setattr(XrayBatchTester, '_verify_xray', lambda self: None)

    configs = [
        'vless://11111111-1111-1111-1111-111111111111@1.2.3.4:443?security=tls#alwaysgood',
        'vless://11111111-1111-1111-1111-111111111111@5.6.7.8:443?security=tls#onlyround1',
        'vless://11111111-1111-1111-1111-111111111111@9.9.9.9:443?security=tls#alwaysbad',
    ]

    tester = ParallelXrayTester(xray_path='xray', max_workers=4, timeout=1, test_urls=['https://a.com'], rounds=2, batch_size=10)
    working = tester.test_all(configs)

    assert len(working) == 1
    assert 'alwaysgood' in working[0]


def test_unsupported_protocol_always_passes_through(monkeypatch):
    monkeypatch.setattr(XrayBatchTester, '_verify_xray', lambda self: None)

    def fake_run_batch(self, entries):
        return {cs: (False, None) for cs, ob in entries}

    monkeypatch.setattr(XrayBatchTester, 'run_batch', fake_run_batch)

    configs = ['wireguard://key@1.2.3.4:51820']
    tester = ParallelXrayTester(xray_path='xray', max_workers=4, timeout=1, test_urls=['https://a.com'], rounds=2, batch_size=10)
    working = tester.test_all(configs)

    assert working == configs