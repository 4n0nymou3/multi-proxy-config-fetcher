import json
import base64
import sys
import os
import logging
import re
from typing import Dict, Optional, List
from urllib.parse import urlparse, parse_qs, unquote

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConfigToXray:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file
        self.outbounds = []

    @staticmethod
    def get_xray_template() -> Dict:
        return {
            "log": {
                "loglevel": "warning"
            },
            "remarks": "👽 Anonymous Multi Balanced",
            "dns": {
                "servers": [
                    "https://dns.google/dns-query",
                    "https://cloudflare-dns.com/dns-query",
                    {
                        "address": "1.1.1.2",
                        "domains": [
                            "domain:ir",
                            "geosite:category-ir"
                        ],
                        "skipFallback": True,
                        "tag": "domestic-dns"
                    }
                ]
            },
            "fakedns": [
                {
                    "ipPool": "198.18.0.0/15",
                    "poolSize": 10000
                }
            ],
            "inbounds": [
                {
                    "listen": "127.0.0.1",
                    "port": 10808,
                    "protocol": "socks",
                    "settings": {
                        "auth": "noauth",
                        "udp": True,
                        "userLevel": 8
                    },
                    "sniffing": {
                        "destOverride": [
                            "http",
                            "tls",
                            "fakedns"
                        ],
                        "enabled": True,
                        "routeOnly": False
                    },
                    "tag": "socks"
                }
            ],
            "observatory": {
                "enableConcurrency": True,
                "probeInterval": "3m",
                "probeUrl": "https://www.gstatic.com/generate_204",
                "subjectSelector": [
                    "proxy-"
                ]
            },
            "outbounds": [],
            "policy": {
                "levels": {
                    "8": {
                        "connIdle": 300,
                        "downlinkOnly": 1,
                        "handshake": 4,
                        "uplinkOnly": 1
                    }
                },
                "system": {
                    "statsOutboundUplink": True,
                    "statsOutboundDownlink": True
                }
            },
            "routing": {
                "balancers": [
                    {
                        "selector": [
                            "proxy-"
                        ],
                        "strategy": {
                            "type": "leastPing"
                        },
                        "tag": "proxy-round"
                    }
                ],
                "domainStrategy": "AsIs",
                "rules": [
                    {
                        "inboundTag": [
                            "socks"
                        ],
                        "outboundTag": "dns-out",
                        "port": "53",
                        "type": "field"
                    },
                    {
                        "ip": [
                            "geoip:private"
                        ],
                        "outboundTag": "direct",
                        "type": "field"
                    },
                    {
                        "domain": [
                            "geosite:private"
                        ],
                        "outboundTag": "direct",
                        "type": "field"
                    },
                    {
                        "domain": [
                            "domain:ir",
                            "geosite:category-ir"
                        ],
                        "outboundTag": "direct",
                        "type": "field"
                    },
                    {
                        "ip": [
                            "geoip:ir"
                        ],
                        "outboundTag": "direct",
                        "type": "field"
                    },
                    {
                        "inboundTag": [
                            "domestic-dns"
                        ],
                        "outboundTag": "direct",
                        "type": "field"
                    },
                    {
                        "balancerTag": "proxy-round",
                        "network": "tcp,udp",
                        "type": "field"
                    }
                ]
            }
        }

    @staticmethod
    def decode_vmess(config: str) -> Optional[Dict]:
        try:
            encoded = config.replace('vmess://', '')
            decoded = base64.b64decode(encoded).decode('utf-8')
            return json.loads(decoded)
        except Exception:
            return None

    @staticmethod
    def parse_vless(config: str) -> Optional[Dict]:
        try:
            url = urlparse(config)
            if url.scheme.lower() != 'vless' or not url.hostname:
                return None
            netloc = url.netloc.split('@')[-1]
            address, port = netloc.split(':') if ':' in netloc else (netloc, '443')
            params = parse_qs(url.query)
            return {
                'uuid': url.username,
                'address': address,
                'port': int(port),
                'flow': params.get('flow', [''])[0],
                'sni': params.get('sni', [address])[0],
                'type': params.get('type', ['tcp'])[0],
                'path': params.get('path', [''])[0],
                'host': params.get('host', [address])[0],
                'security': params.get('security', ['none'])[0],
                'alpn': params.get('alpn', [''])[0],
                'fp': params.get('fp', [''])[0]
            }
        except Exception:
            return None

    @staticmethod
    def parse_trojan(config: str) -> Optional[Dict]:
        try:
            url = urlparse(config)
            if url.scheme.lower() != 'trojan' or not url.hostname:
                return None
            port = url.port or 443
            params = parse_qs(url.query)
            return {
                'password': url.username,
                'address': url.hostname,
                'port': port,
                'sni': params.get('sni', [url.hostname])[0],
                'alpn': params.get('alpn', [''])[0],
                'type': params.get('type', ['tcp'])[0],
                'path': params.get('path', [''])[0],
                'host': params.get('host', [url.hostname])[0]
            }
        except Exception:
            return None

    @staticmethod
    def parse_shadowsocks(config: str) -> Optional[Dict]:
        try:
            parts = config.replace('ss://', '').split('@')
            if len(parts) != 2:
                return None
            
            fragment = parts[1].split('#')[0]
            if ':' not in fragment:
                return None
            host, port_str = fragment.rsplit(':', 1)
            port = int(port_str)

            credential_part = unquote(parts[0])
            if ConfigToXray.is_base64(credential_part):
                method_pass_b64 = credential_part.replace('-', '+').replace('_', '/')
                padding = '=' * (-len(method_pass_b64) % 4)
                method_pass = base64.b64decode(method_pass_b64 + padding).decode('utf-8')
                method, password = method_pass.split(':', 1)
            else:
                method, password = credential_part.split(':', 1)

            return {
                'method': method,
                'password': password,
                'address': host,
                'port': port
            }
        except Exception:
            return None
            
    @staticmethod
    def is_base64(s: str) -> bool:
        try:
            s = s.rstrip('=')
            return bool(re.match(r'^[A-Za-z0-9+/\-_]*$', s))
        except:
            return False

    def convert_vmess(self, data: Dict) -> Dict:
        outbound = {
            "protocol": "vmess",
            "settings": {
                "vnext": [
                    {
                        "address": data.get('add'),
                        "port": int(data.get('port')),
                        "users": [
                            {
                                "id": data.get('id'),
                                "alterId": int(data.get('aid', 0)),
                                "security": data.get('scy', 'auto'),
                                "level": 8
                            }
                        ]
                    }
                ]
            },
            "streamSettings": {
                "network": data.get('net', 'tcp'),
                "security": data.get('tls', 'none')
            }
        }

        if data.get('net') == 'ws':
            outbound["streamSettings"]["wsSettings"] = {
                "path": data.get('path', '/'),
                "headers": {"Host": data.get('host', data['add'])}
            }
        
        if data.get('tls') == 'tls':
            outbound["streamSettings"]["tlsSettings"] = {
                "serverName": data.get('sni', data['add']),
                "allowInsecure": False
            }
            if data.get('fp'):
                outbound["streamSettings"]["tlsSettings"]["fingerprint"] = data.get('fp')

        return outbound

    def convert_vless(self, data: Dict) -> Dict:
        outbound = {
            "protocol": "vless",
            "settings": {
                "vnext": [
                    {
                        "address": data['address'],
                        "port": data['port'],
                        "users": [
                            {
                                "id": data['uuid'],
                                "flow": data.get('flow', ''),
                                "encryption": "none",
                                "level": 8
                            }
                        ]
                    }
                ]
            },
            "streamSettings": {
                "network": data.get('type', 'tcp'),
                "security": data.get('security', 'none')
            }
        }

        if data.get('type') == 'ws':
            outbound["streamSettings"]["wsSettings"] = {
                "path": data.get('path', '/'),
                "headers": {"Host": data.get('host', data['address'])}
            }
        
        if data.get('security') == 'tls':
            outbound["streamSettings"]["tlsSettings"] = {
                "serverName": data.get('sni', data['address']),
                "allowInsecure": False
            }
            if data.get('alpn'):
                outbound["streamSettings"]["tlsSettings"]["alpn"] = data['alpn'].split(',')
            if data.get('fp'):
                outbound["streamSettings"]["tlsSettings"]["fingerprint"] = data.get('fp')

        return outbound

    def convert_trojan(self, data: Dict) -> Dict:
        outbound = {
            "protocol": "trojan",
            "settings": {
                "servers": [
                    {
                        "address": data['address'],
                        "port": data['port'],
                        "password": data['password'],
                        "level": 8
                    }
                ]
            },
            "streamSettings": {
                "network": data.get('type', 'tcp'),
                "security": "tls"
            }
        }

        if data.get('type') == 'ws':
            outbound["streamSettings"]["wsSettings"] = {
                "path": data.get('path', '/'),
                "headers": {"Host": data.get('host', data['address'])}
            }
        
        outbound["streamSettings"]["tlsSettings"] = {
            "serverName": data.get('sni', data['address']),
            "allowInsecure": False
        }
        if data.get('alpn'):
            outbound["streamSettings"]["tlsSettings"]["alpn"] = data['alpn'].split(',')

        return outbound

    def convert_shadowsocks(self, data: Dict) -> Dict:
        return {
            "protocol": "shadowsocks",
            "settings": {
                "servers": [
                    {
                        "address": data['address'],
                        "port": data['port'],
                        "method": data['method'],
                        "password": data['password'],
                        "level": 8
                    }
                ]
            },
            "streamSettings": {
                "network": "tcp"
            }
        }

    def process_configs(self):
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            logger.error(f"{self.input_file} not found!")
            return
        except Exception as e:
            logger.error(f"Error reading {self.input_file}: {e}")
            return

        final_config = self.get_xray_template()
        temp_outbounds = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            
            line_lower = line.lower()
            outbound = None

            try:
                if line_lower.startswith('vmess://'):
                    data = self.decode_vmess(line)
                    if data:
                        outbound = self.convert_vmess(data)
                elif line_lower.startswith('vless://'):
                    data = self.parse_vless(line)
                    if data:
                        outbound = self.convert_vless(data)
                elif line_lower.startswith('trojan://'):
                    data = self.parse_trojan(line)
                    if data:
                        outbound = self.convert_trojan(data)
                elif line_lower.startswith('ss://'):
                    data = self.parse_shadowsocks(line)
                    if data:
                        outbound = self.convert_shadowsocks(data)
            except Exception as e:
                logger.warning(f"Failed to parse config {line[:30]}...: {e}")

            if outbound:
                outbound["tag"] = f"proxy-{len(temp_outbounds) + 1}"
                temp_outbounds.append(outbound)
        
        if not temp_outbounds:
            logger.error("No valid configs found to convert.")
            return

        temp_outbounds.extend([
            {"protocol": "freedom", "settings": {}, "tag": "direct"},
            {"protocol": "blackhole", "settings": {"response": {"type": "http"}}, "tag": "block"},
            {"protocol": "dns", "tag": "dns-out"}
        ])
        
        final_config["outbounds"] = temp_outbounds
        
        try:
            os.makedirs(os.path.dirname(self.output_file) or '.', exist_ok=True)
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(final_config, f, indent=2, ensure_ascii=False)
            logger.info(f"Successfully converted {len(temp_outbounds) - 3} configs to {self.output_file}")
        except Exception as e:
            logger.error(f"Failed to write output file: {e}")

def main():
    input_file = 'configs/proxy_configs_tested.txt'
    output_file = 'configs/xray_loadbalanced_config.json'

    converter = ConfigToXray(input_file, output_file)
    converter.process_configs()

if __name__ == '__main__':
    main()
