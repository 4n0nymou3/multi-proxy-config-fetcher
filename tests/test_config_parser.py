import config_parser as parser


def test_parse_vless_basic_fields():
    link = "vless://11111111-1111-1111-1111-111111111111@example.com:443?security=tls&type=ws&path=%2Fabc&host=x.com&sni=example.com#myname"
    data = parser.parse_vless(link)
    assert data is not None
    assert data['uuid'] == '11111111-1111-1111-1111-111111111111'
    assert data['address'] == 'example.com'
    assert data['port'] == 443
    assert data['security'] == 'tls'
    assert data['type'] == 'ws'
    assert data['path'] == '/abc'
    assert data['name'] == 'myname'


def test_parse_vless_rejects_missing_uuid():
    assert parser.parse_vless("vless://@example.com:443") is None


def test_parse_vless_xhttp_mode_field():
    link = "vless://11111111-1111-1111-1111-111111111111@example.com:443?type=xhttp&mode=packet-up"
    data = parser.parse_vless(link)
    assert data['mode'] == 'packet-up'


def test_parse_trojan_basic_fields():
    link = "trojan://mypassword@example.com:443?sni=example.com#mytrojan"
    data = parser.parse_trojan(link)
    assert data is not None
    assert data['password'] == 'mypassword'
    assert data['address'] == 'example.com'
    assert data['port'] == 443


def test_decode_vmess_valid_base64_json():
    import base64
    import json
    payload = {
        "add": "example.com",
        "port": "443",
        "id": "11111111-1111-1111-1111-111111111111",
        "net": "ws",
        "tls": "tls"
    }
    encoded = base64.b64encode(json.dumps(payload).encode()).decode()
    link = f"vmess://{encoded}"
    data = parser.decode_vmess(link)
    assert data is not None
    assert data['add'] == 'example.com'
    assert data['port'] == 443


def test_decode_vmess_rejects_garbage():
    assert parser.decode_vmess("vmess://not-valid-base64-json!!!") is None


def test_parse_shadowsocks_plain_form():
    link = "ss://aes-128-gcm:mypassword@example.com:8388#myss"
    data = parser.parse_shadowsocks(link)
    assert data is not None
    assert data['method'] == 'aes-128-gcm'
    assert data['password'] == 'mypassword'
    assert data['address'] == 'example.com'
    assert data['port'] == 8388


def test_parse_shadowsocks_accepts_legacy_method_format_parsing_only():
    link = "ss://rc4-md5:mypassword@example.com:8388"
    data = parser.parse_shadowsocks(link)
    assert data is not None
    assert data['method'] == 'rc4-md5'


def test_parse_shadowsocks_rejects_unknown_method():
    link = "ss://not-a-real-cipher:mypassword@example.com:8388"
    data = parser.parse_shadowsocks(link)
    assert data is None


def test_compute_identity_ignores_name_and_param_order():
    link1 = "vless://11111111-1111-1111-1111-111111111111@1.2.3.4:443?security=tls&type=ws&path=%2Fabc&host=x.com#nameA"
    link2 = "vless://11111111-1111-1111-1111-111111111111@1.2.3.4:443?type=ws&host=x.com&path=%2Fabc&security=tls#nameB-totally-different"
    assert parser.compute_identity(link1) == parser.compute_identity(link2)


def test_compute_identity_differs_for_different_servers():
    link1 = "vless://11111111-1111-1111-1111-111111111111@1.2.3.4:443?security=tls&type=ws"
    link2 = "vless://11111111-1111-1111-1111-111111111111@5.6.7.8:443?security=tls&type=ws"
    assert parser.compute_identity(link1) != parser.compute_identity(link2)


def test_compute_identity_differs_for_different_uuid():
    link1 = "vless://11111111-1111-1111-1111-111111111111@1.2.3.4:443?security=tls"
    link2 = "vless://22222222-2222-2222-2222-222222222222@1.2.3.4:443?security=tls"
    assert parser.compute_identity(link1) != parser.compute_identity(link2)