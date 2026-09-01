# Please modify the settings below according to your needs.

# List of source URLs to fetch proxy configurations from.
# Add or remove URLs as needed. All URLs in this list are automatically enabled.
SOURCE_URLS = [
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mci/sub_1.txt",
    #"https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mci/sub_2.txt",
    #"https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mci/sub_3.txt",
    #"https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mci/sub_4.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_1.txt",
    #"https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_2.txt",
    #"https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_3.txt",
    #"https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_4.txt",
    #"https://raw.githubusercontent.com/MahsaNetConfigTopic/config/refs/heads/main/xray_final.txt",
    "https://raw.githubusercontent.com/Mahdi0024/ProxyCollector/master/sub/proxies.txt",
    "https://raw.githubusercontent.com/zieng2/wl/refs/heads/main/vless_universal.txt",
    "https://raw.githubusercontent.com/iampedii/whitedns-sub/refs/heads/main/base64.txt",
    "https://raw.githubusercontent.com/0xRadikal/Free-v2ray-Configs/main/verified/configs.txt",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/main/subscriptions/xray/mix",
    "https://github.com/Delta-Kronecker/V2ray-Config/raw/refs/heads/main/config/all_configs.txt",
    #"https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt",
    "https://raw.githubusercontent.com/Ashkan-m/v2ray/main/Sub.txt",
    "https://raw.githubusercontent.com/arshiacomplus/v2rayExtractor/refs/heads/main/mix/sub.html",
    #"https://raw.githubusercontent.com/therealaleph/Iran-configs/refs/heads/main/ir_configs.txt",
    "https://t.me/s/persianvpnhub",
]

# Set to True to fetch the maximum possible number of configurations.
# If True, SPECIFIC_CONFIG_COUNT will be ignored.
USE_MAXIMUM_POWER = False

# Desired number of configurations to fetch.
# This is used only if USE_MAXIMUM_POWER is False.
SPECIFIC_CONFIG_COUNT = 600

# Dictionary of protocols to enable or disable.
# Set each protocol to True to enable, False to disable.
ENABLED_PROTOCOLS = {
    "wireguard://": False,
    "hysteria2://": False,
    "vless://": True,
    "vmess://": False,
    "ss://": False,
    "trojan://": True,
    "tuic://": False,
}

# Maximum age of configurations in days.
# Configurations older than this will be considered invalid.
MAX_CONFIG_AGE_DAYS = 1

# --- Xray Config Tester Settings ---

# Set to True to enable testing of configs using Xray core.
# If True, Xray will be used to test all fetched configs before conversion and create a 'tested' config file.
# If False, the testing step will be skipped.
ENABLE_XRAY_TESTER = True

# Number of parallel workers to use for testing Xray configs.
# A higher number means faster testing but uses more CPU/RAM.
XRAY_TESTER_MAX_WORKERS = 24

# Maximum time (in seconds) to wait for an Xray config to respond during testing.
# Configs that take longer than this will be marked as failed.
# Kept short on purpose: most of the total testing time in a large batch is spent
# waiting out this timeout for the many dead/unreachable configs, not for the
# working ones, so a lower value here speeds up the whole run substantially.
XRAY_TESTER_TIMEOUT_SECONDS = 5

# List of URLs to test Xray configs against.
# Before testing starts, this list is automatically checked and any URL that is
# currently unreachable (from the runner itself, without a proxy) is skipped.
XRAY_TESTER_URLS = [
    'https://www.youtube.com/generate_204',
    'https://www.gstatic.com/generate_204',
    'https://cp.cloudflare.com'
]

# Number of independent test rounds a config must pass to be marked as working.
# A config is only kept if it succeeds in every round, which filters out
# "flaky" configs that only appear to work when tested a single time.
# Each round tests against exactly one URL, and that URL changes between
# rounds, so a config is checked against more than one destination overall
# without paying the cost of trying multiple URLs within the same round.
# Higher values are more accurate but take longer to run. 2 is a good default.
XRAY_TESTER_ROUNDS = 3

# Maximum number of configs tested together inside a single shared Xray process.
# Instead of starting a brand new Xray process for every single config, up to
# this many configs are tested through one shared process at once, which
# reduces process startup overhead. If a batch contains a config that prevents
# Xray from starting, the batch is automatically split in half and retried
# until the problem config is isolated, so one bad config cannot block the
# rest of the batch. 200 is a safe default for a public GitHub Actions runner.
XRAY_TESTER_BATCH_SIZE = 200

# --- Sing-box Config Tester Settings ---

# Set to True to enable testing of configs using sing-box.
# If True, sing-box will be used to test all fetched configs and create a 'tested' config file.
# If False, the testing step will be skipped.
ENABLE_SINGBOX_TESTER = True

# Number of parallel workers to use for testing sing-box configs.
# A higher number means faster testing but uses more CPU/RAM.
SINGBOX_TESTER_MAX_WORKERS = 24

# Maximum time (in seconds) to wait for a sing-box config to respond during testing.
# Configs that take longer than this will be marked as failed.
# Kept short on purpose: most of the total testing time in a large batch is spent
# waiting out this timeout for the many dead/unreachable configs, not for the
# working ones, so a lower value here speeds up the whole run substantially.
SINGBOX_TESTER_TIMEOUT_SECONDS = 5

# List of URLs to test sing-box configs against.
# Before testing starts, this list is automatically checked and any URL that is
# currently unreachable (from the runner itself, without a proxy) is skipped.
SINGBOX_TESTER_URLS = [
    'https://www.youtube.com/generate_204',
    'https://www.gstatic.com/generate_204',
    'https://cp.cloudflare.com'
]

# Number of independent test rounds a config must pass to be marked as working.
# A config is only kept if it succeeds in every round, which filters out
# "flaky" configs that only appear to work when tested a single time.
# Each round tests against exactly one URL, and that URL changes between
# rounds, so a config is checked against more than one destination overall
# without paying the cost of trying multiple URLs within the same round.
# Higher values are more accurate but take longer to run. 2 is a good default.
SINGBOX_TESTER_ROUNDS = 3

# Maximum number of configs tested together inside a single shared Sing-box process.
# Instead of starting a brand new Sing-box process for every single config, up to
# this many configs are tested through one shared process at once, which
# reduces process startup overhead. If a batch contains a config that prevents
# Sing-box from starting, the batch is automatically split in half and retried
# until the problem config is isolated, so one bad config cannot block the
# rest of the batch. 200 is a safe default for a public GitHub Actions runner.
SINGBOX_TESTER_BATCH_SIZE = 200

# --- Location API Settings ---

# List of free IP geolocation APIs to identify server countries.
# The system tries APIs in order from top to bottom (first = highest priority).
# If one API fails or is rate-limited, the system automatically tries the next one.
#
# HOW TO ADD AN API:
# Simply add the domain name or full URL. Examples:
#   freeipapi.com
#   ip-api.com
#   https://ipapi.co
#   api.iplocation.net
#
# The system automatically detects the correct API format and endpoint.
# No API key is required for the APIs listed below.
#
# RECOMMENDED FREE APIs (ranked by reliability and rate limits):
#
# 1. freeipapi.com - 60 requests/minute, very fast, no registration
# 2. ip-api.com - 45 requests/minute, very reliable, widely used
# 3. ipapi.co - 1000 requests/day (~30k/month), good accuracy
# 4. ipwhois.app - 10000 requests/month, decent speed
# 5. api.iplocation.net - unlimited, fast, accurate
#
LOCATION_APIS = [
    'api.iplocation.net',
    'freeipapi.com',
    'ip-api.com',
    'ipapi.co'
]