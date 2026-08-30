# ⚙️ Anonymous Wizard — راهنمای فارسی نصب

<p align="center">
  <img src="https://img.shields.io/badge/Anonymous-Wizard-blue?style=for-the-badge" />
</p>

راهنمای کامل و گام‌به‌گام برای نصب، اجرا و مدیریت پروژه‌ی **Multi Proxy Config Fetcher** روی سیستم محلی شما — شامل Termux (اندروید)، لینوکس، macOS، iSH (iOS) و ویندوز (از طریق WSL2).

---

## 📋 فهرست مطالب

- [پیش‌نیازها](#-پیش‌نیازها)
- [نصب خودکار با Wizard](#-نصب-خودکار-با-wizard)
- [نصب دستی](#-نصب-دستی)
- [اجرای پروژه](#️-اجرای-پروژه)
- [فایل‌های خروجی](#-فایل‌های-خروجی)
- [استفاده از کانفیگ‌ها](#-استفاده-از-کانفیگ‌ها)
- [اسکریپت مدیریت](#️-اسکریپت-مدیریت)
- [زمان‌بندی اجرای خودکار](#-زمان‌بندی-اجرای-خودکار)
- [سفارشی‌سازی منابع و تنظیمات](#-سفارشی‌سازی-منابع-و-تنظیمات)
- [سفارشی‌سازی خروجی Fragment](#-سفارشی‌سازی-خروجی-fragment)
- [نکات امنیتی](#-نکات-امنیتی)
- [رفع مشکلات رایج](#-رفع-مشکلات-رایج)
- [سوالات متداول](#-سوالات-متداول)
- [به‌روزرسانی](#-به‌روزرسانی)
- [شروع سریع برای Termux](#-شروع-سریع-برای-termux)

---

## 📦 پیش‌نیازها

Wizard همه‌ی موارد زیر را به‌صورت خودکار نصب می‌کند. اگر می‌خواهید دستی نصب کنید، به این‌ها نیاز دارید:

| ابزار | نسخه | کاربرد |
|------|------|--------|
| Python | 3.9 به بالا | اجرای پایپ‌لاین |
| pip | آخرین نسخه | نصب کتابخانه‌های پایتون |
| git | هر نسخه | دریافت مخزن پروژه |
| curl | هر نسخه | دانلود Xray/Sing-box |
| cron (لینوکس) / launchd (macOS) | هر نسخه | اجرای زمان‌بندی‌شده |

**کاربران ویندوز:** نصب‌کننده مستقیماً روی ویندوز اجرا نمی‌شود. از **WSL2** (زیرسیستم لینوکس ویندوز) استفاده کنید و تمام دستورات این راهنما را داخل توزیع لینوکسِ WSL2 اجرا کنید.

---

## 🚀 نصب خودکار با Wizard

این یک دستور، پلتفرم شما را تشخیص می‌دهد و همه‌چیز را نصب می‌کند: Xray-core، Sing-box، کتابخانه‌های پایتون، خودِ مخزن پروژه، یک اسکریپت اجراکننده، یک اسکریپت مدیریتی، و یک وظیفه‌ی زمان‌بندی‌شده (cron / سرویس Termux / launchd، بسته به پلتفرم شما).

```bash
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

### مراحلی که Wizard به‌ترتیب انجام می‌دهد:
1. تشخیص سیستم‌عامل شما (Termux، لینوکس یا macOS)
2. نصب پیش‌نیازهای سیستمی (git، Python، curl، cron و غیره)
3. کلون یا آپدیت مخزن پروژه در مسیر `~/multi-proxy-config-fetcher`
4. ساخت محیط مجازی پایتون و نصب `requirements.txt`
5. نصب Xray-core
6. نصب Sing-box
7. ساخت `run.sh` — اسکریپتی که کل پایپ‌لاین را اجرا می‌کند
8. ساخت `manage.sh` — اسکریپتی که روزانه استفاده می‌کنید
9. تنظیم اجرای خودکار متناسب با پلتفرم شما (بخش [زمان‌بندی](#-زمان‌بندی-اجرای-خودکار) را ببینید)

### بعد از نصب، یک‌بار پایپ‌لاین را دستی اجرا کنید:
```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```

---

## 🔧 نصب دستی

اگر ترجیح می‌دهید دستور یک‌خطی را اجرا نکنید، دقیقاً همان کاری که آن دستور پشت‌صحنه انجام می‌دهد این‌جا آورده شده:

### مرحله ۱: دریافت مخزن
```bash
git clone https://github.com/4n0nymou3/multi-proxy-config-fetcher.git
cd multi-proxy-config-fetcher
```

### مرحله ۲: نصب کتابخانه‌های پایتون
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### مرحله ۳: نصب Xray-core

**لینوکس/macOS:**
```bash
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
```

**Termux:** فایل مناسب معماری پردازنده‌ی خود را مستقیماً از [صفحه‌ی release های Xray-core](https://github.com/XTLS/Xray-core/releases) دانلود کنید و فایل اجرایی `xray` را در مسیری داخل `$PATH` (مثلاً `$PREFIX/bin`) قرار دهید.

### مرحله ۴: نصب Sing-box

**لینوکس:**
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

## ▶️ اجرای پروژه

### مراحل پایپ‌لاین (به‌ترتیب دقیق):
```
۱.  Fetch Configs                    دریافت از همه‌ی منابع پیکربندی‌شده
۲.  Enrich Configs                   تشخیص موقعیت جغرافیایی سرورها
۳.  Rename Configs                   اعمال برچسب‌های توصیفی
۴.  Test with Xray                   تست سلامت چنددوره‌ای با هسته‌ی Xray
۵.  Convert to Sing-box              ساخت فرمت JSON برای Sing-box
۶.  Test with Sing-box               تست سلامت چنددوره‌ای با هسته‌ی Sing-box
۷.  Security Filter                  حذف کانفیگ‌های ناامن و بازسازی خروجی‌های امن
۸.  Generate Clash YAML              ساخت کانفیگ‌های Clash/Mihomo
۹.  Generate Xray Balanced Config     ساخت کانفیگ متعادل‌شده‌ی Xray
۱۰. Generate Xray Fragment Config     ساخت کانفیگ Xray با Fragment (ضدفیلترینگ)
۱۱. Generate Charts                  ساخت نمودارهای عملکرد
۱۲. Generate Pipeline Summary         نمایش تعداد کانفیگ در هر مرحله
```

### اجرای یک‌باره:
```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```

هر اجرا یک فایل لاگ با مهر زمانی در مسیر `logs/run_<تاریخ>.log` می‌سازد، و لاگ‌های قدیمی‌تر از ۷ روز به‌صورت خودکار پاک می‌شوند.

---

## 📁 فایل‌های خروجی

| فایل | توضیح | اپ‌های سازگار |
|------|-------|----------------|
| `proxy_configs.txt` | کانفیگ‌های خام | v2rayNG, v2rayN |
| `proxy_configs_tested.txt` | تست‌شده با Xray | v2rayNG, v2rayN ⭐ |
| `singbox_configs_all.json` | همه کانفیگ‌ها، فرمت Sing-box | SFA, Hiddify, NekoBox |
| `singbox_configs_tested.json` | تست‌شده با Sing-box | SFA, Hiddify, NekoBox ⭐ |
| `singbox_configs_secure.json` | تست‌شده و فیلترشده از نظر امنیت | SFA, Hiddify 🛡️⭐ |
| `clash_configs_all.yaml` | همه کانفیگ‌ها، فرمت Clash | Clash Verge, Mihomo |
| `clash_configs_tested.yaml` | تست‌شده برای Clash | Clash Verge, Mihomo ⭐ |
| `clash_configs_secure.yaml` | تست‌شده و فیلترشده از نظر امنیت | Clash Verge, Mihomo 🛡️⭐ |
| `xray_loadbalanced_config.json` | تعادل بار Xray | v2rayNG, v2rayN, Nekoray ⭐ |
| `xray_fragment_loadbalanced_config.json` | تعادل بار Xray با قطعه‌بندی پیشرفته‌ی دومرحله‌ای TLS برای مقاومت بیشتر در برابر فیلترینگ | v2rayNG, v2rayN, Nekoray 🧩⭐ |
| `xray_secure_loadbalanced_config.json` | تعادل بار امن Xray | v2rayNG, v2rayN, Nekoray 🛡️⭐ |

⭐ = پیشنهادی · 🛡️ = امنیت بالا · 🧩 = قطعه‌بندی ضدفیلترینگ

---

## 📱 استفاده از کانفیگ‌ها

### 🐱 استفاده در Clash / Mihomo (اندروید، iOS، ویندوز، macOS، لینوکس)

**روش ۱: وارد کردن از فایل محلی**
```bash
# Termux
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/clash_configs_secure.yaml ~/storage/downloads/
```
در Clash Verge یا Mihomo: **Profiles ← Import ← انتخاب فایل ← `clash_configs_secure.yaml` ← Import**

**روش ۲: ارائه از طریق HTTP (دسترسی از هر دستگاه در شبکه‌ی شما)**
```bash
cd ~/multi-proxy-config-fetcher/configs
python3 -m http.server 8080
```
لینک اشتراک Clash:
```
http://YOUR_IP:8080/clash_configs_tested.yaml
```

---

### 📦 استفاده در اپ‌های Sing-box (SFA، Hiddify، NekoBox)

**روش ۱: وارد کردن از فایل محلی**
```bash
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/singbox_configs_secure.json ~/storage/downloads/
```
در Sing-box For Android (SFA): **Profiles ← New Profile ← Import ← `singbox_configs_secure.json` ← Import**

**روش ۲: ارائه از طریق HTTP**
```bash
cd ~/multi-proxy-config-fetcher/configs
python3 -m http.server 8080
```
لینک اشتراک Sing-box:
```
http://YOUR_IP:8080/singbox_configs_tested.json
```

---

### 🚀 استفاده در v2rayNG / v2rayN / Nekoray

**روش ۱: لینک اشتراک**
```bash
cd ~/multi-proxy-config-fetcher/configs
python3 -m http.server 8080
```
لینک اشتراک:
```
http://YOUR_IP:8080/proxy_configs_tested.txt
```
در v2rayNG: **Subscription ← Add Subscription ← وارد کردن URL ← Update**

**روش ۲: وارد کردن مستقیم JSON**
```bash
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json ~/storage/downloads/
```
اگر مقاومت بیشتری در برابر فیلترینگ می‌خواهید، `xray_fragment_loadbalanced_config.json` را به همین شکل کپی کنید.

---

## 🛠️ اسکریپت مدیریت

بعد از نصب، `manage.sh` ابزار اصلی روزانه‌ی شماست:

```bash
bash ~/multi-proxy-config-fetcher/manage.sh start            # اجرای دستی پایپ‌لاین
bash ~/multi-proxy-config-fetcher/manage.sh status           # نمایش نسخه‌ی Xray/Sing-box، وضعیت سرویس، فایل‌های خروجی، آخرین لاگ‌ها
bash ~/multi-proxy-config-fetcher/manage.sh logs             # نمایش آخرین لاگ
bash ~/multi-proxy-config-fetcher/manage.sh clean            # حذف لاگ‌های قدیمی‌تر از ۷ روز
bash ~/multi-proxy-config-fetcher/manage.sh update           # دریافت آخرین کد از گیت‌هاب
bash ~/multi-proxy-config-fetcher/manage.sh restart-service  # فقط Termux: راه‌اندازی مجدد سرویس پس‌زمینه
bash ~/multi-proxy-config-fetcher/manage.sh help             # نمایش همین لیست دستورات
```

**نمونه‌ی خروجی `status`:**
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

## ⏰ زمان‌بندی اجرای خودکار

Wizard اجرای خودکار را برای شما تنظیم می‌کند، اما مکانیزم آن بسته به پلتفرم فرق دارد:

| پلتفرم | مکانیزم | فاصله زمانی |
|--------|---------|-------------|
| Termux (اندروید) | سرویس پس‌زمینه (`sv`)، هنگام روشن شدن گوشی اجرا می‌شود | هر ۱۲ ساعت |
| لینوکس | `cron` | هر ۱۲ ساعت (`0 */12 * * *`) |
| macOS | `launchd` (LaunchAgent) | دو بار در روز، ساعت ۰۸:۰۰ و ۲۰:۰۰ (به وقت محلی سیستم) |

### ⚠️ Termux — یک مرحله‌ی حیاتی اضافه

سرویس پس‌زمینه‌ی Termux به‌خودی‌خود **از ری‌استارت گوشی جان سالم به‌در نمی‌برد**. برای این‌که اجرای خودکار بعد از ری‌استارت گوشی هم کار کند، باید:
1. اپ **Termux:Boot** را از F-Droid نصب کنید (نه گوگل‌پلی)
2. اپ Termux:Boot را **یک‌بار** باز کنید تا اندروید آن را ثبت کند
3. به **تنظیمات اندروید ← اپ‌ها ← Termux ← باتری ← بدون محدودیت** بروید تا اندروید سرویس پس‌زمینه را نکشد

بدون این سه مرحله، سرویس بعد از هر ری‌استارت از کار می‌افتد و باید دوباره دستی `bash run.sh` را اجرا کنید.

### تغییر فاصله‌ی زمانی

**لینوکس (cron):**
```bash
crontab -e
```
خطی که نصب‌کننده اضافه کرده را ویرایش کنید، مثلاً برای اجرا هر ۶ ساعت به‌جای ۱۲ ساعت:
```
0 */6 * * * /bin/bash ~/multi-proxy-config-fetcher/run.sh >> ~/multi-proxy-config-fetcher/logs/cron.log 2>&1
```

**Termux:** مقدار `INTERVAL=43200` (بر حسب ثانیه) داخل فایل `$PREFIX/var/service/multiproxy/run` را ویرایش کنید، سپس `bash manage.sh restart-service` را اجرا کنید.

**macOS:** بخش `StartCalendarInterval` داخل `~/Library/LaunchAgents/com.anonymous.multiproxy.plist` را ویرایش کنید، سپس:
```bash
launchctl unload ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
launchctl load ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
```

---

## 🎛️ سفارشی‌سازی منابع و تنظیمات

فایل `settings/user_settings.py` را ویرایش کنید تا رفتار fetcher را کنترل کنید:

```python
SOURCE_URLS = [
    "https://t.me/s/your_channel",
    "https://raw.githubusercontent.com/user/repo/main/configs.txt",
]

USE_MAXIMUM_POWER = True   # دریافت حداکثر تعداد ممکن کانفیگ
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

بعد از ویرایش، کافیست `bash run.sh` را دوباره اجرا کنید (یا منتظر اجرای زمان‌بندی‌شده‌ی بعدی بمانید) تا تغییرات اعمال شوند.

---

## 🧩 سفارشی‌سازی خروجی Fragment

فایل `xray_fragment_loadbalanced_config.json` یک مکانیزم پیشرفته و دومرحله‌ای قطعه‌بندی TLS ClientHello را روی تمام کانفیگ‌ها اعمال می‌کند که می‌تواند در برابر فیلترینگ مبتنی بر DPI کمک‌کننده باشد. تمام پارامترهای آن در فایل `settings/fragment_settings.py` قرار دارند:

```python
FRAGMENT_ENABLED = True
FRAGMENT_STAGE_1 = {"packets": "tlshello", "lengths": ["5", "94", "1"], "delays": ["0"], "max_split": "0"}
FRAGMENT_STAGE_2_ENABLED = True
FRAGMENT_STAGE_2 = {"packets": "1-1", "lengths": ["109", "1"], "delays": ["1"], "max_split": "355"}
FRAGMENT_TLS_FINGERPRINT = "unsafe"
FRAGMENT_TLS_CIPHER_SUITES = "TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:..."
```

مقادیر را اینجا تغییر دهید و `bash run.sh` را دوباره اجرا کنید تا فایل با تنظیمات قطعه‌بندی دلخواه خودتان بازسازی شود.

---

## 🔒 نکات امنیتی

**همیشه این فایل‌ها را ترجیح دهید:**
- ✅ `xray_secure_loadbalanced_config.json`
- ✅ `singbox_configs_secure.json`
- ✅ `clash_configs_secure.yaml`

**از استفاده‌ی مستقیم این فایل‌ها خودداری کنید** (شامل کانفیگ‌های تست‌نشده یا فیلترنشده هستند):
- ❌ `proxy_configs.txt`
- ❌ `singbox_configs_all.json`
- ❌ `clash_configs_all.yaml`

### فیلتر امنیتی چه چیزهایی را حذف می‌کند:
- کانفیگ‌های Shadowsocks با شِیفرهای غیر-AEAD (ناامن)
- کانفیگ‌های VMess با `alterId` منسوخ و غیرصفر
- کانفیگ‌های VLESS/Trojan بدون TLS
- کانفیگ‌هایی با `insecure=true` (بدون اعتبارسنجی گواهی)
- کانفیگ‌های VMess با `security=none`

---

## 🔧 رفع مشکلات رایج

### Xray پیدا نمی‌شود
```bash
which xray
```
**راه‌حل:**
```bash
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
```

### Sing-box پیدا نمی‌شود
```bash
which sing-box
```
**راه‌حل (Termux):**
```bash
pkg install sing-box -y
```
**راه‌حل (لینوکس):**
```bash
bash <(curl -fsSL https://sing-box.app/install.sh)
```

### خطاهای پایتون
```bash
source ~/multi-proxy-config-fetcher/venv/bin/activate
pip install -r ~/multi-proxy-config-fetcher/requirements.txt --upgrade
```

### فایل خروجی ساخته نمی‌شود / پایپ‌لاین انگار نیمه‌کاره متوقف شده
```bash
ls -la ~/multi-proxy-config-fetcher/configs/
tail -100 ~/multi-proxy-config-fetcher/logs/run_*.log
```
آخرین فایل لاگ دقیقاً نشان می‌دهد کدام مرحله شکست خورده.

### اجرای زمان‌بندی‌شده انجام نمی‌شود
```bash
# لینوکس
crontab -l
systemctl status cron

# Termux
sv status multiproxy
```

---

## ❓ سوالات متداول

**س: کدام فایل کانفیگ را واقعاً باید استفاده کنم؟**
هر فایلی که پسوند `_tested` یا `_secure` دارد، از تست سلامت رد شده. برای بالاترین اطمینان، از فایل‌های `_secure` استفاده کنید؛ یا اگر به مقاومت بیشتر در برابر فیلترینگ نیاز دارید، از `xray_fragment_loadbalanced_config.json`.

**س: کانفیگ‌ها هر چند وقت آپدیت می‌شوند؟**
به‌صورت پیش‌فرض هر ۱۲ ساعت روی لینوکس/Termux، یا دو بار در روز (۰۸:۰۰/۲۰:۰۰) روی macOS. برای تغییر آن به بخش [زمان‌بندی](#-زمان‌بندی-اجرای-خودکار) مراجعه کنید.

**س: سیستم چند کانفیگ دریافت می‌کند؟**
بستگی به `USE_MAXIMUM_POWER` در `settings/user_settings.py` دارد. با مقدار `True`، حداکثر تعداد ممکن از منابع پیکربندی‌شده‌ی شما دریافت می‌شود.

**س: می‌توانم منابع خودم را اضافه کنم؟**
بله — آن‌ها را به `SOURCE_URLS` در `settings/user_settings.py` اضافه کنید (بخش [سفارشی‌سازی منابع و تنظیمات](#-سفارشی‌سازی-منابع-و-تنظیمات) را ببینید).

**س: روی گوشی‌های اندروید قدیمی‌تر هم کار می‌کند؟**
بله، روی اندروید ۷ به بالا تست شده. باید Termux را از **F-Droid** نصب کنید، نه از گوگل‌پلی (نسخه‌ی گوگل‌پلی قدیمی و از سوی خود تیم Termux پشتیبانی نمی‌شود).

**س: تفاوت خروجی‌های Xray، Sing-box و Clash چیست؟**
- فایل‌های **Xray** با v2rayNG، v2rayN، Nekoray کار می‌کنند
- فایل‌های **Sing-box** با SFA، Hiddify، NekoBox کار می‌کنند
- فایل‌های **Clash/Mihomo** با Clash Verge، Mihomo، Clash Meta کار می‌کنند

هر سه از یک لیست پراکسی یکسان ساخته می‌شوند و از نظر عملکرد معادل هم هستند — هرکدام که با اپ کلاینت شما سازگار است را انتخاب کنید.

**س: خروجی Fragment دقیقاً چه کار متفاوتی انجام می‌دهد؟**
همان کانفیگ متعادل‌شده‌ی Xray (`xray_loadbalanced_config.json`) را می‌سازد، اما دست‌دهی TLS را به قطعات کوچک و با تأخیر، در دو مرحله می‌شکند. این کار می‌تواند شناسایی اتصال توسط سیستم‌های DPI که بر اساس الگوی TLS ClientHello فیلتر می‌کنند را سخت‌تر کند.

---

## 🔄 به‌روزرسانی

```bash
cd ~/multi-proxy-config-fetcher
bash manage.sh update
```

یا به‌صورت دستی:
```bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

---

## 🤝 مشارکت

مشارکت‌ها خوش‌آمدند:
1. مخزن را فورک کنید
2. یک برنچ جدید بسازید
3. تغییرات خود را اعمال کنید
4. یک Pull Request ارسال کنید

---

## 🙏 قدردانی

- **تیم Xray-core** — موتور پراکسی با عملکرد بالا
- **تیم Sing-box** — موتور پراکسی جامع
- **تیم Clash/Mihomo** — سکوی پراکسی مدرن
- **جامعه‌ی متن‌باز** — پشتیبانی و بازخورد

---

## 📚 منابع

- **مخزن اصلی**: https://github.com/4n0nymou3/multi-proxy-config-fetcher
- **صفحه‌ی وب کانفیگ‌ها**: https://4n0nymou3.github.io/Anonymous-Proxy-Hub/
- **Xray-core**: https://github.com/XTLS/Xray-core
- **Sing-box**: https://sing-box.sagernet.org
- **Clash/Mihomo**: https://github.com/MetaCubeX/mihomo
- **v2rayNG**: https://github.com/2dust/v2rayNG
- **Termux**: https://termux.dev
- **Crontab Guru** (تست فرمت cron): https://crontab.guru

---

## 📄 مجوز

مجوز MIT — جزئیات در فایل [LICENSE](LICENSE).

---

## 📬 ارتباط

- **گیت‌هاب**: https://github.com/4n0nymou3
- **توییتر/X**: https://x.com/4n0nymou3

---

## ⚡ شروع سریع برای Termux

برای کاربران جدیدی که می‌خواهند فوراً شروع کنند:

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

بعد فراموش نکنید سه مرحله‌ی حیاتی Termux:Boot در بخش [زمان‌بندی](#-زمان‌بندی-اجرای-خودکار) را هم انجام دهید تا اجرای خودکار بعد از ری‌استارت گوشی هم کار کند.

---

> 🎉 **تبریک!** ابزار دریافت کانفیگ پراکسی شما نصب شد و در حال اجراست. برای هر مشکلی، با `bash manage.sh logs` لاگ‌ها را بررسی کنید.