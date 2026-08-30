# ⚙️ Anonymous Wizard — English Setup Guide

<p align="center">
  <img src="https://img.shields.io/badge/Anonymous-Wizard-blue?style=for-the-badge" />
</p>

A complete step-by-step guide for installing, running and managing the **Multi Proxy Config Fetcher** project on your local system — including Termux (Android), Linux, macOS, iSH (iOS), and Windows (via WSL2).

---

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Automatic Installation with the Wizard](#-automatic-installation-with-the-wizard)
- [Manual Installation](#-manual-installation)
- [Running the Project](#️-running-the-project)
- [Output Files](#-output-files)
- [Using the Configs](#-using-the-configs)
- [Management Script](#️-management-script)
- [Scheduling](#-scheduling)
- [Customizing Sources and Settings](#-customizing-sources-and-settings)
- [Customizing the Fragment Endpoint](#-customizing-the-fragment-endpoint)
- [Security Notes](#-security-notes)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Updating](#-updating)
- [Quick Start for Termux](#-quick-start-for-termux)

---

## 📦 Prerequisites

The Wizard installs everything below automatically. If you're installing manually, make sure you have:

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.9+ | Runs the pipeline |
| pip | Latest | Installs Python dependencies |
| git | Any | Clones the repository |
| curl | Any | Downloads Xray/Sing-box |
| cron (Linux) / launchd (macOS) | Any | Scheduled runs |

**Windows users:** the installer does not run natively on Windows. Use **WSL2** (Windows Subsystem for Linux) and run every command in this guide inside your WSL2 Linux distribution.

---

## 🚀 Automatic Installation with the Wizard

This single command detects your platform and installs everything: Xray-core, Sing-box, Python dependencies, the repository itself, a runner script, a management script, and a scheduled task (cron / Termux service / launchd, depending on your platform).

```bash
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

### What the Wizard does, step by step:
1. Detects your operating system (Termux, Linux, or macOS)
2. Installs system dependencies (git, Python, curl, cron, etc.)
3. Clones (or updates) the repository into `~/multi-proxy-config-fetcher`
4. Creates a Python virtual environment and installs `requirements.txt`
5. Installs Xray-core
6. Installs Sing-box
7. Generates `run.sh` — the script that runs the full pipeline
8. Generates `manage.sh` — the script you'll use day to day
9. Sets up automatic scheduling for your platform (see [Scheduling](#-scheduling))

### After installation, run the pipeline once manually:
```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```

---

## 🔧 Manual Installation

If you'd rather not run the one-liner, here is exactly what it does under the hood.

### Step 1: Clone the repository
```bash
git clone https://github.com/4n0nymou3/multi-proxy-config-fetcher.git
cd multi-proxy-config-fetcher
```

### Step 2: Install Python dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Install Xray-core

**Linux/macOS:**
```bash
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
```

**Termux:** download the correct build for your CPU architecture directly from the [Xray-core releases page](https://github.com/XTLS/Xray-core/releases) and place the `xray` binary somewhere on your `$PATH` (e.g. `$PREFIX/bin`).

### Step 4: Install Sing-box

**Linux:**
```bash
bash <(curl -fsSL https://sing-box.app/install.sh)
```

**macOS:**
```bash
brew install sing-box
```

**Termux:**
```bash
pkg install sing-box -y
```

---

## ▶️ Running the Project

### Pipeline steps (in exact order):
```
1.  Fetch Configs                    Fetch from all configured sources
2.  Enrich Configs                   Detect server locations
3.  Rename Configs                   Apply descriptive tags
4.  Test with Xray                   Health test - multi-round, Xray core
5.  Convert to Sing-box               Build the Sing-box JSON format
6.  Test with Sing-box                Health test - multi-round, Sing-box core
7.  Security Filter                  Remove insecure configs, rebuild secure outputs
8.  Generate Clash YAML               Build Clash/Mihomo configs
9.  Generate Xray Balanced Config     Build the load-balanced Xray config
10. Generate Xray Fragment Config     Build the Fragment (anti-DPI) Xray config
11. Generate Charts                  Build the performance charts
12. Generate Pipeline Summary         Print a config count for every stage
```

### Run once:
```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```

Each run also writes a timestamped log file under `logs/run_<date>.log`, and logs older than 7 days are cleaned up automatically.

---

## 📁 Output Files

| File | Description | Compatible Apps |
|------|-------------|----------------|
| `proxy_configs.txt` | Raw configs | v2rayNG, v2rayN |
| `proxy_configs_tested.txt` | Xray-tested | v2rayNG, v2rayN ⭐ |
| `singbox_configs_all.json` | All configs, Sing-box format | SFA, Hiddify, NekoBox |
| `singbox_configs_tested.json` | Sing-box tested | SFA, Hiddify, NekoBox ⭐ |
| `singbox_configs_secure.json` | Tested & security-filtered | SFA, Hiddify 🛡️⭐ |
| `clash_configs_all.yaml` | All configs, Clash format | Clash Verge, Mihomo |
| `clash_configs_tested.yaml` | Clash tested | Clash Verge, Mihomo ⭐ |
| `clash_configs_secure.yaml` | Tested & security-filtered | Clash Verge, Mihomo 🛡️⭐ |
| `xray_loadbalanced_config.json` | Xray load balancer | v2rayNG, v2rayN, Nekoray ⭐ |
| `xray_fragment_loadbalanced_config.json` | Xray load balancer with advanced two-stage TLS fragmentation for stronger DPI resistance | v2rayNG, v2rayN, Nekoray 🧩⭐ |
| `xray_secure_loadbalanced_config.json` | Secure load balancer | v2rayNG, v2rayN, Nekoray 🛡️⭐ |

⭐ = Recommended · 🛡️ = High security · 🧩 = Anti-censorship fragmentation

---

## 📱 Using the Configs

### 🐱 Using in Clash / Mihomo (Android, iOS, Windows, macOS, Linux)

**Method 1: Import from local file**
```bash
# Termux
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/clash_configs_secure.yaml ~/storage/downloads/
```
In Clash Verge or Mihomo: **Profiles → Import → Select file → `clash_configs_secure.yaml` → Import**

**Method 2: Serve over HTTP (access from any device on your network)**
```bash
cd ~/multi-proxy-config-fetcher/configs
python3 -m http.server 8080
```
Clash subscription link:
```
http://YOUR_IP:8080/clash_configs_tested.yaml
```

---

### 📦 Using in Sing-box Apps (SFA, Hiddify, NekoBox)

**Method 1: Import from local file**
```bash
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/singbox_configs_secure.json ~/storage/downloads/
```
In Sing-box For Android (SFA): **Profiles → New Profile → Import → `singbox_configs_secure.json` → Import**

**Method 2: Serve over HTTP**
```bash
cd ~/multi-proxy-config-fetcher/configs
python3 -m http.server 8080
```
Sing-box subscription link:
```
http://YOUR_IP:8080/singbox_configs_tested.json
```

---

### 🚀 Using in v2rayNG / v2rayN / Nekoray

**Method 1: Subscription link**
```bash
cd ~/multi-proxy-config-fetcher/configs
python3 -m http.server 8080
```
Subscription URL:
```
http://YOUR_IP:8080/proxy_configs_tested.txt
```
In v2rayNG: **Subscription → Add Subscription → Enter URL → Update**

**Method 2: Direct JSON import**
```bash
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json ~/storage/downloads/
```
Want stronger DPI resistance instead? Copy `xray_fragment_loadbalanced_config.json` the same way.

---

## 🛠️ Management Script

After installation, `manage.sh` is your main day-to-day tool:

```bash
bash ~/multi-proxy-config-fetcher/manage.sh start            # Run the pipeline manually
bash ~/multi-proxy-config-fetcher/manage.sh status           # Show Xray/Sing-box versions, service status, output files, recent logs
bash ~/multi-proxy-config-fetcher/manage.sh logs             # Show the most recent log
bash ~/multi-proxy-config-fetcher/manage.sh clean            # Delete logs older than 7 days
bash ~/multi-proxy-config-fetcher/manage.sh update           # Pull the latest code from GitHub
bash ~/multi-proxy-config-fetcher/manage.sh restart-service  # Termux only: restart the background service
bash ~/multi-proxy-config-fetcher/manage.sh help             # Show this command list
```

**Sample `status` output:**
```
📊 System Status:

✓ Xray: Xray 26.7.28
✓ Sing-box: sing-box version 1.13.0

🔄 Service Status:
run: multiproxy: (pid 4821) 3600s

📁 Output files:
    configs/proxy_configs.txt - 62K
    configs/singbox_configs_secure.json - 178K

📝 Recent logs:
    logs/run_2026-08-27_06-00-01.log
```

---

## ⏰ Scheduling

The Wizard sets up automatic runs for you, but the mechanism differs per platform:

| Platform | Mechanism | Interval |
|----------|-----------|----------|
| Termux (Android) | Background service (`sv`), started at boot | Every 12 hours |
| Linux | `cron` | Every 12 hours (`0 */12 * * *`) |
| macOS | `launchd` (LaunchAgent) | Twice daily, at 08:00 and 20:00 (system local time) |

### ⚠️ Termux — critical extra step

A Termux background service does **not** survive a phone reboot by itself. To keep automatic runs working after restarting your phone, you must:
1. Install **Termux:Boot** from F-Droid (not the Play Store)
2. Open the Termux:Boot app **once** so Android registers it
3. Go to **Android Settings → Apps → Termux → Battery → Unrestricted**, so Android doesn't kill the background service

Without these three steps, the service stops working after every reboot and you'll need to run `bash run.sh` manually again.

### Changing the interval

**Linux (cron):**
```bash
crontab -e
```
Edit the line added by the installer, for example to run every 6 hours instead:
```
0 */6 * * * /bin/bash ~/multi-proxy-config-fetcher/run.sh >> ~/multi-proxy-config-fetcher/logs/cron.log 2>&1
```

**Termux:** edit `INTERVAL=43200` (seconds) inside `$PREFIX/var/service/multiproxy/run`, then run `bash manage.sh restart-service`.

**macOS:** edit the `StartCalendarInterval` block inside `~/Library/LaunchAgents/com.anonymous.multiproxy.plist`, then run:
```bash
launchctl unload ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
launchctl load ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
```

---

## 🎛️ Customizing Sources and Settings

Edit `settings/user_settings.py` to control what the fetcher does:

```python
SOURCE_URLS = [
    "https://t.me/s/your_channel",
    "https://raw.githubusercontent.com/user/repo/main/configs.txt",
]

USE_MAXIMUM_POWER = True   # Fetch as many configs as possible
ENABLED_PROTOCOLS = {
    "vless://": True,
    "vmess://": True,
    "trojan://": True,
    "ss://": True,
    "hysteria2://": True,
    "wireguard://": False,
    "tuic://": False,
}
```

After editing, just run `bash run.sh` again (or wait for the next scheduled run) to apply the changes.

---

## 🧩 Customizing the Fragment Endpoint

`xray_fragment_loadbalanced_config.json` applies an advanced, two-stage TLS ClientHello fragmentation to every config, which can help against DPI-based filtering. All of its parameters live in `settings/fragment_settings.py`:

```python
FRAGMENT_ENABLED = True
FRAGMENT_STAGE_1 = {"packets": "tlshello", "lengths": ["5", "94", "1"], "delays": ["0"], "max_split": "0"}
FRAGMENT_STAGE_2_ENABLED = True
FRAGMENT_STAGE_2 = {"packets": "1-1", "lengths": ["109", "1"], "delays": ["1"], "max_split": "355"}
FRAGMENT_TLS_FINGERPRINT = "unsafe"
FRAGMENT_TLS_CIPHER_SUITES = "TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:..."
```

Change the values here and run `bash run.sh` again to regenerate the file with your own fragmentation settings.

---

## 🔒 Security Notes

**Prefer these files:**
- ✅ `xray_secure_loadbalanced_config.json`
- ✅ `singbox_configs_secure.json`
- ✅ `clash_configs_secure.yaml`

**Avoid using these directly** (they include untested or unfiltered configs):
- ❌ `proxy_configs.txt`
- ❌ `singbox_configs_all.json`
- ❌ `clash_configs_all.yaml`

### What the security filter removes:
- Shadowsocks configs using non-AEAD (insecure) ciphers
- VMess configs with a deprecated, non-zero `alterId`
- VLESS/Trojan configs without TLS
- Configs with `insecure=true` (certificate validation disabled)
- VMess configs with `security=none`

---

## 🔧 Troubleshooting

### Xray not found
```bash
which xray
```
**Fix:**
```bash
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
```

### Sing-box not found
```bash
which sing-box
```
**Fix (Termux):**
```bash
pkg install sing-box -y
```
**Fix (Linux):**
```bash
bash <(curl -fsSL https://sing-box.app/install.sh)
```

### Python errors
```bash
source ~/multi-proxy-config-fetcher/venv/bin/activate
pip install -r ~/multi-proxy-config-fetcher/requirements.txt --upgrade
```

### No output files / pipeline seems to have failed partway
```bash
ls -la ~/multi-proxy-config-fetcher/configs/
tail -100 ~/multi-proxy-config-fetcher/logs/run_*.log
```
The last log file will show exactly which step failed.

### Scheduled runs aren't happening
```bash
# Linux
crontab -l
systemctl status cron

# Termux
sv status multiproxy
```

---

## ❓ FAQ

**Q: Which config file should I actually use?**
Anything with a `_tested` or `_secure` suffix has passed the health tests. For the highest confidence, use the `_secure` files, or `xray_fragment_loadbalanced_config.json` if you specifically need stronger anti-filtering resistance.

**Q: How often are configs updated?**
Every 12 hours by default on Linux/Termux, or twice daily (08:00/20:00) on macOS. See [Scheduling](#-scheduling) to change this.

**Q: How many configs does the system fetch?**
Depends on `USE_MAXIMUM_POWER` in `settings/user_settings.py`. With `True`, it fetches the maximum available from your configured sources.

**Q: Can I add my own sources?**
Yes — add them to `SOURCE_URLS` in `settings/user_settings.py` (see [Customizing Sources and Settings](#-customizing-sources-and-settings)).

**Q: Does this work on older Android phones?**
Yes, it's been tested on Android 7+. You need Termux installed from **F-Droid**, not the Google Play Store (the Play Store build is outdated and unsupported by the Termux project itself).

**Q: What's the difference between the Xray, Sing-box, and Clash outputs?**
- **Xray** files work with v2rayNG, v2rayN, Nekoray
- **Sing-box** files work with SFA, Hiddify, NekoBox
- **Clash/Mihomo** files work with Clash Verge, Mihomo, Clash Meta

All three are generated from the same underlying proxy list and are functionally equivalent — pick whichever matches your client app.

**Q: What does the Fragment output actually do differently?**
It applies the same load-balanced Xray config as `xray_loadbalanced_config.json`, but splits the TLS handshake into small, delayed pieces across two stages. This can make the connection harder to fingerprint for DPI systems that block based on TLS ClientHello patterns.

---

## 🔄 Updating

```bash
cd ~/multi-proxy-config-fetcher
bash manage.sh update
```

Or manually:
```bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

---

## 🤝 Contributing

Contributions are welcome:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 🙏 Acknowledgments

- **Xray-core Team** — high-performance proxy engine
- **Sing-box Team** — universal proxy engine
- **Clash/Mihomo Team** — modern proxy platform
- **Open Source Community** — support and feedback

---

## 📚 Resources

- **Main Repository**: https://github.com/4n0nymou3/multi-proxy-config-fetcher
- **Config Web Page**: https://4n0nymou3.github.io/Anonymous-Proxy-Hub/
- **Xray-core**: https://github.com/XTLS/Xray-core
- **Sing-box**: https://sing-box.sagernet.org
- **Clash/Mihomo**: https://github.com/MetaCubeX/mihomo
- **v2rayNG**: https://github.com/2dust/v2rayNG
- **Termux**: https://termux.dev
- **Crontab Guru** (test cron syntax): https://crontab.guru

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 📬 Contact

- **GitHub**: https://github.com/4n0nymou3
- **Twitter/X**: https://x.com/4n0nymou3

---

## ⚡ Quick Start for Termux

For new users who want to get started immediately:

```bash
pkg update && pkg upgrade -y
pkg install curl git -y
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
cd ~/multi-proxy-config-fetcher
bash run.sh
termux-setup-storage
cp configs/xray_secure_loadbalanced_config.json ~/storage/downloads/
cp configs/clash_configs_secure.yaml ~/storage/downloads/
```

Then don't forget the three critical Termux:Boot steps in [Scheduling](#-scheduling) so automatic runs survive a phone reboot.

---

> 🎉 **Congratulations!** Your proxy config fetcher is set up and running. For any issues, check the logs with `bash manage.sh logs`.