
from typing import Dict, List
from datetime import datetime
import re
import os
import telegram
from telegram.ext import Updater, CommandHandler

# Class to track metrics for each channel
class ChannelMetrics:
    def __init__(self):
        self.total_configs = 0  # Total number of configurations fetched
        self.valid_configs = 0  # Total number of valid configurations
        self.unique_configs = 0  # Total number of unique configurations
        self.avg_response_time = 0  # Average response time of the channel
        self.last_success_time = None  # Timestamp of the last successful fetch
        self.fail_count = 0  # Total number of fetch failures
        self.success_count = 0  # Total number of successful fetches
        self.overall_score = 0.0  # Overall performance score of the channel

# Class representing a single channel configuration
class ChannelConfig:
    def __init__(self, url: str, enabled: bool = True):
        self.url = url  # URL of the channel
        self.enabled = enabled  # Whether the channel is enabled
        self.metrics = ChannelMetrics()  # Metrics object for the channel
        self.is_telegram = bool(re.match(r'^https://t\.me/s/', url))  # Check if the channel is a Telegram channel
        
    # Calculate the overall score for the channel based on its metrics
    def calculate_overall_score(self):
        if self.metrics.success_count + self.metrics.fail_count == 0:
            reliability_score = 0
        else:
            reliability_score = (self.metrics.success_count / (self.metrics.success_count + self.metrics.fail_count)) * 35
        
        if self.metrics.total_configs == 0:
            quality_score = 0
        else:
            quality_score = (self.metrics.valid_configs / self.metrics.total_configs) * 25
        
        if self.metrics.valid_configs == 0:
            uniqueness_score = 0
        else:
            uniqueness_score = (self.metrics.unique_configs / self.metrics.valid_configs) * 25
        
        if self.metrics.avg_response_time == 0:
            response_score = 15
        else:
            response_score = max(0, min(15, 15 * (1 - (self.metrics.avg_response_time / 10))))
        
        self.metrics.overall_score = reliability_score + quality_score + uniqueness_score + response_score

