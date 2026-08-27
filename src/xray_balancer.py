import json
import os
import logging
from typing import Dict
import config_parser as parser
import transport_builder
import xray_template

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConfigToXray:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file
        self.outbounds = []

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
            "streamSettings": transport_builder.build_xray_settings(data)
        }
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
            "streamSettings": transport_builder.build_xray_settings(data)
        }
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
            "streamSettings": transport_builder.build_xray_settings(data)
        }
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

        final_config = xray_template.get_xray_template("👽 Anonymous Multi Balanced")
        temp_outbounds = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            
            line_lower = line.lower()
            outbound = None
            data = None

            try:
                if line_lower.startswith('vmess://'):
                    data = parser.decode_vmess(line)
                    if data:
                        outbound = self.convert_vmess(data)
                elif line_lower.startswith('vless://'):
                    data = parser.parse_vless(line)
                    if data:
                        outbound = self.convert_vless(data)
                elif line_lower.startswith('trojan://'):
                    data = parser.parse_trojan(line)
                    if data:
                        outbound = self.convert_trojan(data)
                elif line_lower.startswith('ss://'):
                    data = parser.parse_shadowsocks(line)
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

        temp_outbounds.extend(xray_template.get_utility_outbounds())
        
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