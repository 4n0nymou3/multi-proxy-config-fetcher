[![Stars](https://img.shields.io/github/stars/4n0nymou3/multi-proxy-config-fetcher?style=flat-square)](https://github.com/4n0nymou3/multi-proxy-config-fetcher/stargazers)
[![Forks](https://img.shields.io/github/forks/4n0nymou3/multi-proxy-config-fetcher?style=flat-square)](https://github.com/4n0nymou3/multi-proxy-config-fetcher/network/members)
[![Issues](https://img.shields.io/github/issues/4n0nymou3/multi-proxy-config-fetcher?style=flat-square)](https://github.com/4n0nymou3/multi-proxy-config-fetcher/issues)
[![License](https://img.shields.io/github/license/4n0nymou3/multi-proxy-config-fetcher?style=flat-square)](https://github.com/4n0nymou3/multi-proxy-config-fetcher/blob/main/LICENSE)
[![Activity](https://img.shields.io/github/last-commit/4n0nymou3/multi-proxy-config-fetcher?style=flat-square)](https://github.com/4n0nymou3/multi-proxy-config-fetcher/commits)

<div dir="rtl">

# Multi Proxy Config Fetcher

[**🇺🇸English**](README.md) | [**![Lang_farsi](https://user-images.githubusercontent.com/125398461/234186932-52f1fa82-52c6-417f-8b37-08fe9250a55f.png)فارسی**](README_FA.md) | [**🇨🇳中文**](README_CN.md) | [**🇷🇺Русский**](README_RU.md)

یک سیستم پیشرفته و خودکار برای مدیریت پیکربندی‌های پراکسی که از منابع مختلف جمع‌آوری، اعتبارسنجی، آزمایش، غنی‌سازی و فیلتر می‌کند. این پروژه مدیریت پراکسی در سطح سازمانی با نظارت سلامت بلادرنگ، برچسب‌گذاری جغرافیایی و فیلتر امنیتی چندمرحله‌ای ارائه می‌دهد.

## 🌐 دسترسی به پیکربندی‌ها

تمام پیکربندی‌ها و نقاط دسترسی از طریق رابط وبِ یکپارچه ما در دسترس هستند:

### **[👉 Anonymous Proxy Hub - دسترسی به همه نقاط](https://4n0nymou3.github.io/Anonymous-Proxy-Hub/)**

رابط وب شامل:
- **۷ نقطه دسترسی متفاوت** برای استفاده‌های مختلف
- **پیکربندی‌های خام** — پیکربندی‌های اصلی بدون فیلتر
- **آزمایش‌شده با Xray** — پیکربندی‌هایی که با Xray بررسی شده‌اند (مرحله ۱)
- **Xray بارگذاری‌شده متعادل** — پیکربندی‌های JSON با تعادل بار هوشمند
- **Xray امن** — پیکربندی‌های فیلترشده با امنیت بالا
- **همه در Sing-box** — همه پیکربندی‌ها در فرمت Sing-box
- **تست‌شده با Sing-box** — پیکربندی‌های تأییدشده توسط Sing-box (مرحله ۲)
- **Sing-box امن** — پیکربندی‌های Sing-box با بالاترین سطح امنیت
- **Clash همه** — همه پیکربندی‌ها در فرمت Clash/Mihomo
- **Clash تست‌شده** — پیکربندی‌های تست‌شده سازگار با Clash
- **Clash امن** — پیکربندی‌های Clash با بالاترین سطح امنیت

## 📊 مانیتورینگ عملکرد منابع

آمار عملکرد بلادرنگ برای همه منابع پیکربندی‌شده (کانال‌های تلگرام و URLها). این نمودار هر ۱۲ ساعت به‌صورت خودکار به‌روز می‌شود.

### نمای سریع
<div align="center">
  <a href="assets/channel_stats_chart.svg">
    <img src="assets/channel_stats_chart.svg" alt="آمار عملکرد منابع" width="800">
  </a>
</div>

### تحلیل‌های دقیق
📊 [مشاهده داشبورد تعاملی کامل](https://htmlpreview.github.io/?https://github.com/4n0nymou3/multi-proxy-config-fetcher/blob/main/assets/performance_report.html)

> **مهم برای مخازن فورک‌شده**:  
> اگر این مخزن را فورک می‌کنید، در لینک داشبورد بالا نام `4n0nymou3` را با نام کاربری گیت‌هاب خود جایگزین کنید تا داشبورد مخصوص شما نمایش داده شود.

هر منبع بر اساس چهار شاخص کلیدی امتیازدهی می‌شود:
- **امتیاز قابلیت اطمینان (۳۵%)**: نرخ موفقیت در دریافت و به‌روزرسانی پیکربندی‌ها
- **کیفیت پیکربندی (۲۵%)**: نسبت پیکربندی‌های معتبر به کل دریافت‌شده
- **منحصربه‌فرد بودن پیکربندی (۲۵%)**: درصد پیکربندی‌های یکتا
- **زمان پاسخ (۱۵%)**: زمان پاسخ و دسترسی سرور

منابعی که امتیاز زیر ۳۰٪ دارند به‌صورت خودکار غیرفعال می‌شوند تا کیفیت سیستم حفظ شود.

## ✨ ویژگی‌های کلیدی

### پشتیبانی چندپروتکلی
- **WireGuard** — پروتکل VPN مدرن و سریع
- **Hysteria2** — پروتکل پراکسی با عملکرد بالا
- **VLESS** — جایگزین سبک برای VMess
- **VMess** — پروتکل محبوب V2Ray
- **Shadowsocks** — پراکسی امن SOCKS5
- **Trojan** — پروتکل پراکسی مبتنی بر TLS
- **TUIC** — پروتکل پراکسی مبتنی بر UDP

### خط لوله پردازش پیشرفته

1. **جذب هوشمند**
   - پشتیبانی از کانال‌های تلگرام، لینک‌های SSCONF و URLهای دلخواه
   - رمزگشایی خودکار base64 و تشخیص فرمت
   - حذف تکراری‌ها و اعتبارسنجی

2. **سیستم آزمایش دو مرحله‌ای**
   - **مرحله ۱**: بررسی سلامت با Xray core
   - **مرحله ۲**: بررسی سلامت با Sing-box core
   - تست موازی با کارگران قابل پیکربندی
   - تایم‌اوت و آدرس تست قابل تنظیم

3. **افزایش اطلاعات جغرافیایی**
   - تشخیص خودکار محل سرور
   - برچسب‌گذاری با ایموجی پرچم کشور
   - پشتیبانی از چند API موقعیت‌یابی
   - سیستم پشتیبان هوشمند

4. **تغییر نام هوشمند**
   - برچسب‌های توصیفی با جزئیات پروتکل
   - تشخیص نوع ترنسپورت (WS, GRPC, HTTP2 و غیره)
   - تشخیص ویژگی‌های امنیتی (TLS, Reality, XTLS, Vision)
   - اطلاعات پورت و کشور

5. **فیلتر امنیتی**
   - حذف روش‌های رمزنگاری ناامن
   - اعتبارسنجی تنظیمات TLS/SSL
   - فیلتر کردن پروتکل‌های منسوخ
   - ایجاد فایل‌های جداگانه برای نقاط امن

6. **تبدیل فرمت**
   - تبدیل خودکار به فرمت JSON برای Sing-box
   - تولید پیکربندی‌های متعادل‌شده Xray
   - تولید فایل YAML برای Clash/Mihomo
   - حفظ سازگاری با هر سه هسته

## 🚀 شروع سریع

### برای کاربران (توصیه‌شده)

1. به **[Anonymous Proxy Hub](https://4n0nymou3.github.io/Anonymous-Proxy-Hub/)** مراجعه کنید
2. نقطه دسترسی مورد نظر را انتخاب کنید
3. URL را کپی کرده و در کلاینت پراکسی خود استفاده کنید

### برای توسعه‌دهندگان

#### فورک و سفارشی‌سازی

1. این مخزن را فورک کنید
2. فایل `src/user_settings.py` را ویرایش کنید تا:
   - URLهای منابع (کانال‌های تلگرام، لینک‌های SSCONF و غیره) را تنظیم کنید
   - پروتکل‌های فعال را مشخص کنید
   - پارامترهای تست را تعیین کنید
   - ترجیحات API موقعیت‌یابی را تنظیم کنید
3. GitHub Actions را در مخزن فورک‌شده فعال کنید
4. پیکربندی‌ها هر ۱۲ ساعت به‌صورت خودکار به‌روز خواهند شد

#### راه‌اندازی محلی

**Anonymous Wizard** یک راهنمای گام‌به‌گام کامل برای نصب، اجرا و مدیریت این پروژه در سیستم محلی شماست — شامل Termux (اندروید)، لینوکس، macOS، iSH (iOS) و ویندوز (WSL2). زبان مورد نظر خود را انتخاب کنید:

| زبان | راهنما |
|------|--------|
| فارسی | [Anonymous Wizard — راهنمای فارسی](README_WIZARD_FA.md) |
| انگلیسی | [Anonymous Wizard — English Guide](README_WIZARD_EN.md) |
| چینی | [Anonymous Wizard — 中文指南](README_WIZARD_CN.md) |
| روسی | [Anonymous Wizard — Руководство на русском](README_WIZARD_RU.md) |

## ⚙️ گزینه‌های پیکربندی

### `src/user_settings.py`

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
SINGBOX_TESTER_URLS = ['https://www.youtube.com/generate_204']

# Xray Testing
ENABLE_XRAY_TESTER = True
XRAY_TESTER_MAX_WORKERS = 8
XRAY_TESTER_TIMEOUT_SECONDS = 10
XRAY_TESTER_URLS = ['https://www.youtube.com/generate_204']

# Geolocation APIs (in priority order)
LOCATION_APIS = [
    'api.iplocation.net',
    'freeipapi.com',
    'ip-api.com',
    'ipapi.co'
]
```

## 📁 فایل‌های خروجی

سیستم چندین فایل خروجی برای استفاده‌های مختلف تولید می‌کند:

- `configs/proxy_configs.txt` - پیکربندی‌های خام دریافت‌شده
- `configs/proxy_configs_tested.txt` - پیکربندی‌های آزمایش‌شده با Xray
- `configs/singbox_configs_all.json` - همه پیکربندی‌ها در فرمت Sing-box
- `configs/singbox_configs_tested.json` - پیکربندی‌های تست‌شده Sing-box
- `configs/singbox_configs_secure.json` - پیکربندی‌های Sing-box فیلترشده از نظر امنیت
- `configs/clash_configs_all.yaml` - همه پیکربندی‌ها در فرمت Clash/Mihomo
- `configs/clash_configs_tested.yaml` - پیکربندی‌های تست‌شده سازگار با Clash
- `configs/clash_configs_secure.yaml` - پیکربندی‌های Clash فیلترشده از نظر امنیت
- `configs/xray_loadbalanced_config.json` - پیکربندی متعادل‌شده Xray
- `configs/xray_secure_loadbalanced_config.json` - پیکربندی متعادل‌شده Xray ایمن
- `configs/location_cache.json` - داده‌های کش شده موقعیت جغرافیایی
- `configs/channel_stats.json` - معیارهای عملکرد منابع

## 🔄 اتوماسیون

این پروژه از GitHub Actions برای به‌روزرسانی خودکار استفاده می‌کند:

- اجرای دو بار در روز (۰۸:۰۰ و ۲۰:۰۰ UTC)
- قابل فراخوانی دستی از طریق workflow_dispatch
- خودکار commit و push تغییرات پیکربندی
- تولید گزارش‌ها و نمودارهای عملکرد

### جریان کاری GitHub Actions

روند کار به‌ترتیب موارد زیر را انجام می‌دهد:
1. دریافت پیکربندی‌ها از همه منابع
2. غنی‌سازی با داده‌های مکانی
3. تغییر نام با برچسب‌های توصیفی
4. تست با Xray core (مرحله ۱)
5. تبدیل به فرمت Sing-box
6. تست با Sing-box core (مرحله ۲)
7. فیلتر امنیتی
8. تولید فایل‌های YAML برای Clash/Mihomo
9. تولید پیکربندی‌های متعادل‌شده
10. به‌روزرسانی نمودارها و گزارش‌ها
11. commit و push تغییرات

## 🛡️ ویژگی‌های امنیتی

### فیلترینگ امنیتی خودکار

سیستم به‌طور خودکار موارد زیر را حذف می‌کند:
- **شِیفرهای ناامن Shadowsocks** (روش‌های غیر-AEAD)
- **VMess با احراز هویت MD5** (alter_id منسوخ)
- **پروتکل‌های بدون رمزنگاری** (VLESS/Trojan بدون TLS)
- **تنظیمات TLS نامعتبر** (insecure=true)
- **VMess با security=none**

### نقاط امن

فایل‌های نقطه دسترسی امن تنها پیکربندی‌هایی را شامل می‌شوند که استانداردهای امنیتی مدرن را رعایت کنند:
- گواهی‌های TLS/SSL معتبر
- الگوریتم‌های رمزنگاری مدرن
- بدون روش‌های احراز هویت منسوخ
- اعتبارسنجی صحیح گواهی‌ها

## 📈 بهینه‌سازی عملکرد

- **پردازش موازی** برای تسریع تست پیکربندی‌ها
- **کش هوشمند** برای داده‌های مکانی
- **استفاده از connection pooling** برای درخواست‌های HTTP
- **قابلیت تنظیم تایم‌اوت** برای تعادل سرعت و اطمینان
- **منطق retry هوشمند** با backoff نمایی
- **پاکسازی منابع** برای جلوگیری از نشت حافظه

## 🌍 سیستم موقعیت‌یابی جغرافیایی

### پشتیبانی از چند API

سیستم از چند API رایگان موقعیت‌یابی با مکانیزم fallback خودکار پشتیبانی می‌کند:

1. **api.iplocation.net** — نامحدود، سریع و دقیق
2. **freeipapi.com** — ۶۰ درخواست در دقیقه، بسیار سریع
3. **ip-api.com** — ۴۵ درخواست در دقیقه، قابل اعتماد
4. **ipapi.co** — ۱۰۰۰ درخواست در روز

### تشخیص هوشمند

- تشخیص الگوی URL به‌صورت خودکار
- کش مؤثر برای کاهش درخواست‌ها به API
- افت تدریجی مسئولانه در صورت خرابی APIها
- نیاز به کلید API ندارد

## 📊 آمار و پایش

### معیارهای بلادرنگ

سیستم معیارهای جامعی برای هر منبع ثبت می‌کند:
- مجموع پیکربندی‌های دریافت‌شده
- نسبت معتبر به نامعتبر
- سهم پیکربندی‌های یکتا
- میانگین زمان پاسخ
- نرخ‌های موفقیت/خطا
- امتیاز کلی سلامت

### داشبوردهای تصویری

- **نمودار SVG** — نمای سریع عملکرد
- **گزارش HTML تعاملی** — تحلیل‌های دقیق با:
  - منابع فعال/غیرفعال
  - توزیع پروتکل‌ها
  - تحلیل زمان پاسخ
  - روندهای تاریخی

## 🤝 مشارکت

مشارکت‌ها خوش‌آمد است! این‌جا می‌توانید کمک کنید:

1. **گزارش باگ** — باگی دیدید؟ Issue باز کنید
2. **پیشنهاد ویژگی** — ایده‌ای دارید؟ بحث را شروع کنید
3. **ارسال PR** — بهبودها همیشه خوش‌آمدند
4. **افزودن منابع** — منابع خوب پراکسی می‌شناسید؟ اضافه کنید
5. **بهبود مستندات** — به بهتر شدن داک‌ها کمک کنید

## ⚠️ تبرئه مسئولیت

این پروژه صرفاً برای **آموزشی و اطلاع‌رسانی** ارائه شده است. توسعه‌دهندگان مسئولیتی در قبال:
- هرگونه سوءاستفاده از این نرم‌افزار
- هرگونه خسارت یا زیان واردشده
- کیفیت یا امنیت پیکربندی‌های شخص ثالث
- نقض قوانین یا مقررات محلی

**مسئولیت‌های کاربران:**
- رعایت قوانین محلی
- بررسی امنیت پیکربندی‌ها
- آگاهی از ریسک‌های استفاده از پراکسی
- احترام به شرایط سرویس ارائه‌دهندگان پراکسی

## 📜 مجوز

این پروژه تحت مجوز MIT منتشر شده است — جزئیات در فایل [LICENSE](LICENSE).

## 👤 درباره توسعه‌دهنده

ساخته‌شده با ❤️ توسط **4n0nymou3**

- 🐙 GitHub: [@4n0nymou3](https://github.com/4n0nymou3)
- 🐦 Twitter/X: [@4n0nymou3](https://x.com/4n0nymou3)
- 📦 Repository: [multi-proxy-config-fetcher](https://github.com/4n0nymou3/multi-proxy-config-fetcher)

## 🙏 قدردانی

- **Xray-core** — سکوی پراکسی با عملکرد بالا
- **Sing-box** — سکوی پراکسی جامع
- **Clash/Mihomo** — سکوی پراکسی مدرن
- **GitHub Actions** — زیرساخت اتوماسیون

---

<div align="center">

**[⬆ بازگشت به بالا](#-دسترسی-به-پیکربندی‌ها)**

Made with 💚 by Anonymous

</div>
</div>