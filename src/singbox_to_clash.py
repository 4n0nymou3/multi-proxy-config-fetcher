import json
import os
import logging
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

INPUT_OUTPUT_PAIRS = [
    ('configs/singbox_configs_all.json', 'configs/clash_configs_all.yaml'),
    ('configs/singbox_configs_tested.json', 'configs/clash_configs_tested.yaml'),
    ('configs/singbox_configs_secure.json', 'configs/clash_configs_secure.yaml'),
]


def singbox_outbound_to_clash_proxy(outbound: Dict) -> Optional[Dict]:
    proxy_type = outbound.get('type')
    server = outbound.get('server')
    port = outbound.get('server_port')
    name = outbound.get('tag', '')

    if not proxy_type or not server or not port:
        return None

    transport = outbound.get('transport') or {}
    tls = outbound.get('tls') or {}

    ws_opts = {}
    if transport.get('type') == 'ws':
        ws_opts_inner = {'path': transport.get('path', '/')}
        host = (transport.get('headers') or {}).get('Host')
        if host:
            ws_opts_inner['headers'] = {'Host': host}
        ws_opts = {'ws-opts': ws_opts_inner}

    tls_fields = {}
    if tls.get('enabled'):
        tls_fields = {
            'tls': True,
            'servername': tls.get('server_name', server),
            'skip-cert-verify': tls.get('insecure', False),
            'client-fingerprint': (tls.get('utls') or {}).get('fingerprint', 'chrome'),
        }
        if tls.get('alpn'):
            tls_fields['alpn'] = tls['alpn']

    if proxy_type == 'vmess':
        proxy = {
            'name': name,
            'type': 'vmess',
            'server': server,
            'port': int(port),
            'uuid': outbound.get('uuid', ''),
            'alterId': int(outbound.get('alter_id', 0)),
            'cipher': outbound.get('security', 'auto'),
            'network': transport.get('type', 'tcp'),
        }
        proxy.update(ws_opts)
        proxy.update(tls_fields)
        return proxy

    elif proxy_type == 'vless':
        proxy = {
            'name': name,
            'type': 'vless',
            'server': server,
            'port': int(port),
            'uuid': outbound.get('uuid', ''),
            'network': transport.get('type', 'tcp'),
        }
        proxy.update(ws_opts)
        proxy.update(tls_fields)
        return proxy

    elif proxy_type == 'trojan':
        proxy = {
            'name': name,
            'type': 'trojan',
            'server': server,
            'port': int(port),
            'password': outbound.get('password', ''),
            'sni': tls.get('server_name', server),
            'skip-cert-verify': tls.get('insecure', False),
        }
        if transport.get('type') == 'ws':
            proxy['network'] = 'ws'
            proxy.update(ws_opts)
        return proxy

    elif proxy_type == 'hysteria2':
        return {
            'name': name,
            'type': 'hysteria2',
            'server': server,
            'port': int(port),
            'auth': outbound.get('password', ''),
            'sni': tls.get('server_name', server),
            'skip-cert-verify': tls.get('insecure', True),
        }

    elif proxy_type == 'shadowsocks':
        return {
            'name': name,
            'type': 'ss',
            'server': server,
            'port': int(port),
            'cipher': outbound.get('method', ''),
            'password': outbound.get('password', ''),
        }

    return None