# Main configuration class for the proxy fetcher
class ProxyConfig:
    def __init__(self):
        # List of channels or URLs to fetch proxy configurations from
        self.SOURCE_URLS = [
            ChannelConfig("https://t.me/s/v2ray_free_conf"),
            ChannelConfig("https://t.me/s/PrivateVPNs"),
            ChannelConfig("https://raw.githubusercontent.com/4n0nymou3/wg-config-fetcher/refs/heads/main/configs/wireguard_configs.txt"),
            ChannelConfig("https://raw.githubusercontent.com/4n0nymou3/ss-config-updater/refs/heads/main/configs.txt")
            # ChannelConfig("ssconf://ainita.s3.eu-north-1.amazonaws.com/AinitaServer-1.csv")
        ]

        # Minimum and maximum number of configurations per protocol
        self.PROTOCOL_CONFIG_LIMITS = {
            "min": 5,  # Minimum number of configurations per protocol
            "max": 15  # Maximum number of configurations per protocol
        }

        # Supported proxy protocols and their limits
        self.SUPPORTED_PROTOCOLS: Dict[str, Dict] = {
            "wireguard://": {"min_configs": self.PROTOCOL_CONFIG_LIMITS["min"], "max_configs": self.PROTOCOL_CONFIG_LIMITS["max"]},
            "hysteria2://": {"min_configs": self.PROTOCOL_CONFIG_LIMITS["min"], "max_configs": self.PROTOCOL_CONFIG_LIMITS["max"]},
            "vless://": {"min_configs": self.PROTOCOL_CONFIG_LIMITS["min"], "max_configs": self.PROTOCOL_CONFIG_LIMITS["max"]},
            "vmess://": {"min_configs": self.PROTOCOL_CONFIG_LIMITS["min"], "max_configs": self.PROTOCOL_CONFIG_LIMITS["max"]},
            "ss://": {"min_configs": self.PROTOCOL_CONFIG_LIMITS["min"], "max_configs": self.PROTOCOL_CONFIG_LIMITS["max"]},
            "trojan://": {"min_configs": self.PROTOCOL_CONFIG_LIMITS["min"], "max_configs": self.PROTOCOL_CONFIG_LIMITS["max"]},
            "tuic://": {"min_configs": self.PROTOCOL_CONFIG_LIMITS["min"], "max_configs": self.PROTOCOL_CONFIG_LIMITS["max"]}
        }

        # Minimum and maximum number of configurations fetched from each channel
        self.MIN_CONFIGS_PER_CHANNEL = 5  # Minimum number of proxy configs required per channel
        self.MAX_CONFIGS_PER_CHANNEL = 30  # Maximum number of proxy configs allowed per channel

        # Maximum age of configurations (in days)
        self.MAX_CONFIG_AGE_DAYS = 7  # Discard configurations older than this many days

        # Retry settings for fetching configurations
        self.CHANNEL_RETRY_LIMIT = 3  # Maximum number of retries if a channel fetch fails
        self.CHANNEL_ERROR_THRESHOLD = 0.5  # Error threshold (e.g., 50%) to disable a channel

        # Minimum ratio of configs required for a protocol to be considered valid
        self.MIN_PROTOCOL_RATIO = 0.15  # Protocol must have at least 15% of all fetched configs

        # File paths for saving outputs
        self.OUTPUT_FILE = 'configs/proxy_configs.txt'  # File to save proxy configurations
        self.STATS_FILE = 'configs/channel_stats.json'  # File to save channel statistics

        # HTTP request settings
        self.MAX_RETRIES = 3  # Maximum retries for a failed HTTP request
        self.RETRY_DELAY = 5  # Delay (in seconds) between retries
        self.REQUEST_TIMEOUT = 30  # Timeout (in seconds) for HTTP requests

        # HTTP headers for requests
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    # Check if a protocol is enabled in the supported protocols
    def is_protocol_enabled(self, protocol: str) -> bool:
        return protocol in self.SUPPORTED_PROTOCOLS

    # Get the list of enabled channels
    def get_enabled_channels(self) -> List[ChannelConfig]:
        return [channel for channel in self.SOURCE_URLS if channel.enabled]

    # Update channel statistics after a fetch attempt
    def update_channel_stats(self, channel: ChannelConfig, success: bool, response_time: float = 0):
        if success:
            channel.metrics.success_count += 1
            channel.metrics.last_success_time = datetime.now()
        else:
            channel.metrics.fail_count += 1
        
        if response_time > 0:
            if channel.metrics.avg_response_time == 0:
                channel.metrics.avg_response_time = response_time
            else:
                channel.metrics.avg_response_time = (channel.metrics.avg_response_time * 0.7) + (response_time * 0.3)
        
        channel.calculate_overall_score()
        
        if channel.metrics.overall_score < 30:
            channel.enabled = False

# توکن ربات تلگرام را جایگزین کنید
TOKEN = '7207194239:AAGOkRaytoJMuk_U8_GikFIke2rVF0XLdDY'
CHANNEL_ID = '@proxyfig'

# ایجاد یک نمونه از بات تلگرام
bot = telegram.Bot(token=TOKEN)

def send_configs_to_channel(update, context):
    # خواندن کانفیگ‌ها از فایل
    config_file_path = 'path/to/your/config/file.txt'
    with open(config_file_path, 'r') as file:
        configs = file.read()

    # ارسال کانفیگ‌ها به کانال تلگرام
    bot.send_message(chat_id=CHANNEL_ID, text=configs)
    update.message.reply_text('Configs sent to the Telegram channel!')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # فرمانی برای ارسال کانفیگ‌ها
    dp.add_handler(CommandHandler('send_configs', send_configs_to_channel))

    updater.start_polling()
    updater.idle()

if __name__ ==__main__
 main()
