import json
import base64
import re
import logging
from typing import Dict, Optional
from urllib.parse import urlparse, parse_qs, unquote
import binascii
from functools import lru_cache

logger = logging.getLogger(__name__)

def _fix_query_string(query: str) -> str:
    return query.replace('&amp;', '&')

def repair_trapped_fragment_params(config: str) -> str:
    parts = config.split('#')
    if len(parts) < 3:
        return config
    base = parts[0]
    middle = parts[1]
    rest = '#'.join(parts[2:])
    if '=' in middle and '&' in middle:
        separator = '&' if '?' in base else '?'
        return base + separator + middle + '#' + rest
    return config

VALID_SS_METHODS = {
    'aes-128-gcm', 'aes-192-gcm', 'aes-256-gcm',
    'chacha20-ietf-poly1305', 'xchacha20-ietf-poly1305',
    '2022-blake3-aes-128-gcm', '2022-blake3-aes-256-gcm',
    'aes-128-cfb', 'aes-192-cfb', 'aes-256-cfb',
    'aes-128-ctr', 'aes-192-ctr', 'aes-256-ctr',
    'chacha20', 'chacha20-ietf', 'rc4-md5'
}

VALID_VLESS_FLOWS = {'', 'xtls-rprx-vision'}
VALID_VLESS_SECURITY = {'none', 'tls', 'reality', 'xtls'}
VALID_TRANSPORT_TYPES = {'tcp', 'kcp', 'ws', 'http', 'h2', 'quic', 'grpc', 'httpupgrade', 'splithttp', 'xhttp', 'raw'}
VALID_XHTTP_MODES = {'auto', 'packet-up', 'stream-up', 'stream-one'}

def is_base64(s: str) -> bool:
    if not s or len(s) < 4:
        return False
    try:
        s = s.rstrip('=')
        return bool(re.match(r'^[A-Za-z0-9+/\-_]+$', s)) and len(s) % 4 in (0, 2, 3)
    except Exception:
        return False

@lru_cache(maxsize=2048)
def safe_b64decode(s: str) -> Optional[str]:
    if not s:
        return None
    try:
        s = s.replace('-', '+').replace('_', '/')
        padding = '=' * (-len(s) % 4)
        decoded = base64.b64decode(s + padding, validate=True)
        return decoded.decode('utf-8', errors='strict')
    except (binascii.Error, UnicodeDecodeError, ValueError):
        pass
    
    try:
        s_original = s.replace('-', '+').replace('_', '/')
        decoded = base64.b64decode(s_original)
        return decoded.decode('utf-8', errors='ignore')
    except Exception:
        return None

def decode_vmess(config: str) -> Optional[Dict]:
    if not config or not isinstance(config, str) or not config.startswith('vmess://'):
        return None
    
    encoded = config[8:].strip()
    if not encoded:
        return None
    
    decoded = safe_b64decode(encoded)
    if not decoded:
        return None
    
    try:
        data = json.loads(decoded)
    except json.JSONDecodeError:
        return None
    
    if not isinstance(data, dict):
        return None
    
    required_fields = ['add', 'port', 'id']
    if not all(field in data and data[field] for field in required_fields):
        return None
    
    try:
        data['port'] = int(data['port'])
    except (ValueError, TypeError):
        return None
    
    data['name'] = data.get('ps', data.get('name', ''))
    data['net'] = data.get('net', 'tcp').lower()
    data['tls'] = data.get('tls', 'none').lower()

    valid_security = {'auto', 'aes-128-gcm', 'chacha20-poly1305', 'none', 'zero'}
    scy = str(data.get('scy') or 'auto').strip().lower()
    data['scy'] = scy if scy in valid_security else 'auto'

    if data['net'] not in VALID_TRANSPORT_TYPES:
        data['net'] = 'tcp'
    
    return data

