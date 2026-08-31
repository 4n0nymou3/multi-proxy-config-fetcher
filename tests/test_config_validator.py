from config_validator import ConfigValidator


def test_split_configs_dedupes_same_server_different_name():
    text = (
        "vless://11111111-1111-1111-1111-111111111111@1.2.3.4:443?security=tls&type=ws&path=%2Fa&host=x.com#nameA\n"
        "vless://11111111-1111-1111-1111-111111111111@1.2.3.4:443?type=ws&host=x.com&path=%2Fa&security=tls#nameB\n"
    )
    result = ConfigValidator.split_configs(text)
    assert len(result) == 1


def test_split_configs_keeps_distinct_servers():
    text = (
        "vless://11111111-1111-1111-1111-111111111111@1.2.3.4:443?security=tls&type=ws#nameA\n"
        "vless://11111111-1111-1111-1111-111111111111@5.6.7.8:443?security=tls&type=ws#nameB\n"
    )
    result = ConfigValidator.split_configs(text)
    assert len(result) == 2


def test_is_valid_config_rejects_unknown_scheme():
    assert ConfigValidator.is_valid_config("http://example.com") is False


def test_is_valid_config_accepts_known_schemes():
    assert ConfigValidator.is_valid_config("vless://abc@1.2.3.4:443") is True
    assert ConfigValidator.is_valid_config("trojan://abc@1.2.3.4:443") is True