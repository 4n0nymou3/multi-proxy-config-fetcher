import json
import transport_builder


def test_tls_stream_settings_never_contain_allow_insecure():
    data = {'net': 'tcp', 'security': 'tls', 'address': 'example.com', 'sni': 'example.com'}
    settings = transport_builder.build_xray_settings(data)
    serialized = json.dumps(settings).lower()
    assert 'allowinsecure' not in serialized


def test_xtls_stream_settings_never_contain_allow_insecure():
    data = {'net': 'tcp', 'security': 'xtls', 'address': 'example.com', 'sni': 'example.com'}
    settings = transport_builder.build_xray_settings(data)
    serialized = json.dumps(settings).lower()
    assert 'allowinsecure' not in serialized


def test_reality_security_produces_reality_settings_not_tls():
    data = {
        'net': 'tcp', 'security': 'reality', 'address': 'example.com',
        'sni': 'example.com', 'pbk': 'somepublickey', 'sid': 'abcd', 'fp': 'chrome'
    }
    settings = transport_builder.build_xray_settings(data)
    assert settings['security'] == 'reality'
    assert 'realitySettings' in settings
    assert settings['realitySettings']['publicKey'] == 'somepublickey'
    assert 'tlsSettings' not in settings


def test_xhttp_mode_passthrough_when_present():
    data = {'net': 'xhttp', 'security': 'none', 'address': 'example.com', 'mode': 'packet-up', 'path': '/x', 'host': 'example.com'}
    settings = transport_builder.build_xray_settings(data)
    assert settings['xhttpSettings']['mode'] == 'packet-up'


def test_xhttp_mode_omitted_when_absent():
    data = {'net': 'xhttp', 'security': 'none', 'address': 'example.com', 'mode': '', 'path': '/x', 'host': 'example.com'}
    settings = transport_builder.build_xray_settings(data)
    assert 'mode' not in settings['xhttpSettings']


def test_singbox_reality_settings_shape():
    data = {
        'net': 'tcp', 'security': 'reality', 'address': 'example.com',
        'sni': 'example.com', 'pbk': 'somepublickey', 'sid': 'abcd', 'fp': 'chrome'
    }
    transport, tls = transport_builder.build_singbox_settings(data)
    assert tls['enabled'] is True
    assert tls['reality']['enabled'] is True
    assert tls['reality']['public_key'] == 'somepublickey'