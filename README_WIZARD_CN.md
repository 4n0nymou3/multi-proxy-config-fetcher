# ⚙️ Anonymous Wizard — 中文安装指南

<p align="center">
  <img src="https://img.shields.io/badge/Anonymous-Wizard-blue?style=for-the-badge" />
</p>

在本地系统上安装、运行和管理 **Multi Proxy Config Fetcher** 项目的完整分步指南——支持 Termux（Android）、Linux、macOS、iSH（iOS）和 Windows（WSL2）。

---

## 📋 目录

- [前置条件](#前置条件)
- [使用 Wizard 自动安装](#使用-wizard-自动安装)
- [手动安装](#手动安装)
- [运行项目](#运行项目)
- [输出文件](#输出文件)
- [使用配置](#使用配置)
- [管理工具](#管理工具)
- [安全说明](#安全说明)
- [故障排除](#故障排除)
- [常见问题](#常见问题)
- [更新](#更新)
- [Termux 快速开始](#termux-快速开始)

---

## 📦 前置条件

开始之前，请确保已安装以下工具：

| 工具 | 版本 | 用途 |
|------|------|------|
| Python | 3.9+ | 核心语言 |
| pip | 最新版 | 包管理器 |
| git | 任意版本 | 克隆仓库 |
| curl | 任意版本 | 下载工具 |
| cron | 任意版本 | 定时任务 |

### Termux（Android）:
```bash
pkg update && pkg upgrade -y
pkg install git python curl wget unzip -y
```

### Linux（Ubuntu/Debian）:
```bash
sudo apt update
sudo apt install git python3 python3-pip curl wget unzip cron -y
```

### macOS:
```bash
brew install git python3 curl wget
```

---

## 🚀 使用 Wizard 自动安装

Wizard 通过一条命令自动完成所有安装：

```bash
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

### Wizard 自动完成以下操作：
1. 检测你的操作系统
2. 自动安装 Xray-core
3. 自动安装 Sing-box
4. 安装 Python 依赖
5. 克隆仓库
6. 创建运行脚本
7. 设置管理工具

### 安装完成后：
```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```

---

## 🔧 手动安装

如需手动安装：

### 第一步：克隆仓库
```bash
git clone https://github.com/4n0nymou3/multi-proxy-config-fetcher.git
cd multi-proxy-config-fetcher
```

### 第二步：安装 Python 依赖
```bash
pip install -r requirements.txt
```

### 第三步：安装 Xray-core

**Linux/Termux:**
```bash
bash <(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)
```

### 第四步：安装 Sing-box

**Linux:**
```bash
bash <(curl -fsSL https://sing-box.app/deb-install.sh)
```

**Termux:**
```bash
pkg install sing-box -y
```

---

## ▶️ 运行项目

### 流水线步骤：
```
➤ Fetch Configs              ✓ 从所有来源获取配置
➤ Enrich Configs             ✓ 地理位置识别
➤ Rename Configs             ✓ 用描述性标签重命名
➤ Test with Xray             ✓ 健康测试 - 第一阶段
➤ Convert to Sing-box        ✓ 转换为 Sing-box 格式
➤ Test with Sing-box         ✓ 健康测试 - 第二阶段
➤ Security Filter            ✓ 安全过滤
➤ Generate Clash YAML        ✓ 生成 Clash/Mihomo 配置
➤ Generate Balanced          ✓ 生成 Xray 负载均衡
➤ Generate Charts            ✓ 生成图表
```

### 单次运行：
```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```

### 使用 cron（每 12 小时）：
```bash
crontab -e
```
添加以下行：
```
0 */12 * * * cd ~/multi-proxy-config-fetcher && bash run.sh >> logs/cron.log 2>&1
```

---

## 📁 输出文件

| 文件 | 描述 | 兼容客户端 |
|------|------|-----------|
| `proxy_configs.txt` | 原始配置 | v2rayNG, v2rayN |
| `proxy_configs_tested.txt` | Xray 测试通过 | v2rayNG, v2rayN ⭐ |
| `singbox_configs_all.json` | 全部 Sing-box | SFA, Hiddify, NekoBox |
| `singbox_configs_tested.json` | Sing-box 测试通过 | SFA, Hiddify, NekoBox ⭐ |
| `singbox_configs_secure.json` | 测试通过且安全 | SFA, Hiddify 🛡️⭐ |
| `clash_configs_all.yaml` | 全部 Clash | Clash Verge, Mihomo |
| `clash_configs_tested.yaml` | Clash 测试通过 | Clash Verge, Mihomo ⭐ |
| `clash_configs_secure.yaml` | 测试通过且安全 | Clash Verge, Mihomo 🛡️⭐ |
| `xray_loadbalanced_config.json` | Xray 负载均衡 | v2rayNG, v2rayN ⭐ |
| `xray_secure_loadbalanced_config.json` | 安全负载均衡 | v2rayNG, v2rayN 🛡️⭐ |

⭐ = 推荐使用
🛡️ = 高安全性

---

## 📱 使用配置

---

### 🐱 在 Clash / Mihomo 中使用（Android、iOS、Windows、macOS、Linux）

#### 方式一：从本地文件导入

```bash
# Termux
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/clash_configs_secure.yaml ~/storage/downloads/
```

**在 Clash Verge 或 Mihomo 中：**
1. Profiles → Import → Select file
2. 选择 `clash_configs_secure.yaml`
3. 导入

---

#### 方式二：HTTP 服务器（从网络访问）

```bash
cd ~/multi-proxy-config-fetcher/configs
python -m http.server 8080
```

**Clash 订阅链接：**
```
http://YOUR_IP:8080/clash_configs_tested.yaml
```

---

### 📦 在 Sing-box 客户端中使用

#### 方式一：从本地文件导入

**Termux:**
```bash
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/singbox_configs_secure.json ~/storage/downloads/
```

**在 Sing-box For Android（SFA）中：**
1. Profiles → New Profile → Import
2. 选择 `singbox_configs_secure.json`
3. 导入

---

#### 方式二：HTTP 服务器

```bash
cd ~/multi-proxy-config-fetcher/configs
python -m http.server 8080
```

**Sing-box 订阅链接：**
```
http://YOUR_IP:8080/singbox_configs_tested.json
```

---

### 🚀 在 v2rayNG / v2rayN 中使用

#### 方式一：订阅链接

```bash
cd ~/multi-proxy-config-fetcher/configs
python -m http.server 8080
```

**订阅链接：**
```
http://YOUR_IP:8080/proxy_configs_tested.txt
```

在 v2rayNG 中：
1. 订阅 → 添加订阅
2. 输入链接
3. 更新

---

#### 方式二：直接导入 JSON（Xray）

```bash
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json ~/storage/downloads/
```

---

## 🛠️ 管理工具

### manage.sh

安装完成后，`manage.sh` 工具即可使用：

```bash
bash ~/multi-proxy-config-fetcher/manage.sh status     # 查看状态
bash ~/multi-proxy-config-fetcher/manage.sh run        # 运行流水线
bash ~/multi-proxy-config-fetcher/manage.sh update     # 更新代码
bash ~/multi-proxy-config-fetcher/manage.sh logs       # 查看日志
bash ~/multi-proxy-config-fetcher/manage.sh cron       # 管理 cron
bash ~/multi-proxy-config-fetcher/manage.sh clean      # 清理旧文件
```

**示例输出：**
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

### 设置 cron（每 12 小时自动运行）

```bash
bash ~/multi-proxy-config-fetcher/manage.sh cron
```

或手动设置：
```bash
crontab -e
```
添加：
```
0 */12 * * * cd ~/multi-proxy-config-fetcher && bash run.sh >> logs/cron.log 2>&1
```

---

## 🔒 安全说明

**请始终使用 secure 文件：**
- ✅ `xray_secure_loadbalanced_config.json`
- ✅ `singbox_configs_secure.json`
- ✅ `clash_configs_secure.yaml`

**请勿使用以下文件：**
- ❌ `proxy_configs.txt`（未测试）
- ❌ `singbox_configs_all.json`（未测试）
- ❌ `clash_configs_all.yaml`（未测试）

### 安全过滤器的作用：
- 删除 TLS 无效的配置
- 删除过时或不安全的加密算法
- 删除已弃用的协议
- 为安全节点创建单独的文件

---

## 🔧 故障排除

### 找不到 Xray：
```bash
which xray || ls ~/.local/share/xray/xray 2>/dev/null || ls /usr/local/bin/xray 2>/dev/null
```

**解决方案——重新安装：**
```bash
bash <(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)
```

### 找不到 Sing-box：
```bash
which sing-box || ls ~/go/bin/sing-box 2>/dev/null
```

**解决方案——重新安装（Termux）：**
```bash
pkg install sing-box -y
```

### Python 错误：
```bash
pip install -r requirements.txt --upgrade
```

### 没有输出文件：
```bash
ls -la configs/
cat logs/run_*.log | tail -50
```

### Cron 未运行：
```bash
crontab -l
service cron status
```

---

## ❓ 常见问题

**Q：如何知道哪个配置文件可用？**
带有 `_tested` 或 `_secure` 后缀的文件已经过测试：
- `proxy_configs_tested.txt` ✅
- `singbox_configs_tested.json` ✅
- `singbox_configs_secure.json` ✅（最安全）
- `clash_configs_tested.yaml` ✅
- `clash_configs_secure.yaml` ✅（最安全）
- `xray_secure_loadbalanced_config.json` ✅（最安全）

---

**Q：配置多久更新一次？**
使用 cron 时，每 12 小时自动更新。可在 crontab 中修改此间隔。

---

**Q：系统获取多少配置？**
取决于 `src/user_settings.py` 中的 `USE_MAXIMUM_POWER`。设为 `True` 时获取最大可用数量。

---

**Q：可以添加自定义来源吗？**
可以，在 `src/user_settings.py` 的 `SOURCE_URLS` 中添加：
```python
SOURCE_URLS = [
    "https://t.me/s/your_channel",
    "https://raw.githubusercontent.com/user/repo/main/configs.txt",
]
```

---

**Q：在旧款 Android 手机上可以使用吗？**
可以。已在 Android 7+ 上测试。需要从 F-Droid（而非 Google Play）安装 Termux。

---

**Q：Sing-box、Clash 和 Xray 配置有什么区别？**
- **Xray** — 兼容 v2rayNG、v2rayN、Nekoray
- **Sing-box** — 兼容 SFA、Hiddify、NekoBox
- **Clash/Mihomo** — 兼容 Clash Verge、Mihomo、Clash Meta

三者均从相同的代理列表生成，功能等效。

---

## 🔄 更新

```bash
cd ~/multi-proxy-config-fetcher
bash manage.sh update
```

或手动更新：
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

## 🤝 贡献

欢迎所有贡献：
1. Fork 仓库
2. 创建功能分支
3. 进行修改
4. 提交 Pull Request

---

## 🙏 致谢

### 贡献者：
- **Xray-core Team** — 高性能代理引擎
- **Sing-box Team** — 通用代理引擎
- **Clash/Mihomo Team** — 现代代理平台
- **开源社区** — 支持与反馈

---

## 📚 资源

- **主仓库**: https://github.com/4n0nymou3/multi-proxy-config-fetcher
- **配置网页**: https://4n0nymou3.github.io/Anonymous-Proxy-Hub/
- **Xray-core**: https://github.com/XTLS/Xray-core
- **Sing-box**: https://sing-box.sagernet.org
- **Clash/Mihomo**: https://github.com/MetaCubeX/mihomo
- **v2rayNG**: https://github.com/2dust/v2rayNG
- **Termux**: https://termux.dev
- **Crontab Guru**（测试 cron 格式）: https://crontab.guru

---

## 📄 许可证

MIT 许可证——详见 [LICENSE](LICENSE) 文件。

---

## 📬 联系方式

- **GitHub**: https://github.com/4n0nymou3
- **Twitter**: https://x.com/4n0nymou3

---

## ⚡ Termux 快速开始

适合想立即开始的新用户：

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

> 🎉 **恭喜！** 你的代理配置获取器已设置完成并开始运行。配置将每 12 小时自动更新。如遇到问题，请使用 `bash manage.sh logs` 查看日志。
