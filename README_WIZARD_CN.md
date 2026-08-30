# ⚙️ Anonymous Wizard — 中文安装指南

<p align="center">
  <img src="https://img.shields.io/badge/Anonymous-Wizard-blue?style=for-the-badge" />
</p>

在本地系统上安装、运行和管理 **Multi Proxy Config Fetcher** 项目的完整分步指南 —— 支持 Termux（Android）、Linux、macOS、iSH（iOS）以及通过 WSL2 的 Windows。

---

## 📋 目录

- [先决条件](#-先决条件)
- [使用 Wizard 自动安装](#-使用-wizard-自动安装)
- [手动安装](#-手动安装)
- [运行项目](#️-运行项目)
- [输出文件](#-输出文件)
- [使用配置](#-使用配置)
- [管理脚本](#️-管理脚本)
- [自动运行的时间表](#-自动运行的时间表)
- [自定义来源与设置](#-自定义来源与设置)
- [自定义 Fragment 端点](#-自定义-fragment-端点)
- [安全说明](#-安全说明)
- [故障排查](#-故障排查)
- [常见问题](#-常见问题)
- [更新](#-更新)
- [Termux 快速开始](#-termux-快速开始)

---

## 📦 先决条件

Wizard 会自动安装以下所有内容。如果你想手动安装，需要确保拥有：

| 工具 | 版本 | 用途 |
|------|------|------|
| Python | 3.9+ | 运行流水线 |
| pip | 最新版 | 安装 Python 依赖 |
| git | 任意版本 | 克隆仓库 |
| curl | 任意版本 | 下载 Xray/Sing-box |
| cron（Linux）/ launchd（macOS） | 任意版本 | 定时运行 |

**Windows 用户：** 安装脚本无法在 Windows 上原生运行。请使用 **WSL2**（Windows 子系统 Linux），并在 WSL2 的 Linux 发行版内执行本指南中的所有命令。

---

## 🚀 使用 Wizard 自动安装

只需一条命令即可自动检测你的平台，并安装好一切：Xray-core、Sing-box、Python 依赖、项目仓库本身、运行脚本、管理脚本，以及根据你的平台设置的定时任务（cron / Termux 服务 / launchd）。

```bash
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

### Wizard 依次执行的步骤：
1. 检测你的操作系统（Termux、Linux 或 macOS）
2. 安装系统依赖（git、Python、curl、cron 等）
3. 克隆（或更新）仓库到 `~/multi-proxy-config-fetcher`
4. 创建 Python 虚拟环境并安装 `requirements.txt`
5. 安装 Xray-core
6. 安装 Sing-box
7. 生成 `run.sh` —— 用于运行完整流水线的脚本
8. 生成 `manage.sh` —— 你日常会用到的管理脚本
9. 为你的平台设置自动定时运行（见 [自动运行的时间表](#-自动运行的时间表)）

### 安装完成后，先手动运行一次流水线：
```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```

---

## 🔧 手动安装

如果你不想运行一键命令，以下是它在幕后所做的具体操作。

### 步骤 1：克隆仓库
```bash
git clone https://github.com/4n0nymou3/multi-proxy-config-fetcher.git
cd multi-proxy-config-fetcher
```

### 步骤 2：安装 Python 依赖
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 步骤 3：安装 Xray-core

**Linux/macOS：**
```bash
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
```

**Termux：** 请直接从 [Xray-core 发布页面](https://github.com/XTLS/Xray-core/releases) 下载与你的 CPU 架构匹配的版本，并将 `xray` 可执行文件放到 `$PATH` 内的某个目录（例如 `$PREFIX/bin`）。

### 步骤 4：安装 Sing-box

**Linux：**
```bash
bash <(curl -fsSL https://sing-box.app/install.sh)
```

**macOS：**
```bash
brew install sing-box
```

**Termux：**
```bash
pkg install sing-box -y
```

---

## ▶️ 运行项目

### 流水线步骤（精确顺序）：
```
1.  Fetch Configs                    从所有已配置的来源抓取
2.  Enrich Configs                   检测服务器地理位置
3.  Rename Configs                   应用描述性标签
4.  Test with Xray                   多轮健康测试 - Xray core
5.  Convert to Sing-box              构建 Sing-box JSON 格式
6.  Test with Sing-box               多轮健康测试 - Sing-box core
7.  Security Filter                  移除不安全配置，重建安全版输出
8.  Generate Clash YAML              构建 Clash/Mihomo 配置
9.  Generate Xray Balanced Config     构建负载均衡的 Xray 配置
10. Generate Xray Fragment Config     构建带 Fragment（抗 DPI）的 Xray 配置
11. Generate Charts                  构建性能图表
12. Generate Pipeline Summary         打印每个阶段的配置数量
```

### 运行一次：
```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```

每次运行都会在 `logs/run_<日期>.log` 下写入带时间戳的日志文件，且超过 7 天的旧日志会被自动清理。

---

## 📁 输出文件

| 文件 | 说明 | 兼容应用 |
|------|------|----------|
| `proxy_configs.txt` | 原始配置 | v2rayNG, v2rayN |
| `proxy_configs_tested.txt` | Xray 测试通过 | v2rayNG, v2rayN ⭐ |
| `singbox_configs_all.json` | 所有配置，Sing-box 格式 | SFA, Hiddify, NekoBox |
| `singbox_configs_tested.json` | Sing-box 测试通过 | SFA, Hiddify, NekoBox ⭐ |
| `singbox_configs_secure.json` | 已测试且安全过滤 | SFA, Hiddify 🛡️⭐ |
| `clash_configs_all.yaml` | 所有配置，Clash 格式 | Clash Verge, Mihomo |
| `clash_configs_tested.yaml` | Clash 测试通过 | Clash Verge, Mihomo ⭐ |
| `clash_configs_secure.yaml` | 已测试且安全过滤 | Clash Verge, Mihomo 🛡️⭐ |
| `xray_loadbalanced_config.json` | Xray 负载均衡 | v2rayNG, v2rayN, Nekoray ⭐ |
| `xray_fragment_loadbalanced_config.json` | 带两阶段高级 TLS 分片的 Xray 负载均衡配置，抗 DPI 能力更强 | v2rayNG, v2rayN, Nekoray 🧩⭐ |
| `xray_secure_loadbalanced_config.json` | 安全版 Xray 负载均衡 | v2rayNG, v2rayN, Nekoray 🛡️⭐ |

⭐ = 推荐 · 🛡️ = 高安全性 · 🧩 = 抗审查分片

---

## 📱 使用配置

### 🐱 在 Clash / Mihomo 中使用（Android、iOS、Windows、macOS、Linux）

**方法一：从本地文件导入**
```bash
# Termux
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/clash_configs_secure.yaml ~/storage/downloads/
```
在 Clash Verge 或 Mihomo 中：**Profiles → Import → 选择文件 → `clash_configs_secure.yaml` → Import**

**方法二：通过 HTTP 提供（供局域网内任意设备访问）**
```bash
cd ~/multi-proxy-config-fetcher/configs
python3 -m http.server 8080
```
Clash 订阅链接：
```
http://YOUR_IP:8080/clash_configs_tested.yaml
```

---

### 📦 在 Sing-box 类应用中使用（SFA、Hiddify、NekoBox）

**方法一：从本地文件导入**
```bash
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/singbox_configs_secure.json ~/storage/downloads/
```
在 Sing-box For Android (SFA) 中：**Profiles → New Profile → Import → `singbox_configs_secure.json` → Import**

**方法二：通过 HTTP 提供**
```bash
cd ~/multi-proxy-config-fetcher/configs
python3 -m http.server 8080
```
Sing-box 订阅链接：
```
http://YOUR_IP:8080/singbox_configs_tested.json
```

---

### 🚀 在 v2rayNG / v2rayN / Nekoray 中使用

**方法一：订阅链接**
```bash
cd ~/multi-proxy-config-fetcher/configs
python3 -m http.server 8080
```
订阅 URL：
```
http://YOUR_IP:8080/proxy_configs_tested.txt
```
在 v2rayNG 中：**Subscription → Add Subscription → 输入 URL → Update**

**方法二：直接导入 JSON**
```bash
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json ~/storage/downloads/
```
如果需要更强的抗过滤能力，可以用同样的方式复制 `xray_fragment_loadbalanced_config.json`。

---

## 🛠️ 管理脚本

安装完成后，`manage.sh` 是你日常使用的主要工具：

```bash
bash ~/multi-proxy-config-fetcher/manage.sh start            # 手动运行流水线
bash ~/multi-proxy-config-fetcher/manage.sh status           # 显示 Xray/Sing-box 版本、服务状态、输出文件、最近日志
bash ~/multi-proxy-config-fetcher/manage.sh logs             # 显示最近的日志
bash ~/multi-proxy-config-fetcher/manage.sh clean            # 删除超过 7 天的旧日志
bash ~/multi-proxy-config-fetcher/manage.sh update           # 从 GitHub 拉取最新代码
bash ~/multi-proxy-config-fetcher/manage.sh restart-service  # 仅 Termux：重启后台服务
bash ~/multi-proxy-config-fetcher/manage.sh help             # 显示此命令列表
```

**`status` 示例输出：**
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

## ⏰ 自动运行的时间表

Wizard 会为你设置自动运行，但不同平台的机制不同：

| 平台 | 机制 | 间隔 |
|------|------|------|
| Termux（Android） | 后台服务（`sv`），开机自动启动 | 每 12 小时 |
| Linux | `cron` | 每 12 小时（`0 */12 * * *`） |
| macOS | `launchd`（LaunchAgent） | 每天两次，08:00 和 20:00（系统本地时间） |

### ⚠️ Termux —— 一个关键的额外步骤

Termux 后台服务**不会**在手机重启后自动存活。要让自动运行在重启手机后依然有效，你必须：
1. 从 F-Droid（而不是 Google Play）安装 **Termux:Boot**
2. **打开一次** Termux:Boot 应用，让 Android 注册它
3. 前往 **Android 设置 → 应用 → Termux → 电池 → 无限制**，防止 Android 杀死后台服务

如果不完成这三步，服务会在每次重启后停止工作，你需要再次手动运行 `bash run.sh`。

### 修改运行间隔

**Linux（cron）：**
```bash
crontab -e
```
编辑安装脚本添加的这一行，例如改为每 6 小时运行一次：
```
0 */6 * * * /bin/bash ~/multi-proxy-config-fetcher/run.sh >> ~/multi-proxy-config-fetcher/logs/cron.log 2>&1
```

**Termux：** 编辑 `$PREFIX/var/service/multiproxy/run` 文件中的 `INTERVAL=43200`（单位：秒），然后运行 `bash manage.sh restart-service`。

**macOS：** 编辑 `~/Library/LaunchAgents/com.anonymous.multiproxy.plist` 中的 `StartCalendarInterval` 部分，然后执行：
```bash
launchctl unload ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
launchctl load ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
```

---

## 🎛️ 自定义来源与设置

编辑 `settings/user_settings.py` 来控制抓取器的行为：

```python
SOURCE_URLS = [
    "https://t.me/s/your_channel",
    "https://raw.githubusercontent.com/user/repo/main/configs.txt",
]

USE_MAXIMUM_POWER = True   # 尽可能多地抓取配置
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

编辑完成后，只需再次运行 `bash run.sh`（或等待下一次定时运行）即可应用更改。

---

## 🧩 自定义 Fragment 端点

`xray_fragment_loadbalanced_config.json` 会对每个配置应用一种高级的两阶段 TLS ClientHello 分片机制，有助于对抗基于 DPI 的过滤。它的所有参数都保存在 `settings/fragment_settings.py` 中：

```python
FRAGMENT_ENABLED = True
FRAGMENT_STAGE_1 = {"packets": "tlshello", "lengths": ["5", "94", "1"], "delays": ["0"], "max_split": "0"}
FRAGMENT_STAGE_2_ENABLED = True
FRAGMENT_STAGE_2 = {"packets": "1-1", "lengths": ["109", "1"], "delays": ["1"], "max_split": "355"}
FRAGMENT_TLS_FINGERPRINT = "unsafe"
FRAGMENT_TLS_CIPHER_SUITES = "TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:..."
```

在这里修改数值，然后重新运行 `bash run.sh`，即可用你自己的分片设置重新生成该文件。

---

## 🔒 安全说明

**优先使用这些文件：**
- ✅ `xray_secure_loadbalanced_config.json`
- ✅ `singbox_configs_secure.json`
- ✅ `clash_configs_secure.yaml`

**避免直接使用这些文件**（包含未测试或未过滤的配置）：
- ❌ `proxy_configs.txt`
- ❌ `singbox_configs_all.json`
- ❌ `clash_configs_all.yaml`

### 安全过滤器会移除：
- 使用非 AEAD（不安全）加密方式的 Shadowsocks 配置
- 使用已弃用、非零 `alterId` 的 VMess 配置
- 没有 TLS 的 VLESS/Trojan 配置
- `insecure=true`（禁用证书验证）的配置
- `security=none` 的 VMess 配置

---

## 🔧 故障排查

### 找不到 Xray
```bash
which xray
```
**修复：**
```bash
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
```

### 找不到 Sing-box
```bash
which sing-box
```
**修复（Termux）：**
```bash
pkg install sing-box -y
```
**修复（Linux）：**
```bash
bash <(curl -fsSL https://sing-box.app/install.sh)
```

### Python 报错
```bash
source ~/multi-proxy-config-fetcher/venv/bin/activate
pip install -r ~/multi-proxy-config-fetcher/requirements.txt --upgrade
```

### 没有输出文件 / 流水线似乎中途失败
```bash
ls -la ~/multi-proxy-config-fetcher/configs/
tail -100 ~/multi-proxy-config-fetcher/logs/run_*.log
```
最新的日志文件会准确显示哪一步失败了。

### 定时运行没有执行
```bash
# Linux
crontab -l
systemctl status cron

# Termux
sv status multiproxy
```

---

## ❓ 常见问题

**问：我到底应该使用哪个配置文件？**
任何带有 `_tested` 或 `_secure` 后缀的文件都已通过健康测试。为获得最高可信度，请使用 `_secure` 文件；如果你特别需要更强的抗过滤能力，请使用 `xray_fragment_loadbalanced_config.json`。

**问：配置多久更新一次？**
Linux/Termux 默认每 12 小时更新一次，macOS 上为每天两次（08:00/20:00）。修改方式见 [自动运行的时间表](#-自动运行的时间表)。

**问：系统会抓取多少配置？**
取决于 `settings/user_settings.py` 中的 `USE_MAXIMUM_POWER`。设为 `True` 时，会从你配置的来源中尽可能多地抓取。

**问：我可以添加自己的来源吗？**
可以 —— 将它们添加到 `settings/user_settings.py` 中的 `SOURCE_URLS`（见 [自定义来源与设置](#-自定义来源与设置)）。

**问：老款 Android 手机能用吗？**
可以，已在 Android 7+ 上测试通过。你需要从 **F-Droid** 安装 Termux，而不是 Google Play（Play 商店版本已过时，且 Termux 团队本身也不再支持它）。

**问：Xray、Sing-box 和 Clash 输出有什么区别？**
- **Xray** 文件适用于 v2rayNG、v2rayN、Nekoray
- **Sing-box** 文件适用于 SFA、Hiddify、NekoBox
- **Clash/Mihomo** 文件适用于 Clash Verge、Mihomo、Clash Meta

三者都基于同一份代理列表生成，功能上是等价的 —— 根据你的客户端应用选择对应格式即可。

**问：Fragment 输出到底有什么不同？**
它构建的是与 `xray_loadbalanced_config.json` 相同的负载均衡 Xray 配置，但会将 TLS 握手拆分成多个小的、带延迟的片段，分两个阶段发送。这可以让基于 TLS ClientHello 特征进行封锁的 DPI 系统更难以识别该连接。

---

## 🔄 更新

```bash
cd ~/multi-proxy-config-fetcher
bash manage.sh update
```

或手动执行：
```bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

---

## 🤝 贡献

欢迎贡献：
1. Fork 本仓库
2. 创建功能分支
3. 进行修改
4. 提交 Pull Request

---

## 🙏 鸣谢

- **Xray-core 团队** —— 高性能代理引擎
- **Sing-box 团队** —— 通用代理引擎
- **Clash/Mihomo 团队** —— 现代代理平台
- **开源社区** —— 支持与反馈

---

## 📚 资源

- **主仓库**: https://github.com/4n0nymou3/multi-proxy-config-fetcher
- **配置网页**: https://4n0nymou3.github.io/Anonymous-Proxy-Hub/
- **Xray-core**: https://github.com/XTLS/Xray-core
- **Sing-box**: https://sing-box.sagernet.org
- **Clash/Mihomo**: https://github.com/MetaCubeX/mihomo
- **v2rayNG**: https://github.com/2dust/v2rayNG
- **Termux**: https://termux.dev
- **Crontab Guru**（测试 cron 语法）: https://crontab.guru

---

## 📄 许可证

MIT 许可证 —— 详见 [LICENSE](LICENSE)。

---

## 📬 联系方式

- **GitHub**: https://github.com/4n0nymou3
- **Twitter/X**: https://x.com/4n0nymou3

---

## ⚡ Termux 快速开始

想要立即开始使用的新用户：

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

之后别忘了完成 [自动运行的时间表](#-自动运行的时间表) 中的三个 Termux:Boot 关键步骤，让自动运行在手机重启后依然有效。

---

> 🎉 **恭喜！** 你的代理配置抓取器已经设置完成并正在运行。如遇到任何问题，请使用 `bash manage.sh logs` 查看日志。