import json
import os

def count_txt_configs(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return sum(1 for line in lines if line.strip() and not line.strip().startswith('//'))
    except FileNotFoundError:
        return None
    except Exception:
        return None

def count_xray_outbounds(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        utility_protocols = {'freedom', 'blackhole', 'dns'}
        return sum(1 for ob in data.get('outbounds', []) if ob.get('protocol') not in utility_protocols)
    except FileNotFoundError:
        return None
    except Exception:
        return None

def count_singbox_outbounds(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        proxy_types = {'vmess', 'vless', 'trojan', 'hysteria2', 'shadowsocks'}
        return sum(1 for ob in data.get('outbounds', []) if ob.get('type') in proxy_types)
    except FileNotFoundError:
        return None
    except Exception:
        return None

def count_clash_proxies(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return len(data.get('proxies', []))
    except FileNotFoundError:
        return None
    except Exception:
        return None

def format_count(value):
    if value is None:
        return '⚠️ missing'
    return str(value)

def build_summary():
    rows = []

    rows.append(('Raw fetched', 'configs/proxy_configs.txt', format_count(count_txt_configs('configs/proxy_configs.txt'))))
    rows.append(('Xray-tested', 'configs/proxy_configs_tested.txt', format_count(count_txt_configs('configs/proxy_configs_tested.txt'))))
    rows.append(('Sing-box all', 'configs/singbox_configs_all.json', format_count(count_singbox_outbounds('configs/singbox_configs_all.json'))))
    rows.append(('Sing-box tested', 'configs/singbox_configs_tested.json', format_count(count_singbox_outbounds('configs/singbox_configs_tested.json'))))
    rows.append(('Sing-box secure', 'configs/singbox_configs_secure.json', format_count(count_singbox_outbounds('configs/singbox_configs_secure.json'))))
    rows.append(('Xray secure load balanced', 'configs/xray_secure_loadbalanced_config.json', format_count(count_xray_outbounds('configs/xray_secure_loadbalanced_config.json'))))
    rows.append(('Clash all', 'configs/clash_configs_all.yaml', format_count(count_clash_proxies('configs/clash_configs_all.yaml'))))
    rows.append(('Clash tested', 'configs/clash_configs_tested.yaml', format_count(count_clash_proxies('configs/clash_configs_tested.yaml'))))
    rows.append(('Clash secure', 'configs/clash_configs_secure.yaml', format_count(count_clash_proxies('configs/clash_configs_secure.yaml'))))
    rows.append(('Xray load balanced', 'configs/xray_loadbalanced_config.json', format_count(count_xray_outbounds('configs/xray_loadbalanced_config.json'))))
    rows.append(('Xray Fragment load balanced', 'configs/xray_fragment_loadbalanced_config.json', format_count(count_xray_outbounds('configs/xray_fragment_loadbalanced_config.json'))))

    lines = []
    lines.append('## Multi Pipeline Run Summary')
    lines.append('')
    lines.append('| Stage | File | Config Count |')
    lines.append('|---|---|---|')
    for name, path, count in rows:
        lines.append(f'| {name} | `{path}` | {count} |')
    lines.append('')
    lines.append('A missing file means that stage failed or produced no output this run.')

    return '\n'.join(lines)

def main():
    summary = build_summary()
    print(summary)

    summary_path = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary_path:
        try:
            with open(summary_path, 'a', encoding='utf-8') as f:
                f.write(summary + '\n')
        except Exception as e:
            print(f"Could not write to GITHUB_STEP_SUMMARY: {e}")

if __name__ == '__main__':
    main()