[![Stars](https://img.shields.io/github/stars/4n0nymou3/multi-proxy-config-fetcher?style=flat-square)](https://github.com/4n0nymou3/multi-proxy-config-fetcher/stargazers)
[![Forks](https://img.shields.io/github/forks/4n0nymou3/multi-proxy-config-fetcher?style=flat-square)](https://github.com/4n0nymou3/multi-proxy-config-fetcher/network/members)
[![Issues](https://img.shields.io/github/issues/4n0nymou3/multi-proxy-config-fetcher?style=flat-square)](https://github.com/4n0nymou3/multi-proxy-config-fetcher/issues)
[![License](https://img.shields.io/github/license/4n0nymou3/multi-proxy-config-fetcher?style=flat-square)](https://github.com/4n0nymou3/multi-proxy-config-fetcher/blob/main/LICENSE)
[![Activity](https://img.shields.io/github/last-commit/4n0nymou3/multi-proxy-config-fetcher?style=flat-square)](https://github.com/4n0nymou3/multi-proxy-config-fetcher/commits)

<div dir="ltr">

# Multi Proxy Config Fetcher

[**🇺🇸English**](README.md) | [**<img src="https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/refs/heads/main/flag/iran.svg" height="14" style="vertical-align:middle">فارسی**](README_FA.md) | [**🇨🇳中文**](README_CN.md) | [**🇷🇺Русский**](README_RU.md)

一个高级的自动化代理配置管理系统，从多个来源抓取、验证、测试、丰富和过滤代理配置。该项目提供企业级的代理管理功能，包括实时健康监控、地理标记、多轮连接测试和多阶段安全过滤。

## 🌐 访问配置

所有代理配置和端点可通过我们的统一 Web 界面获取：

### **[👉 Anonymous Proxy Hub - 访问所有端点](https://4n0nymou3.github.io/Anonymous-Proxy-Hub/)**

Web 界面提供：
- **11 个不同的端点** 以满足不同使用场景
- **原始配置** — 未过滤的原始配置
- **Xray 测试** — 使用 Xray core 验证的配置
- **Xray 负载均衡** — 智能负载均衡的 JSON 配置
- **Xray Fragment 负载均衡** — 在负载均衡 JSON 配置基础上加入了两阶段高级 TLS 分片，以增强抗 DPI 检测能力
- **Xray 安全** — 高安全性过滤配置
- **Sing-box 全部** — 以 Sing-box 格式提供的所有配置
- **Sing-box 测试** — 使用 Sing-box 验证的配置
- **Sing-box 安全** — 最高安全级别的 Sing-box 配置
- **Clash 全部** — 以 Clash/Mihomo 格式提供的所有配置
- **Clash 测试** — 使用 Clash 验证的测试配置
- **Clash 安全** — 最高安全级别的 Clash 配置

## 📊 源性能监控

对所有已配置来源（Telegram 频道和 URL）进行实时性能统计。该图表在每次运行后自动更新。

### 快速概览
<div align="center">
  <a href="assets/channel_stats_chart.svg">
    <img src="assets/channel_stats_chart.svg" alt="源性能统计" width="800">
  </a>
</div>

### 详细分析
📊 [查看完整交互式仪表板](https://htmlpreview.github.io/?https://github.com/4n0nymou3/multi-proxy-config-fetcher/blob/main/assets/performance_report.html)

> **对于 Fork 的仓库的重要提示**：  
> 如果你 fork 了此仓库，请在上面的仪表板链接中将 `4n0nymou3` 替换为你的 GitHub 用户名，以访问你自己的分析仪表板。

每个来源根据四个关键指标评分：
- **可靠性得分 (35%)**：抓取与更新配置的成功率
- **配置质量 (25%)**：有效配置与抓取总数的比例
- **配置独特性 (25%)**：贡献的唯一配置百分比
- **响应时间 (15%)**：服务器响应时间与可用性

得分低于 30% 的来源会被自动禁用，以维持系统质量。

## ✨ 主要特性

### 多协议支持
- **VLESS** — 轻量级的 VMess 替代方案，完整支持 Reality 与 XTLS Vision
- **VMess** — 流行的 V2Ray 协议
- **Trojan** — 基于 TLS 的代理协议
- **Shadowsocks** — 安全的 SOCKS5 代理（仅 AEAD 加密方式）
- **Hysteria2** — 高性能代理协议
- **WireGuard** — 现代且快速的 VPN 协议（目前仅包含在原始/测试文本输出中；默认禁用，尚未加入 Sing-box、Xray 负载均衡或 Clash 转换）
- **TUIC** — 基于 UDP 的代理协议（与上面 WireGuard 相同的当前限制；默认禁用）

### 高级处理流水线

1. **智能抓取**
   - 支持 Telegram 频道、SSCONF 链接和自定义 URL
   - 自动 base64 解码与格式检测
   - 语义级去重（按协议、地址、端口和凭据匹配，忽略名称或参数顺序）与校验
   - 仅对临时性错误（超时、连接问题、HTTP 408/429/5xx）重试失败的来源；永久性错误会快速失败

2. **多轮双核心测试系统**
   - 同时使用 Xray core 与 Sing-box core 进行健康检查
   - 每个 core 会进行多轮独立测试（默认 2 轮）——只有每一轮都通过的配置才会被保留，从而过滤掉不稳定的配置
   - 测试 URL 会在各轮之间轮换，避免配置只依据单一目标被判定
   - 每次运行前会自动预检测试 URL，当时不可用的端点会被跳过
   - 支持并行测试，worker 数量、超时时间和测试 URL 均可配置

3. **地理信息增强**
   - 自动检测服务器位置
   - 使用国家旗帜表情进行标记
   - 支持多个地理定位 API
   - 智能回退机制

4. **智能重命名**
   - 带协议细节的描述性标签
   - 传输类型识别（WS、GRPC、HTTP2 等）
   - 安全特性检测（TLS、Reality、XTLS、Vision）
   - 端口与国家信息

5. **安全过滤**
   - 移除不安全的加密方法
   - 验证 TLS/SSL 配置
   - 过滤已弃用的协议
   - 为 Xray、Sing-box 和 Clash 分别生成安全端点文件

6. **格式转换**
   - 自动转换为 Sing-box JSON 格式
   - 生成 Xray 负载均衡配置，包含带有两阶段高级 TLS 分片的版本
   - 生成 Clash/Mihomo YAML 配置
   - 每种输出格式均完整支持 Reality 与 XTLS Vision

## 🚀 快速开始

### 对于用户（推荐）

1. 访问 **[Anonymous Proxy Hub](https://4n0nymou3.github.io/Anonymous-Proxy-Hub/)**  
2. 选择你偏好的端点  
3. 复制 URL 并在你的代理客户端中使用

### 对于开发者

#### Fork 与定制

1. Fork 本仓库  
2. 编辑 `settings/user_settings.py` 配置：
   - 源 URL（Telegram 频道、SSCONF 链接等）
   - 启用的协议
   - 测试参数
   - 地理定位 API 优先级
3. 如需自定义 Fragment 端点使用的高级 TLS 分片，可编辑 `settings/fragment_settings.py`
4. 在你的 fork 中启用 GitHub Actions  
5. 配置将按照项目的计划自动更新

#### 本地部署

**Anonymous Wizard** 是在本地系统上安装、运行和管理本项目的完整分步指南——支持 Termux（Android）、Linux、macOS、iSH（iOS）和 Windows（WSL2）。请选择您的首选语言：

| 语言 | 指南 |
|------|------|
| 波斯语 | [Anonymous Wizard — راهنمای فارسی](README_WIZARD_FA.md) |
| 英语 | [Anonymous Wizard — English Guide](README_WIZARD_EN.md) |
| 中文 | [Anonymous Wizard — 中文指南](README_WIZARD_CN.md) |
| 俄语 | [Anonymous Wizard — Руководство на русском](README_WIZARD_RU.md) |

## ⚙️ 配置选项

### `settings/user_settings.py`

```python
# Source URLs
SOURCE_URLS = [
    "https://t.me/s/your_channel",
    "https://raw.githubusercontent.com/user/repo/main/configs.txt",
    # Add your sources here
]

# Power Mode
USE_MAXIMUM_POWER = True  # Fetch maximum configs
SPECIFIC_CONFIG_COUNT = 50  # Used if USE_MAXIMUM_POWER is False

# Protocol Filtering
ENABLED_PROTOCOLS = {
    "wireguard://": False,
    "hysteria2://": True,
    "vless://": True,
    "vmess://": True,
    "ss://": True,
    "trojan://": True,
    "tuic://": False,
}

# Config Age Filtering
MAX_CONFIG_AGE_DAYS = 1

# Sing-box Testing
ENABLE_SINGBOX_TESTER = True
SINGBOX_TESTER_MAX_WORKERS = 8
SINGBOX_TESTER_TIMEOUT_SECONDS = 10
SINGBOX_TESTER_URLS = [
    'https://www.youtube.com/generate_204',
    'https://www.gstatic.com/generate_204',
    'https://cp.cloudflare.com'
]
SINGBOX_TESTER_ROUNDS = 2

# Xray Testing
ENABLE_XRAY_TESTER = True
XRAY_TESTER_MAX_WORKERS = 8
XRAY_TESTER_TIMEOUT_SECONDS = 10
XRAY_TESTER_URLS = [
    'https://www.youtube.com/generate_204',
    'https://www.gstatic.com/generate_204',
    'https://cp.cloudflare.com'
]
XRAY_TESTER_ROUNDS = 2

# Geolocation APIs (in priority order)
LOCATION_APIS = [
    'api.iplocation.net',
    'freeipapi.com',
    'ip-api.com',
    'ipapi.co'
]
```

关闭任意一个测试器（`ENABLE_SINGBOX_TESTER = False` 或 `ENABLE_XRAY_TESTER = False`）会使该次运行完全跳过对应阶段的连接检测——上一阶段的文件会被原样复制过去。这样可以加快流水线速度，但请注意，Sing-box、Clash 以及 Xray 安全版这几个输出都依赖 Sing-box 测试阶段，关闭它会降低这些输出的可靠性；而普通的 Xray 与 Xray Fragment 输出不受影响。

### `settings/fragment_settings.py`

```python
FRAGMENT_ENABLED = True

FRAGMENT_STAGE_1 = {
    "packets": "tlshello",
    "lengths": ["5", "94", "1"],
    "delays": ["0"],
    "max_split": "0"
}

FRAGMENT_STAGE_2_ENABLED = True

FRAGMENT_STAGE_2 = {
    "packets": "1-1",
    "lengths": ["109", "1"],
    "delays": ["1"],
    "max_split": "355"
}

FRAGMENT_TLS_FINGERPRINT = "unsafe"
FRAGMENT_TLS_CIPHER_SUITES = "TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:..."
```

该文件控制应用于 `xray_fragment_loadbalanced_config.json` 端点中每个配置的高级两阶段 TLS ClientHello 分片。你可以直接在这里调整各阶段参数、指纹或密码套件，无需修改任何其他文件。

## 📁 输出文件

系统为不同用途生成多个输出文件：

- `configs/proxy_configs.txt` - 原始抓取的配置
- `configs/proxy_configs_tested.txt` - Xray 测试通过的配置
- `configs/singbox_configs_all.json` - 以 Sing-box 格式保存的所有配置
- `configs/singbox_configs_tested.json` - Sing-box 测试通过的配置
- `configs/singbox_configs_secure.json` - 安全过滤后的 Sing-box 配置
- `configs/clash_configs_all.yaml` - 以 Clash/Mihomo 格式保存的所有配置
- `configs/clash_configs_tested.yaml` - Clash 测试通过的配置
- `configs/clash_configs_secure.yaml` - 安全过滤后的 Clash 配置
- `configs/xray_loadbalanced_config.json` - Xray 负载均衡配置
- `configs/xray_fragment_loadbalanced_config.json` - 带高级 TLS 分片的 Xray 负载均衡配置
- `configs/xray_secure_loadbalanced_config.json` - 安全的 Xray 负载均衡配置
- `configs/location_cache.json` - 地理位置缓存数据
- `configs/channel_stats.json` - 源性能指标

## 🔄 自动化

该项目使用 GitHub Actions 进行自动更新：

- 每 3 小时运行一次（每天 8 次）
- 可通过 workflow_dispatch 手动触发
- 自动提交并推送更新的配置
- 生成性能报告、图表以及每次运行的流水线摘要

### GitHub Actions 流程

流程按顺序执行以下步骤：
1. 从所有来源抓取配置
2. 使用地理位置数据进行丰富
3. 以描述性标签重命名
4. 使用 Xray core 测试（多轮）
5. 转换为 Sing-box 格式
6. 使用 Sing-box core 测试（多轮）
7. 进行安全过滤，并生成安全版的 Sing-box 与 Xray 输出
8. 生成 Clash/Mihomo YAML 配置
9. 生成 Xray 负载均衡配置
10. 生成带 Fragment 的 Xray 负载均衡配置
11. 更新图表和报告
12. 生成流水线运行摘要
13. 提交并推送更改

## 🛡️ 安全功能

### 自动安全过滤

系统会自动移除：
- **不安全的 Shadowsocks 加密方式**（非 AEAD）
- **使用 MD5 验证的 VMess**（已弃用的 alter_id）
- **未加密的协议**（VLESS/Trojan 无 TLS）
- **无效的 TLS 配置**（insecure=true）
- **security=none 的 VMess**

### 安全端点

专用的安全端点文件仅包含满足现代安全标准的配置：
- 有效的 TLS/SSL 证书
- 现代加密算法
- 无已弃用的验证方法
- 正确的证书校验

## 📈 性能优化

- **并行处理** 加速配置测试
- **智能缓存** 用于地理数据
- **连接池** 提高 HTTP 请求效率
- **可配置超时** 在速度与稳定性之间平衡
- **智能重试策略**（指数退避），仅针对临时性错误
- **资源清理** 防止内存泄漏

## 🌍 地理定位系统

### 多 API 支持

系统支持多个免费地理定位 API，并具备自动回退机制：

1. **api.iplocation.net** — 无限、快速且准确
2. **freeipapi.com** — 每分钟 60 次请求，非常快速
3. **ip-api.com** — 每分钟 45 次请求，可靠
4. **ipapi.co** — 每日 1000 次请求

### 智能检测

- 自动识别 URL 模式
- 高效缓存以减少 API 调用
- 在 API 失败时优雅降级
- 无需 API 密钥

## 📊 统计与监控

### 实时指标

系统跟踪每个来源的全面指标：
- 抓取的配置总数
- 有效与无效比率
- 唯一配置贡献
- 平均响应时间
- 成功/失败率
- 整体健康得分

### 可视化仪表板

- **SVG 图表** — 快速性能概览
- **交互式 HTML 报告** — 详细分析包括：
  - 活跃/非活跃来源
  - 协议分布
  - 响应时间分析
  - 历史趋势
- **流水线运行摘要** — 在每次 GitHub Actions 运行页面上直接显示各阶段与各输出文件的配置数量

## 🤝 贡献

欢迎贡献！你可以这样帮忙：

1. **报告问题** — 发现 bug？请打开 issue
2. **建议功能** — 有想法？发起讨论
3. **提交 PR** — 欢迎改进
4. **添加来源** — 知道可靠的代理来源？加入它们
5. **改善文档** — 帮助提升文档质量

## ⚠️ 免责声明

本项目仅用于**教育和参考**目的。开发者不对以下情况负责：
- 任何滥用本软件的行为
- 任何由此造成的损失或损害
- 第三方代理配置的质量或安全性
- 违反当地法律或法规的行为

**用户需承担的责任：**
- 遵守当地法律
- 验证配置的安全性
- 了解使用代理服务的风险
- 遵守代理提供者的服务条款

## 📜 许可证

本项目采用 MIT 许可证 — 详情见 [LICENSE](LICENSE)。

## 👤 开发者

由 **4n0nymou3** 用 ❤️ 制作

- 🐙 GitHub: [@4n0nymou3](https://github.com/4n0nymou3)
- 🐦 Twitter/X: [@4n0nymou3](https://x.com/4n0nymou3)
- 📦 仓库: [multi-proxy-config-fetcher](https://github.com/4n0nymou3/multi-proxy-config-fetcher)

## 🙏 鸣谢

- **Xray-core** — 高性能代理平台
- **Sing-box** — 通用代理平台
- **Clash/Mihomo** — 现代代理平台
- **GitHub Actions** — 自动化基础设施

---

<div align="center">

**[⬆ Back to Top](#-access-configurations)**

Made with 💚 by Anonymous

</div>
</div>