def parse_vless(config: str) -> Optional[Dict]:
    if not config or not isinstance(config, str) or not config.startswith('vless://'):
        return None
    
    config = repair_trapped_fragment_params(config)
    
    try:
        url = urlparse(config)
    except Exception:
        return None
    
    if not url.hostname or not url.username:
        return None
    
    port = url.port or 443
    
    params = parse_qs(_fix_query_string(url.query))
    security = params.get('security', ['none'])[0].lower()
    if security not in VALID_VLESS_SECURITY:
        security = 'none'
    
    flow = params.get('flow', [''])[0].lower()
    if flow and flow not in VALID_VLESS_FLOWS:
        flow = ''
    
    transport_type = params.get('type', ['tcp'])[0].lower()
    if transport_type not in VALID_TRANSPORT_TYPES:
        transport_type = 'tcp'
    
    mode = params.get('mode', [''])[0].lower()
    if mode not in VALID_XHTTP_MODES:
        mode = ''
    
    return {
        'uuid': unquote(url.username),
        'address': url.hostname,
        'port': port,
        'flow': flow,
        'sni': params.get('sni', [url.hostname])[0],
        'type': transport_type,
        'path': params.get('path', [''])[0],
        'serviceName': params.get('serviceName', [''])[0],
        'host': params.get('host', [url.hostname])[0],
        'security': security,
        'alpn': params.get('alpn', [''])[0],
        'fp': params.get('fp', [''])[0],
        'pbk': params.get('pbk', [''])[0],
        'sid': params.get('sid', [''])[0],
        'spx': params.get('spx', [''])[0],
        'mode': mode,
        'name': unquote(url.fragment) if url.fragment else ''
    }

def parse_trojan(config: str) -> Optional[Dict]:
    if not config or not isinstance(config, str) or not config.startswith('trojan://'):
        return None
    
    config = repair_trapped_fragment_params(config)
    
    try:
        url = urlparse(config)
    except Exception:
        return None
    
    if not url.hostname or not url.username:
        return None
    
    port = url.port or 443
    
    params = parse_qs(_fix_query_string(url.query))
    transport_type = params.get('type', ['tcp'])[0].lower()
    if transport_type not in VALID_TRANSPORT_TYPES:
        transport_type = 'tcp'
    
    mode = params.get('mode', [''])[0].lower()
    if mode not in VALID_XHTTP_MODES:
        mode = ''
    
    trojan_flow = params.get('flow', [''])[0].lower()
    if trojan_flow and trojan_flow not in VALID_VLESS_FLOWS:
        trojan_flow = ''

    return {
        'password': unquote(url.username),
        'address': url.hostname,
        'port': port,
        'sni': params.get('sni', [url.hostname])[0],
        'alpn': params.get('alpn', [''])[0],
        'type': transport_type,
        'path': params.get('path', [''])[0],
        'serviceName': params.get('serviceName', [''])[0],
        'host': params.get('host', [url.hostname])[0],
        'security': params.get('security', ['tls'])[0],
        'fp': params.get('fp', [''])[0],
        'flow': trojan_flow,
        'pbk': params.get('pbk', [''])[0],
        'sid': params.get('sid', [''])[0],
        'spx': params.get('spx', [''])[0],
        'mode': mode,
        'name': unquote(url.fragment) if url.fragment else ''
    }

def parse_hysteria2(config: str) -> Optional[Dict]:
    if not config or not isinstance(config, str) or not config.startswith(('hysteria2://', 'hy2://')):
        return None
    
    try:
        url = urlparse(config)
    except Exception:
        return None
    
    if not url.hostname:
        return None
    
    try:
        port = url.port or 443
    except ValueError:
        netloc_host = url.netloc.rsplit('@', 1)[-1]
        port_part = netloc_host.rsplit(':', 1)[-1] if ':' in netloc_host else ''
        first_port = re.split(r'[-,]', port_part)[0].strip()
        if not first_port.isdigit():
            return None
        port = int(first_port)
    
    params = parse_qs(_fix_query_string(url.query))
    password = unquote(url.username) if url.username else params.get('password', [''])[0]
    if not password:
        return None
    
    return {
        'address': url.hostname,
        'port': port,
        'password': password,
        'security': 'tls',
        'sni': params.get('sni', [url.hostname])[0],
        'obfs': params.get('obfs', [''])[0],
        'obfs-password': params.get('obfs-password', [''])[0],
        'insecure': params.get('insecure', ['0'])[0],
        'pinSHA256': params.get('pinSHA256', [''])[0],
        'name': unquote(url.fragment) if url.fragment else ''
    }

