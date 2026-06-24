# ⚙️ Anonymous Wizard — English Setup Guide

<p align="center">
  <img src="https://img.shields.io/badge/Anonymous-Wizard-blue?style=for-the-badge" />
</p>

A complete step-by-step guide for installing, running and managing the **Multi Proxy Config Fetcher** project on your local system — including Termux (Android), Linux, macOS, iSH (iOS), and Windows (WSL2).

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Automatic Installation with Wizard](#automatic-installation)
- [Manual Installation](#manual-installation)
- [Running the Project](#running-the-project)
- [Output Files](#output-files)
- [Using the Configs](#using-the-configs)
- [Management](#management)
- [Security Notes](#security-notes)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Updating](#updating)
- [Quick Start for Termux](#quick-start-for-termux)

---

## 📦 Prerequisites

Before starting, make sure you have the following installed:

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.9+ | Core language |
| pip | Latest | Package manager |
| git | Any | Clone repository |
| curl | Any | Download tools |
| cron | Any | Scheduled tasks |

### Termux (Android):
```bash
pkg update && pkg upgrade -y
pkg install git python curl wget unzip -y
```

### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install git python3 python3-pip curl wget unzip cron -y
```

### macOS:
```bash
brew install git python3 curl wget
```

---

## 🚀 Automatic Installation with Wizard

The Wizard automatically installs everything with a single command:

```bash
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

### What the Wizard does:
1. Detects your operating system
2. Installs Xray-core automatically
3. Installs Sing-box automatically
4. Installs Python dependencies
5. Clones the repository
6. Creates run scripts
7. Sets up management tools

### After installation:
```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```

---

## 🔧 Manual Installation

If you prefer to install manually:

### Step 1: Clone repository
```bash
git clone https://github.com/4n0nymou3/multi-proxy-config-fetcher.git
cd multi-proxy-config-fetcher
```

### Step 2: Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install Xray-core

**Linux/Termux:**
```bash
bash <(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)
```

### Step 4: Install Sing-box

**Linux:**
```bash
bash <(curl -fsSL https://sing-box.app/deb-install.sh)
```

**Termux:**
```bash
pkg install sing-box -y
```

---

## ▶️ Running the Project

### Pipeline steps:
```
➤ Fetch Configs              ✓ Fetch from all sources
➤ Enrich Configs             ✓ Geo-location identification
➤ Rename Configs             ✓ Rename with descriptive tags
➤ Test with Xray             ✓ Health test - Pass 1
➤ Convert to Sing-box        ✓ Convert to Sing-box format
➤ Test with Sing-box         ✓ Health test - Pass 2
➤ Security Filter            ✓ Security filtering
➤ Generate Clash YAML        ✓ Build Clash/Mihomo configs
➤ Generate Balanced          ✓ Build Xray load balancer
➤ Generate Charts            ✓ Build charts
```

### Run once:
```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```

### Run with cron (every 12 hours):
```bash
crontab -e
```
Add this line:
```
0 */12 * * * cd ~/multi-proxy-config-fetcher && bash run.sh >> logs/cron.log 2>&1
```

---

## 📁 Output Files

| File | Description | Compatible Apps |
|------|-------------|----------------|
| `proxy_configs.txt` | Raw configs | v2rayNG, v2rayN |
| `proxy_configs_tested.txt` | Xray-tested | v2rayNG, v2rayN ⭐ |
| `singbox_configs_all.json` | All Sing-box | SFA, Hiddify, NekoBox |
| `singbox_configs_tested.json` | Sing-box tested | SFA, Hiddify, NekoBox ⭐ |
| `singbox_configs_secure.json` | Tested & secure | SFA, Hiddify 🛡️⭐ |
| `clash_configs_all.yaml` | All Clash | Clash Verge, Mihomo |
| `clash_configs_tested.yaml` | Clash tested | Clash Verge, Mihomo ⭐ |
| `clash_configs_secure.yaml` | Tested & secure Clash | Clash Verge, Mihomo 🛡️⭐ |
| `xray_loadbalanced_config.json` | Xray load balancer | v2rayNG, v2rayN ⭐ |
| `xray_secure_loadbalanced_config.json` | Secure load balancer | v2rayNG, v2rayN 🛡️⭐ |

⭐ = Recommended
🛡️ = High security

---

## 📱 Using the Configs

---

### 🐱 Using in Clash / Mihomo (Android, iOS, Windows, macOS, Linux)

#### Method 1: Import from local file

```bash
# Termux
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/clash_configs_secure.yaml ~/storage/downloads/
```

**In Clash Verge or Mihomo:**
1. Profiles → Import → Select file
2. Select `clash_configs_secure.yaml`
3. Import

---

#### Method 2: HTTP Server (access from network)

```bash
cd ~/multi-proxy-config-fetcher/configs
python -m http.server 8080
```

**Clash subscription link:**
```
http://YOUR_IP:8080/clash_configs_tested.yaml
```

---

### 📦 Using in Sing-box Apps

#### Method 1: Import from local file

**Termux:**
```bash
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/singbox_configs_secure.json ~/storage/downloads/
```

**In Sing-box For Android (SFA):**
1. Profiles → New Profile → Import
2. Select `singbox_configs_secure.json`
3. Import

---

#### Method 2: HTTP Server

```bash
cd ~/multi-proxy-config-fetcher/configs
python -m http.server 8080
```

**Sing-box subscription link:**
```
http://YOUR_IP:8080/singbox_configs_tested.json
```

---

### 🚀 Using in v2rayNG / v2rayN

#### Method 1: Subscription link

```bash
cd ~/multi-proxy-config-fetcher/configs
python -m http.server 8080
```

**Subscription URL:**
```
http://YOUR_IP:8080/proxy_configs_tested.txt
```

In v2rayNG:
1. Subscription → Add Subscription
2. Enter URL
3. Update

---

#### Method 2: Direct JSON import (Xray)

```bash
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json ~/storage/downloads/
```

---

## 🛠️ Management

### manage.sh

After installation, the `manage.sh` tool is available:

```bash
bash ~/multi-proxy-config-fetcher/manage.sh status     # Check status
bash ~/multi-proxy-config-fetcher/manage.sh run        # Run pipeline
bash ~/multi-proxy-config-fetcher/manage.sh update     # Update code
bash ~/multi-proxy-config-fetcher/manage.sh logs       # View logs
bash ~/multi-proxy-config-fetcher/manage.sh cron       # Manage cron
bash ~/multi-proxy-config-fetcher/manage.sh clean      # Clean old files
```

**Sample output:**
```
📊 System Status:

✓ Xray: Xray 1.8.9
✓ Sing-box: sing-box version 1.8.0

🔄 Service Status:
✓ Service is running

📁 Output files:
   configs/proxy_configs.txt - 45K
   configs/singbox_configs_secure.json - 156K
   configs/clash_configs_secure.yaml - 148K
```

---

### Setting up cron (auto-run every 12 hours)

```bash
bash ~/multi-proxy-config-fetcher/manage.sh cron
```

Or manually:
```bash
crontab -e
```
Add:
```
0 */12 * * * cd ~/multi-proxy-config-fetcher && bash run.sh >> logs/cron.log 2>&1
```

---

## 🔒 Security Notes

**Always use secure files:**
- ✅ `xray_secure_loadbalanced_config.json`
- ✅ `singbox_configs_secure.json`
- ✅ `clash_configs_secure.yaml`

**Do not use these files:**
- ❌ `proxy_configs.txt` (untested)
- ❌ `singbox_configs_all.json` (untested)
- ❌ `clash_configs_all.yaml` (untested)

### What the security filter does:
- Removes configs with invalid TLS
- Removes outdated/insecure encryption
- Removes deprecated protocols
- Creates separate files for secure endpoints

---

## 🔧 Troubleshooting

### Xray not found:
```bash
which xray || ls ~/.local/share/xray/xray 2>/dev/null || ls /usr/local/bin/xray 2>/dev/null
```

**Solution — reinstall:**
```bash
bash <(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)
```

### Sing-box not found:
```bash
which sing-box || ls ~/go/bin/sing-box 2>/dev/null
```

**Solution — reinstall (Termux):**
```bash
pkg install sing-box -y
```

### Python errors:
```bash
pip install -r requirements.txt --upgrade
```

### No output files:
```bash
ls -la configs/
cat logs/run_*.log | tail -50
```

### Cron not running:
```bash
crontab -l
service cron status
```

---

## ❓ FAQ

**Q: How do I know which config file works?**
Files with `_tested` or `_secure` suffix have been tested:
- `proxy_configs_tested.txt` ✅
- `singbox_configs_tested.json` ✅
- `singbox_configs_secure.json` ✅ (most secure)
- `clash_configs_tested.yaml` ✅
- `clash_configs_secure.yaml` ✅ (most secure)
- `xray_secure_loadbalanced_config.json` ✅ (most secure)

---

**Q: How often are configs updated?**
With cron, every 12 hours automatically. You can change this interval in crontab.

---

**Q: How many configs does the system fetch?**
Depends on `USE_MAXIMUM_POWER` in `src/user_settings.py`. With `True`, the maximum available number is fetched.

---

**Q: Can I add my own sources?**
Yes, add them to `SOURCE_URLS` in `src/user_settings.py`:
```python
SOURCE_URLS = [
    "https://t.me/s/your_channel",
    "https://raw.githubusercontent.com/user/repo/main/configs.txt",
]
```

---

**Q: Does this work on older Android phones?**
Yes. Tested on Android 7+. Requires Termux installed from F-Droid (not Google Play).

---

**Q: What's the difference between Sing-box, Clash and Xray configs?**
- **Xray** — compatible with v2rayNG, v2rayN, Nekoray
- **Sing-box** — compatible with SFA, Hiddify, NekoBox
- **Clash/Mihomo** — compatible with Clash Verge, Mihomo, Clash Meta

All three are generated from the same proxy list and are functionally equivalent.

---

## 🔄 Updating

```bash
cd ~/multi-proxy-config-fetcher
bash manage.sh update
```

Or manually:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

## 🤝 Contributing

We welcome all contributions:
1. Fork the repository
2. Create a feature branch
3. Make changes
4. Submit a pull request

---

## 🙏 Acknowledgments

### Contributors:
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
- **Crontab Guru** (test cron format): https://crontab.guru

---

## 📄 License

MIT License — see [LICENSE](LICENSE) file for details.

---

## 📬 Contact

- **GitHub**: https://github.com/4n0nymou3
- **Twitter**: https://x.com/4n0nymou3

---

## ⚡ Quick Start for Termux

For new users who want to get started immediately:

### Termux:
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

---

> 🎉 **Congratulations!** Your proxy config fetcher is set up and running. Configs will update automatically every 12 hours. For any issues, check the logs with `bash manage.sh logs`.