def create_clash_config(clash_proxies: List[Dict], proxy_names: List[str]) -> Dict:
    return {
        'mixed-port': 7890,
        'allow-lan': False,
        'unified-delay': False,
        'log-level': 'silent',
        'mode': 'rule',
        'tcp-concurrent': True,
        'geo-auto-update': True,
        'geo-update-interval': 168,
        'external-controller': '127.0.0.1:9090',
        'external-ui': 'ui',
        'profile': {'store-selected': True, 'store-fake-ip': True},
        'tun': {
            'enable': True,
            'stack': 'mixed',
            'auto-route': True,
            'strict-route': True,
            'auto-detect-interface': True,
            'dns-hijack': ['any:53', 'tcp://any:53'],
            'mtu': 9000,
        },
        'sniffer': {
            'enable': True,
            'force-dns-mapping': True,
            'parse-pure-ip': True,
            'override-destination': True,
            'sniff': {
                'HTTP': {'ports': [80, 8080]},
                'TLS': {'ports': [443, 8443, 2053, 2083, 2087, 2096]},
            },
        },
        'dns': {
            'enable': True,
            'respect-rules': True,
            'use-system-hosts': False,
            'listen': '127.0.0.1:1053',
            'ipv6': False,
            'nameserver': ['https://8.8.8.8/dns-query#\u2705 Anonymous Multi'],
            'proxy-server-nameserver': ['8.8.8.8#DIRECT'],
            'direct-nameserver': ['8.8.8.8#DIRECT'],
            'direct-nameserver-follow-policy': True,
            'nameserver-policy': {'rule-set:geosite-ir': '8.8.8.8#DIRECT'},
            'enhanced-mode': 'fake-ip',
            'fake-ip-range': '198.18.0.1/16',
            'fake-ip-filter-mode': 'blacklist',
            'fake-ip-filter': ['+.lan', '+.local'],
        },
        'proxies': clash_proxies,
        'proxy-groups': [
            {
                'name': '\u2705 Anonymous Multi',
                'type': 'select',
                'proxies': ['\U0001f680 Best Ping'] + proxy_names + ['DIRECT'],
            },
            {
                'name': '\U0001f680 Best Ping',
                'type': 'url-test',
                'proxies': proxy_names,
                'url': 'https://www.gstatic.com/generate_204',
                'interval': 180,
                'tolerance': 50,
            },
        ],
        'rule-providers': {
            'geosite-malware': {'type': 'http', 'format': 'text', 'behavior': 'domain', 'path': './ruleset/geosite-malware.txt', 'interval': 86400, 'url': 'https://raw.githubusercontent.com/Chocolate4U/Iran-clash-rules/release/malware.txt'},
            'geosite-phishing': {'type': 'http', 'format': 'text', 'behavior': 'domain', 'path': './ruleset/geosite-phishing.txt', 'interval': 86400, 'url': 'https://raw.githubusercontent.com/Chocolate4U/Iran-clash-rules/release/phishing.txt'},
            'geosite-cryptominers': {'type': 'http', 'format': 'text', 'behavior': 'domain', 'path': './ruleset/geosite-cryptominers.txt', 'interval': 86400, 'url': 'https://raw.githubusercontent.com/Chocolate4U/Iran-clash-rules/release/cryptominers.txt'},
            'geosite-ads': {'type': 'http', 'format': 'text', 'behavior': 'domain', 'path': './ruleset/geosite-ads.txt', 'interval': 86400, 'url': 'https://raw.githubusercontent.com/Chocolate4U/Iran-clash-rules/release/category-ads-all.txt'},
            'geosite-ir': {'type': 'http', 'format': 'text', 'behavior': 'domain', 'path': './ruleset/geosite-ir.txt', 'interval': 86400, 'url': 'https://raw.githubusercontent.com/Chocolate4U/Iran-clash-rules/release/ir.txt'},
            'geoip-ir': {'type': 'http', 'format': 'text', 'behavior': 'ipcidr', 'path': './ruleset/geoip-ir.txt', 'interval': 86400, 'url': 'https://raw.githubusercontent.com/Chocolate4U/Iran-clash-rules/release/ircidr.txt'},
        },
        'rules': [
            'GEOIP,lan,DIRECT,no-resolve',
            'NETWORK,udp,REJECT',
            'RULE-SET,geosite-malware,REJECT',
            'RULE-SET,geosite-phishing,REJECT',
            'RULE-SET,geosite-cryptominers,REJECT',
            'RULE-SET,geosite-ads,REJECT',
            'RULE-SET,geosite-ir,DIRECT',
            'RULE-SET,geoip-ir,DIRECT',
            'MATCH,\u2705 Anonymous Multi',
        ],
        'ntp': {'enable': True, 'server': 'time.cloudflare.com', 'port': 123, 'interval': 30},
    }


def convert_singbox_to_clash(input_path: str, output_path: str) -> bool:
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            singbox_config = json.load(f)
    except FileNotFoundError:
        logger.error(f"{input_path} not found, skipping.")
        return False
    except Exception as e:
        logger.error(f"Failed to read {input_path}: {e}")
        return False

    proxy_types = {'vmess', 'vless', 'trojan', 'hysteria2', 'shadowsocks'}
    outbounds = singbox_config.get('outbounds', [])
    proxy_outbounds = [o for o in outbounds if o.get('type') in proxy_types]

    if not proxy_outbounds:
        logger.error(f"No proxy outbounds found in {input_path}")
        return False

    clash_proxies = []
    proxy_names = []
    for outbound in proxy_outbounds:
        proxy = singbox_outbound_to_clash_proxy(outbound)
        if proxy:
            clash_proxies.append(proxy)
            proxy_names.append(proxy['name'])

    if not clash_proxies:
        logger.error(f"No valid Clash proxies converted from {input_path}")
        return False

    clash_config = create_clash_config(clash_proxies, proxy_names)

    try:
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(clash_config, f, indent=2, ensure_ascii=False)
        logger.info(f"Converted {len(clash_proxies)} proxies from {input_path} → {output_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to write {output_path}: {e}")
        return False


def main():
    for input_path, output_path in INPUT_OUTPUT_PAIRS:
        convert_singbox_to_clash(input_path, output_path)


if __name__ == '__main__':
    main()