def parse_shadowsocks(config: str) -> Optional[Dict]:
    if not config or not isinstance(config, str) or not config.startswith('ss://'):
        return None
    
    try:
        fragment_index = config.find('#')
        if fragment_index != -1:
            url_part = config[:fragment_index]
            fragment = config[fragment_index+1:]
        else:
            url_part = config
            fragment = ''
        
        url_part = url_part[5:]
        
        if '@' in url_part:
            credential_part, server_part = url_part.split('@', 1)
            
            if ':' not in server_part:
                return None
            
            host, port_str = server_part.rsplit(':', 1)
            host = host.strip('[]')
            
            try:
                port = int(port_str)
            except ValueError:
                return None
            
            credential_decoded = unquote(credential_part)
            
            if is_base64(credential_decoded):
                method_pass = safe_b64decode(credential_decoded)
                if not method_pass or ':' not in method_pass:
                    return None
                method, password = method_pass.split(':', 1)
            else:
                if ':' not in credential_decoded:
                    return None
                method, password = credential_decoded.split(':', 1)
        else:
            full_decoded = safe_b64decode(url_part)
            if not full_decoded:
                return None
            
            if '@' not in full_decoded:
                return None
            
            credential_part, server_part = full_decoded.split('@', 1)
            
            if ':' not in server_part:
                return None
            
            host, port_str = server_part.rsplit(':', 1)
            host = host.strip('[]')
            
            try:
                port = int(port_str)
            except ValueError:
                return None
            
            if ':' not in credential_part:
                return None
            
            method, password = credential_part.split(':', 1)
        
        if not method or not password:
            return None
        
        method = method.lower().strip()
        if method not in VALID_SS_METHODS:
            return None
        
        return {
            'method': method,
            'password': password,
            'address': host,
            'port': port,
            'plugin': '',
            'name': unquote(fragment) if fragment else ''
        }
    
    except Exception as e:
        logger.debug(f"Shadowsocks parse error: {e}")
        return None

def parse_wireguard(config: str) -> Optional[Dict]:
    if not config or not isinstance(config, str) or not config.startswith('wireguard://'):
        return None
    
    try:
        url = urlparse(config)
    except Exception:
        return None
    
    if not url.hostname:
        return None
    
    port = url.port or 51820
    
    params = parse_qs(_fix_query_string(url.query))
    private_key = unquote(url.username) if url.username else params.get('privatekey', [''])[0]
    if not private_key:
        return None
    
    return {
        'address': url.hostname,
        'port': port,
        'private_key': private_key,
        'public_key': params.get('publickey', [''])[0],
        'preshared_key': params.get('presharedkey', [''])[0],
        'reserved': params.get('reserved', [''])[0],
        'mtu': params.get('mtu', ['1420'])[0],
        'local_address': params.get('address', [''])[0],
        'peers': params.get('peer', []),
        'name': unquote(url.fragment) if url.fragment else ''
    }

def parse_tuic(config: str) -> Optional[Dict]:
    if not config or not isinstance(config, str) or not config.startswith('tuic://'):
        return None
    
    try:
        url = urlparse(config)
    except Exception:
        return None
    
    if not url.hostname:
        return None
    
    port = url.port or 443
    
    if not url.username or ':' not in url.username:
        return None
    
    try:
        uuid, password = url.username.split(':', 1)
        uuid = unquote(uuid)
        password = unquote(password)
    except ValueError:
        return None
    
    params = parse_qs(_fix_query_string(url.query))
    
    return {
        'address': url.hostname,
        'port': port,
        'uuid': uuid,
        'password': password,
        'congestion_control': params.get('congestion_control', ['bbr'])[0],
        'udp_relay_mode': params.get('udp_relay_mode', ['native'])[0],
        'alpn': params.get('alpn', ['h3'])[0],
        'sni': params.get('sni', [url.hostname])[0],
        'allow_insecure': params.get('allow_insecure', ['0'])[0],
        'disable_sni': params.get('disable_sni', ['0'])[0],
        'name': unquote(url.fragment) if url.fragment else ''
    }

