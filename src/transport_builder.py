import logging
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)

VALID_SINGBOX_FINGERPRINTS = {
    'chrome', 'firefox', 'edge', 'safari', '360', 'qq', 'ios', 'android',
    'random', 'randomized',
    'chrome_psk', 'chrome_psk_shuffle', 'chrome_padding_psk_shuffle',
    'chrome_pq', 'chrome_pq_psk'
}

def sanitize_fingerprint(fp: Optional[str]) -> str:
    if not fp:
        return 'chrome'
    normalized = str(fp).strip().lower()
    if normalized in VALID_SINGBOX_FINGERPRINTS:
        return normalized
    return 'chrome'

def map_transport_for_singbox(net_type: str) -> str:
    transport_map = {
        'httpupgrade': 'ws',
        'splithttp': 'http',
        'xhttp': 'http'
    }
    return transport_map.get(net_type, net_type)

def build_singbox_settings(data: Dict, alpn_override: Optional[list] = None, disable_utls: bool = False) -> Tuple[Dict, Dict]:
    transport = {}
    tls = {"enabled": False}
    
    net_type = data.get('net', data.get('type', 'tcp')).lower()
    security = data.get('security', data.get('tls', 'none')).lower()
    address = data.get('address', data.get('add', ''))
    port = data.get('port', 443)
    
    try:
        net_type = map_transport_for_singbox(net_type)
        
        if net_type == 'ws':
            transport = {
                "type": "ws",
                "path": data.get('path', '/'),
                "headers": {"Host": data.get('host', address)}
            }
        elif net_type == 'grpc':
            transport = {
                "type": "grpc",
                "service_name": data.get('path', data.get('serviceName', ''))
            }
        elif net_type in ('http', 'h2'):
            transport = {
                "type": "http",
                "host": [data.get('host', address)],
                "path": data.get('path', '/')
            }
        elif net_type == 'quic':
            transport = {"type": "quic"}
        elif net_type == 'kcp':
            transport = {"type": "kcp"}
        
        tls_enabled = security in ('tls', 'xtls', 'reality') or port in [443, 2053, 2083, 2087, 2096, 8443]
        
        if security == 'reality':
            tls = {
                "enabled": True,
                "server_name": data.get('sni', address),
                "reality": {
                    "enabled": True,
                    "public_key": data.get('pbk', ''),
                    "short_id": data.get('sid', '')
                },
                "utls": {"enabled": True, "fingerprint": sanitize_fingerprint(data.get('fp'))}
            }
        elif tls_enabled:
            insecure_flag = str(data.get('insecure', '0')).lower() in ('1', 'true')
            tls = {
                "enabled": True,
                "server_name": data.get('sni', address),
                "insecure": insecure_flag,
                "alpn": alpn_override if alpn_override else (data.get('alpn', '').split(',') if data.get('alpn') else ["h2", "http/1.1"]),
            }
            if not disable_utls:
                tls["utls"] = {"enabled": True, "fingerprint": sanitize_fingerprint(data.get('fp'))}
            if security == 'xtls':
                tls["xtls"] = {"enabled": True}

    except Exception as e:
        logger.warning(f"Error building Sing-box settings: {e}")
    
    return transport, tls

def build_xray_settings(data: Dict) -> Dict:
    stream_settings = {"network": "tcp", "security": "none"}
    
    net_type = data.get('net', data.get('type', 'tcp')).lower()
    security = data.get('security', data.get('tls', 'none')).lower()
    address = data.get('address', data.get('add', ''))
    
    try:
        stream_settings["network"] = net_type
        
        if net_type == 'ws':
            stream_settings["wsSettings"] = {
                "path": data.get('path', '/'),
                "headers": {"Host": data.get('host', address)}
            }
        elif net_type == 'grpc':
            stream_settings["grpcSettings"] = {
                "serviceName": data.get('path', data.get('serviceName', ''))
            }
        elif net_type in ('http', 'h2', 'h3', 'quic'):
            stream_settings["network"] = "xhttp"
            stream_settings["xhttpSettings"] = {
                "path": data.get('path', '/'),
                "host": data.get('host', address),
                "mode": "stream-one"
            }
        elif net_type == 'kcp':
            stream_settings["kcpSettings"] = {}
            stream_settings["finalmask"] = {
                "udp": [{"type": "mkcp-original", "settings": {}}]
            }
        elif net_type == 'httpupgrade':
            stream_settings["httpupgradeSettings"] = {
                "path": data.get('path', '/'),
                "host": data.get('host', address)
            }
        elif net_type == 'splithttp':
            splithttp_settings = {
                "path": data.get('path', '/'),
                "host": data.get('host', address)
            }
            if data.get('mode'):
                splithttp_settings["mode"] = data.get('mode')
            stream_settings["splithttpSettings"] = splithttp_settings
        elif net_type == 'xhttp':
            xhttp_settings = {
                "path": data.get('path', '/'),
                "host": data.get('host', address)
            }
            if data.get('mode'):
                xhttp_settings["mode"] = data.get('mode')
            stream_settings["xhttpSettings"] = xhttp_settings
        
        if security == 'reality':
            stream_settings["security"] = "reality"
            stream_settings["realitySettings"] = {
                "serverName": data.get('sni', address),
                "publicKey": data.get('pbk', ''),
                "password": data.get('pbk', ''),
                "shortId": data.get('sid', ''),
                "fingerprint": sanitize_fingerprint(data.get('fp'))
            }
        elif security in ('tls', 'xtls'):
            stream_settings["security"] = "tls"
            stream_settings["tlsSettings"] = {
                "serverName": data.get('sni', address),
                "fingerprint": sanitize_fingerprint(data.get('fp')),
                "alpn": data.get('alpn', '').split(',') if data.get('alpn') else ["h2", "http/1.1"]
            }
            
    except Exception as e:
        logger.warning(f"Error building Xray settings: {e}")
        
    return stream_settings