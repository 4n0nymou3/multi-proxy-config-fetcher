from typing import Dict

def get_xray_template(remarks: str) -> Dict:
    return {
        "log": {
            "loglevel": "warning"
        },
        "version": {"min": "26.2.6"},
        "remarks": remarks,
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

def get_utility_outbounds() -> list:
    return [
        {"protocol": "freedom", "settings": {"domainStrategy": "UseIP"}, "tag": "direct"},
        {"protocol": "blackhole", "settings": {"response": {"type": "http"}}, "tag": "block"},
        {"protocol": "dns", "settings": {"rules": [{"action": "hijack"}]}, "tag": "dns-out"}
    ]