def compute_identity(config: str) -> str:
    if not config or not isinstance(config, str):
        return config
    
    cleaned = config.strip()
    low = cleaned.lower()
    
    try:
        if low.startswith('vmess://'):
            data = decode_vmess(cleaned)
            if data:
                return '|'.join(['vmess', str(data.get('add', '')).lower(), str(data.get('port', '')),
                                  str(data.get('id', '')).lower(), str(data.get('net', 'tcp')).lower(),
                                  str(data.get('tls', 'none')).lower(), str(data.get('path', '')),
                                  str(data.get('host', '')).lower()])
        elif low.startswith('vless://'):
            data = parse_vless(cleaned)
            if data:
                return '|'.join(['vless', str(data.get('address', '')).lower(), str(data.get('port', '')),
                                  str(data.get('uuid', '')).lower(), str(data.get('type', 'tcp')),
                                  str(data.get('security', 'none')), str(data.get('flow', '')),
                                  str(data.get('path', '')), str(data.get('host', '')).lower(),
                                  str(data.get('sni', '')).lower(), str(data.get('pbk', ''))])
        elif low.startswith('trojan://'):
            data = parse_trojan(cleaned)
            if data:
                return '|'.join(['trojan', str(data.get('address', '')).lower(), str(data.get('port', '')),
                                  str(data.get('password', '')), str(data.get('type', 'tcp')),
                                  str(data.get('path', '')), str(data.get('host', '')).lower()])
        elif low.startswith(('hysteria2://', 'hy2://')):
            data = parse_hysteria2(cleaned)
            if data:
                return '|'.join(['hysteria2', str(data.get('address', '')).lower(), str(data.get('port', '')),
                                  str(data.get('password', ''))])
        elif low.startswith('ss://'):
            data = parse_shadowsocks(cleaned)
            if data:
                return '|'.join(['ss', str(data.get('address', '')).lower(), str(data.get('port', '')),
                                  str(data.get('method', '')), str(data.get('password', ''))])
        elif low.startswith('wireguard://'):
            data = parse_wireguard(cleaned)
            if data:
                return '|'.join(['wireguard', str(data.get('address', '')).lower(), str(data.get('port', '')),
                                  str(data.get('private_key', ''))])
        elif low.startswith('tuic://'):
            data = parse_tuic(cleaned)
            if data:
                return '|'.join(['tuic', str(data.get('address', '')).lower(), str(data.get('port', '')),
                                  str(data.get('uuid', '')).lower(), str(data.get('password', ''))])
    except Exception as e:
        logger.debug(f"compute_identity fallback for config due to: {e}")
    
    fragment_index = cleaned.find('#')
    if fragment_index != -1:
        cleaned = cleaned[:fragment_index]
    return cleaned.lower()

def extract_address(config: str) -> Optional[str]:
    try:
        config_lower = config.lower()
        data = None

        if config_lower.startswith('vmess://'):
            data = decode_vmess(config)
            if data and 'add' in data:
                return data['add']

        elif config_lower.startswith('vless://'):
            data = parse_vless(config)

        elif config_lower.startswith('trojan://'):
            data = parse_trojan(config)

        elif config_lower.startswith(('hysteria2://', 'hy2://')):
            data = parse_hysteria2(config)

        elif config_lower.startswith('ss://'):
            data = parse_shadowsocks(config)

        if data and 'address' in data:
            return data['address']

        return None
    except Exception as e:
        logger.debug(f"Failed to extract address from config: {e}")
        return None