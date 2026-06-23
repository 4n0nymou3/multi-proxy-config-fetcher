<div dir="rtl">

# 🧙‍♂️ راهنمای کامل Multi Wizard

**طراحی شده توسط: 👽 Anonymous**

---

## 📋 فهرست مطالب

1. [معرفی](#-معرفی)
2. [پیش‌نیازها](#-پیشنیازها)
3. [نصب](#-نصب)
   - [Linux](#-نصب-در-linux)
   - [macOS](#-نصب-در-macos)
   - [Termux (Android)](#-نصب-در-termux-android)
   - [Windows](#-نصب-در-windows)
4. [اجرای دستی](#-اجرای-دستی)
5. [تنظیم اجرای خودکار](#-تنظیم-اجرای-خودکار)
6. [مدیریت سیستم](#-مدیریت-سیستم)
7. [استفاده از کانفیگ‌ها](#-استفاده-از-کانفیگها)
8. [به‌روزرسانی](#-بهروزرسانی)
9. [عیب‌یابی](#-عیبیابی)
10. [حذف کامل](#-حذف-کامل)

---

## 🎯 معرفی

**Multi Wizard** یک نصب‌کننده خودکار و کامل برای سیستم مدیریت پروکسی است که:

✅ تمام ابزارهای مورد نیاز را نصب می‌کند  
✅ محیط کار را به طور کامل راه‌اندازی می‌کند  
✅ اجرای خودکار هر 12 ساعت را تنظیم می‌کند  
✅ ابزارهای مدیریتی ساده ارائه می‌دهد  

### چه چیزهایی نصب می‌شود؟
- **Git** - برای دریافت کدها
- **Python 3.9+** - زبان برنامه‌نویسی
- **Xray-core** - موتور تست پروکسی (مرحله اول)
- **Sing-box** - موتور تست پروکسی (مرحله دوم)
- **وابستگی‌های Python** - کتابخانه‌های مورد نیاز
- **Cron/LaunchAgent/Service** - برای اجرای خودکار

---

## 📦 پیش‌نیازها

### برای همه پلتفرم‌ها:
- ✅ اتصال به اینترنت (پایدار)
- ✅ حداقل 500MB فضای خالی
- ✅ دسترسی به ترمینال/Terminal

### Termux (Android):
- ✅ نصب [Termux از F-Droid](https://f-droid.org/packages/com.termux/)
- ⚠️ نسخه Google Play پشتیبانی نمی‌شود!
- ✅ توصیه می‌شود: نصب [Termux:Boot](https://f-droid.org/packages/com.termux.boot/)

### Linux:
- ✅ توزیع‌های پشتیبانی شده: Ubuntu, Debian, Arch, Fedora, CentOS
- ✅ دسترسی sudo (برای نصب پکیج‌ها)

### macOS:
- ✅ macOS 10.15+ (Catalina یا جدیدتر)
- ✅ Homebrew (نصب خودکار انجام می‌شود)

### Windows:
- ✅ WSL2 (Windows Subsystem for Linux)
- یا Git Bash

---

## 🚀 نصب

### 🐧 نصب در Linux

#### روش 1: نصب با یک دستور (توصیه می‌شود)
```bash
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

یا:
```bash
wget -qO- https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

#### روش 2: نصب دستی
```bash
sudo apt install git -y
git clone https://github.com/4n0nymou3/multi-proxy-config-fetcher.git
cd multi-proxy-config-fetcher
bash install.sh
```

#### زمان تقریبی نصب:
⏱️ **5-10 دقیقه** (بسته به سرعت اینترنت)

---

### 🍎 نصب در macOS

#### روش 1: نصب با یک دستور
```bash
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

#### روش 2: نصب دستی
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install git
git clone https://github.com/4n0nymou3/multi-proxy-config-fetcher.git
cd multi-proxy-config-fetcher
bash install.sh
```

#### زمان تقریبی نصب:
⏱️ **8-15 دقیقه**

---

### 📱 نصب در Termux (Android)

#### مرحله 1: نصب Termux از F-Droid
1. دانلود [F-Droid](https://f-droid.org/)
2. نصب **Termux** از F-Droid
3. باز کردن Termux

⚠️ **هشدار**: نسخه Google Play کار نمی‌کند!

#### مرحله 2: به‌روزرسانی پکیج‌ها
```bash
pkg update
pkg upgrade -y
```

#### مرحله 3: نصب Multi Wizard
```bash
pkg install curl git -y
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

#### زمان تقریبی نصب:
⏱️ **10-20 دقیقه** (بسته به گوشی و اینترنت)

#### نکات مهم برای Termux:
1. **Termux را باز نگه دارید** - در حین نصب Termux را نبندید
2. **Wake Lock فعال کنید**:
   ```bash
   termux-wake-lock
   ```
3. **Battery Optimization را غیرفعال کنید**:
   - Settings → Apps → Termux → Battery → Unrestricted

---

### 🪟 نصب در Windows

#### روش 1: WSL2 (توصیه می‌شود)

##### مرحله 1: نصب WSL2
```powershell
wsl --install
```

##### مرحله 2: راه‌اندازی مجدد
کامپیوتر را Restart کنید

##### مرحله 3: نصب Ubuntu
1. باز کردن Microsoft Store
2. جستجوی "Ubuntu"
3. نصب Ubuntu
4. باز کردن Ubuntu از Start Menu

##### مرحله 4: نصب Multi Wizard
```bash
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

#### روش 2: Git Bash
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh)
```

---

## ▶️ اجرای دستی

بعد از نصب، برای اجرای دستی:

```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```

یا:

```bash
cd ~/multi-proxy-config-fetcher
bash manage.sh start
```

### زمان تقریبی اجرا:
⏱️ **5-15 دقیقه** (بسته به تعداد کانفیگ‌ها)

### مراحل اجرا:
```
➤ Fetch Configs              ✓ دریافت از منابع
➤ Enrich Configs             ✓ شناسایی موقعیت جغرافیایی
➤ Rename Configs             ✓ تغییر نام با جزئیات
➤ Test with Xray             ✓ تست سلامت مرحله 1
➤ Convert to Sing-box        ✓ تبدیل فرمت Sing-box
➤ Test with Sing-box         ✓ تست سلامت مرحله 2
➤ Security Filter            ✓ فیلتر امنیتی
➤ Generate Clash YAML        ✓ ساخت کانفیگ Clash/Mihomo
➤ Generate Balanced          ✓ ساخت لودبالانس Xray
➤ Generate Charts            ✓ ساخت نمودارها
```

---

## ⏰ تنظیم اجرای خودکار

Multi Wizard به طور پیش‌فرض **هر 12 ساعت** یکبار اجرا می‌شود. برای تغییر این زمان:

---

### 🐧 Linux - تنظیم Cron

#### روش 1: تنظیم سریع با یک دستور

**هر 1 ساعت:**
```bash
echo "0 * * * * bash $HOME/multi-proxy-config-fetcher/run.sh >> $HOME/multi-proxy-config-fetcher/logs/cron.log 2>&1" | crontab -
```

**هر 6 ساعت:**
```bash
echo "0 */6 * * * bash $HOME/multi-proxy-config-fetcher/run.sh >> $HOME/multi-proxy-config-fetcher/logs/cron.log 2>&1" | crontab -
```

**هر 12 ساعت (پیش‌فرض):**
```bash
echo "0 */12 * * * bash $HOME/multi-proxy-config-fetcher/run.sh >> $HOME/multi-proxy-config-fetcher/logs/cron.log 2>&1" | crontab -
```

**هر 24 ساعت (روزانه در ساعت 8 صبح):**
```bash
echo "0 8 * * * bash $HOME/multi-proxy-config-fetcher/run.sh >> $HOME/multi-proxy-config-fetcher/logs/cron.log 2>&1" | crontab -
```

---

#### روش 2: ویرایش دستی Crontab

```bash
crontab -e
```

**فرمت Cron:**
```
دقیقه ساعت روز ماه روزهفته دستور
```

**مثال‌ها:**
```bash
0 * * * *        # هر 1 ساعت
0 */2 * * *      # هر 2 ساعت
0 */6 * * *      # هر 6 ساعت
0 */12 * * *     # هر 12 ساعت
0 8 * * *        # روزانه ساعت 8 صبح
0 8,20 * * *     # روزانه ساعت 8 صبح و 8 شب
*/30 * * * *     # هر 30 دقیقه
```

**بعد از ویرایش:**
- فشار `Ctrl + O` (ذخیره)
- فشار `Enter`
- فشار `Ctrl + X` (خروج)

---

#### بررسی Cron Jobs فعلی:
```bash
crontab -l
```

#### حذف تمام Cron Jobs:
```bash
crontab -r
```

#### بررسی وضعیت سرویس Cron:
```bash
sudo systemctl status cron
```

یا:
```bash
sudo systemctl status cronie
```

#### راه‌اندازی سرویس Cron:
```bash
sudo systemctl start cron
sudo systemctl enable cron
```

---

### 📱 Termux - تنظیم Service

#### روش 1: تنظیم سریع با یک دستور

**تغییر به هر 1 ساعت (پیشنهادی):**
```bash
sed -i 's/INTERVAL=43200/INTERVAL=3600/' $PREFIX/var/service/multiproxy/run && sv restart multiproxy
```

**تغییر به هر 1 ساعت:**
```bash
echo "0 * * * * bash $HOME/multi-proxy-config-fetcher/run.sh >> $HOME/multi-proxy-config-fetcher/logs/cron.log 2>&1" | crontab -
crond
```

**تغییر به هر 6 ساعت:**
```bash
echo "0 */6 * * * bash $HOME/multi-proxy-config-fetcher/run.sh >> $HOME/multi-proxy-config-fetcher/logs/cron.log 2>&1" | crontab -
crond
```

**تغییر به هر 12 ساعت (پیش‌فرض):**
```bash
echo "0 */12 * * * bash $HOME/multi-proxy-config-fetcher/run.sh >> $HOME/multi-proxy-config-fetcher/logs/cron.log 2>&1" | crontab -
crond
```

---

#### روش 2: تغییر Service Interval

اگر از `termux-services` استفاده می‌کنید:

```bash
nano $PREFIX/var/service/multiproxy/run
```

**در خط `INTERVAL` تغییر دهید:**
```bash
INTERVAL=3600      # 1 ساعت
INTERVAL=21600     # 6 ساعت
INTERVAL=43200     # 12 ساعت
INTERVAL=86400     # 24 ساعت
```

**ذخیره و خروج:**
- `Ctrl + O` → `Enter` → `Ctrl + X`

**Restart سرویس:**
```bash
sv restart multiproxy
```

---

#### بررسی وضعیت:
```bash
sv status multiproxy
```

#### مشاهده لاگ‌ها:
```bash
tail -f ~/multi-proxy-config-fetcher/logs/cron.log
```

#### بررسی Cron Jobs:
```bash
crontab -l
```

#### بررسی crond:
```bash
pgrep crond
```

اگر خروجی نداد، crond را راه‌اندازی کنید:
```bash
crond
termux-wake-lock
```

---

### 🍎 macOS - تنظیم LaunchAgent

#### روش 1: تنظیم سریع

**هر 1 ساعت:**
```bash
cat > ~/Library/LaunchAgents/com.anonymous.multiproxy.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.anonymous.multiproxy</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$HOME/multi-proxy-config-fetcher/run.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF

launchctl unload ~/Library/LaunchAgents/com.anonymous.multiproxy.plist 2>/dev/null
launchctl load ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
```

**هر 6 ساعت:**
```bash
sed -i '' 's/<integer>.*<\/integer>/<integer>21600<\/integer>/' ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
launchctl unload ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
launchctl load ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
```

**هر 12 ساعت:**
```bash
sed -i '' 's/<integer>.*<\/integer>/<integer>43200<\/integer>/' ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
launchctl unload ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
launchctl load ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
```

---

#### روش 2: ویرایش دستی

```bash
nano ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
```

**برای اجرای دوره‌ای، از `StartInterval` استفاده کنید:**
```xml
<key>StartInterval</key>
<integer>3600</integer>
```

**مقادیر:**
- `3600` = 1 ساعت
- `21600` = 6 ساعت
- `43200` = 12 ساعت
- `86400` = 24 ساعت

**برای اجرای در ساعت‌های مشخص، از `StartCalendarInterval` استفاده کنید:**
```xml
<key>StartCalendarInterval</key>
<array>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <dict>
        <key>Hour</key>
        <integer>20</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</array>
```

**بعد از ویرایش:**
```bash
launchctl unload ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
launchctl load ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
```

---

#### بررسی وضعیت:
```bash
launchctl list | grep multiproxy
```

#### مشاهده لاگ‌ها:
```bash
tail -f ~/multi-proxy-config-fetcher/logs/launchd.log
```

---

### 🪟 Windows (WSL2) - تنظیم Cron

دقیقاً مانند Linux:

```bash
echo "0 * * * * bash $HOME/multi-proxy-config-fetcher/run.sh >> $HOME/multi-proxy-config-fetcher/logs/cron.log 2>&1" | crontab -
```

**راه‌اندازی Cron در WSL2:**
```bash
sudo service cron start
sudo service cron status
```

**برای اجرای خودکار Cron بعد از راه‌اندازی WSL2:**
```bash
echo "sudo service cron start" >> ~/.bashrc
```

---

## 🔧 مدیریت سیستم

### دستورات موجود:

#### 1️⃣ اجرای Pipeline
```bash
bash manage.sh start
```

---

#### 2️⃣ بررسی وضعیت
```bash
bash manage.sh status
```

**خروجی نمونه:**
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

#### 3️⃣ مشاهده لاگ‌ها
```bash
bash manage.sh logs
```

---

#### 4️⃣ پاکسازی لاگ‌های قدیمی
```bash
bash manage.sh clean
```

---

#### 5️⃣ به‌روزرسانی از GitHub
```bash
bash manage.sh update
```

---

#### 6️⃣ Restart سرویس (Termux)
```bash
bash manage.sh restart-service
```

---

#### 7️⃣ راهنما
```bash
bash manage.sh help
```

---

## 📁 استفاده از کانفیگ‌ها

### انواع فایل‌های خروجی:

| فایل | توضیحات | کاربرد |
|------|---------|--------|
| `proxy_configs.txt` | کانفیگ‌های خام | v2rayNG, v2rayN |
| `proxy_configs_tested.txt` | تست شده با Xray | v2rayNG, v2rayN ⭐ |
| `singbox_configs_all.json` | همه کانفیگ‌ها Sing-box | SFA, Hiddify, NekoBox |
| `singbox_configs_tested.json` | تست شده Sing-box | SFA, Hiddify, NekoBox ⭐ |
| `singbox_configs_secure.json` | تست شده و امن | SFA, Hiddify 🛡️⭐ |
| `clash_configs_all.yaml` | همه کانفیگ‌ها Clash | Clash Verge, Mihomo |
| `clash_configs_tested.yaml` | تست شده Clash | Clash Verge, Mihomo ⭐ |
| `clash_configs_secure.yaml` | تست شده و امن Clash | Clash Verge, Mihomo 🛡️⭐ |
| `xray_loadbalanced_config.json` | لودبالانس Xray | v2rayNG, v2rayN ⭐ |
| `xray_secure_loadbalanced_config.json` | لودبالانس امن | v2rayNG, v2rayN 🛡️⭐ |

⭐ = توصیه می‌شود  
🛡️ = امنیت بالا

---

### 📱 استفاده در v2rayNG (Android)

#### روش 1: Import از فایل محلی

```bash
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json ~/storage/downloads/
```

**در v2rayNG:**
1. منو ☰ → Import config from file
2. انتخاب فایل از Downloads
3. Import

---

#### روش 2: HTTP Server (دسترسی از شبکه)

##### Terminal 1: راه‌اندازی Server
```bash
cd ~/multi-proxy-config-fetcher/configs
python -m http.server 8080
```

##### Terminal 2: پیدا کردن IP
```bash
ifconfig wlan0 | grep "inet " | awk '{print $2}'
```

**در v2rayNG:**

**Import یکباره:**
```
http://YOUR_IP:8080/xray_secure_loadbalanced_config.json
```

**Subscription (به‌روزرسانی خودکار):**
```
http://YOUR_IP:8080/proxy_configs_tested.txt
```

---

### 💻 استفاده در v2rayN (Windows)

```bash
cp ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json /mnt/c/Users/YOUR_USERNAME/Downloads/
```

**در v2rayN:**
- منو → Import → Import from file

---

### 🐱 استفاده در Clash / Mihomo (Android, iOS, Windows, macOS, Linux)

#### روش 1: Import از فایل محلی

```bash
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/clash_configs_secure.yaml ~/storage/downloads/
```

**در Clash Verge یا Mihomo:**
1. Profiles → Import → Select file
2. انتخاب فایل `clash_configs_secure.yaml`
3. Import

---

#### روش 2: HTTP Server (دسترسی از شبکه)

```bash
cd ~/multi-proxy-config-fetcher/configs
python -m http.server 8080
```

**لینک اشتراک Clash:**
```
http://YOUR_IP:8080/clash_configs_tested.yaml
```

---

### 📦 استفاده در Sing-box Apps

```bash
cp ~/multi-proxy-config-fetcher/configs/singbox_configs_secure.json ~/storage/downloads/
```

**در برنامه:**
- Import → Select file

---

## 🔄 به‌روزرسانی

### به‌روزرسانی دستی:
```bash
cd ~/multi-proxy-config-fetcher
bash manage.sh update
```

یا:
```bash
cd ~/multi-proxy-config-fetcher
git pull origin main
pip install -r requirements.txt
```

---

## 🐛 عیب‌یابی

### مشکل 1: Cron اجرا نمی‌شود

#### Linux:
```bash
sudo systemctl status cron
sudo systemctl start cron
sudo systemctl enable cron
```

#### Termux:
```bash
pgrep crond || crond
termux-wake-lock
```

#### بررسی Cron Jobs:
```bash
crontab -l
```

---

### مشکل 2: خطای Permission

```bash
cd ~/multi-proxy-config-fetcher
chmod +x run.sh manage.sh install.sh
```

---

### مشکل 3: Python Module خطا

```bash
cd ~/multi-proxy-config-fetcher
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

### مشکل 4: Termux Service متوقف می‌شود

```bash
sv status multiproxy
sv up multiproxy
termux-wake-lock
```

**بررسی Boot Script:**
```bash
ls -la ~/.termux/boot/
cat ~/.termux/boot/start-multiproxy
```

---

### مشکل 5: لاگ‌ها خالی است

```bash
tail -f ~/multi-proxy-config-fetcher/logs/cron.log
tail -f ~/multi-proxy-config-fetcher/logs/run_*.log
```

---

## 🗑️ حذف کامل

### مرحله 1: حذف Cron/Service

**Linux:**
```bash
crontab -r
```

**Termux:**
```bash
crontab -r
sv down multiproxy
rm -rf $PREFIX/var/service/multiproxy
```

**macOS:**
```bash
launchctl unload ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
rm ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
```

---

### مرحله 2: حذف فایل‌ها
```bash
rm -rf ~/multi-proxy-config-fetcher
```

---

### مرحله 3: حذف Xray و Sing-box (اختیاری)

**Linux:**
```bash
sudo rm /usr/local/bin/xray
sudo apt remove sing-box -y
```

**Termux:**
```bash
rm $PREFIX/bin/xray
pkg uninstall sing-box -y
```

**macOS:**
```bash
sudo rm /usr/local/bin/xray
brew uninstall sing-box
```

---

## 💡 نکات کاربردی

### 1. سفارشی‌سازی منابع
```bash
nano ~/multi-proxy-config-fetcher/src/user_settings.py
```

```python
SOURCE_URLS = [
    "https://t.me/s/your_channel",
    "https://raw.githubusercontent.com/user/repo/main/configs.txt",
]
```

---

### 2. تنظیم پروتکل‌های فعال
```python
ENABLED_PROTOCOLS = {
    "wireguard://": False,
    "hysteria2://": True,
    "vless://": True,
    "vmess://": True,
    "ss://": True,
    "trojan://": True,
    "tuic://": False,
}
```

---

### 3. تنظیم Worker ها

**سیستم قدرتمند:**
```python
SINGBOX_TESTER_MAX_WORKERS = 16
XRAY_TESTER_MAX_WORKERS = 16
```

**Termux/سیستم ضعیف:**
```python
SINGBOX_TESTER_MAX_WORKERS = 4
XRAY_TESTER_MAX_WORKERS = 4
```

---

### 4. Backup خودکار
```bash
cat > ~/multi-proxy-config-fetcher/backup.sh << 'EOF'
#!/usr/bin/env bash
DATE=$(date +%Y-%m-%d)
BACKUP_DIR=~/multi-proxy-backups/$DATE
mkdir -p $BACKUP_DIR
cp -r ~/multi-proxy-config-fetcher/configs $BACKUP_DIR/
echo "Backup created: $BACKUP_DIR"
EOF

chmod +x ~/multi-proxy-config-fetcher/backup.sh
```

**اضافه کردن به Cron:**
```bash
echo "0 */12 * * * cd ~/multi-proxy-config-fetcher && bash run.sh && bash backup.sh >> logs/backup.log 2>&1" | crontab -
```

---

### 5. نوتیفیکیشن Termux
```bash
pkg install termux-api
```

**اضافه کردن به run.sh:**
```bash
termux-notification --title "Multi Wizard" --content "Pipeline completed!" --priority high
```

---

## 🎓 آموزش سریع برای مبتدیان

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

## 🎯 خلاصه دستورات

| کار | دستور |
|-----|-------|
| نصب | `curl -fsSL URL \| bash` |
| اجرا | `bash run.sh` |
| وضعیت | `bash manage.sh status` |
| لاگ | `bash manage.sh logs` |
| به‌روزرسانی | `bash manage.sh update` |
| Cron هر 1 ساعت | `echo "0 * * * * bash $HOME/multi-proxy-config-fetcher/run.sh" \| crontab -` |
| Cron هر 6 ساعت | `echo "0 */6 * * * bash $HOME/multi-proxy-config-fetcher/run.sh" \| crontab -` |
| Cron هر 12 ساعت | `echo "0 */12 * * * bash $HOME/multi-proxy-config-fetcher/run.sh" \| crontab -` |
| بررسی Cron | `crontab -l` |
| حذف Cron | `crontab -r` |
| راه‌اندازی crond | `crond` (Termux) |
| بررسی Service | `sv status multiproxy` (Termux) |
| Restart Service | `sv restart multiproxy` (Termux) |

---

## 📚 منابع بیشتر

- **ریپازیتوری اصلی**: https://github.com/4n0nymou3/multi-proxy-config-fetcher
- **صفحه وب کانفیگ‌ها**: https://4n0nymou3.github.io/Anonymous-Proxy-Hub/
- **Xray-core**: https://github.com/XTLS/Xray-core
- **Sing-box**: https://sing-box.sagernet.org
- **Clash/Mihomo**: https://github.com/MetaCubeX/mihomo
- **v2rayNG**: https://github.com/2dust/v2rayNG
- **Termux**: https://termux.dev
- **Crontab Guru** (برای تست فرمت Cron): https://crontab.guru

---

## ❓ سوالات متداول (FAQ)

### ❓ چگونه زمان اجرای خودکار را تغییر دهم؟

**پاسخ:**

**Linux/Termux/WSL2:**
```bash
echo "0 * * * * bash $HOME/multi-proxy-config-fetcher/run.sh >> $HOME/multi-proxy-config-fetcher/logs/cron.log 2>&1" | crontab -
```
این دستور را با زمان دلخواه تغییر دهید.

**macOS:**
```bash
nano ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
```
مقدار `StartInterval` را تغییر دهید (ثانیه).

---

### ❓ چگونه بررسی کنم که Cron کار می‌کند؟

**پاسخ:**
```bash
crontab -l
tail -f ~/multi-proxy-config-fetcher/logs/cron.log
```

**Termux:**
```bash
pgrep crond
```
اگر خروجی نداد:
```bash
crond
termux-wake-lock
```

---

### ❓ چرا بعد از restart گوشی، اجرای خودکار متوقف می‌شود؟

**پاسخ:**

1. **نصب Termux:Boot** از F-Droid
2. **یکبار Termux:Boot را باز کنید**
3. **بررسی Boot Script:**
```bash
ls -la ~/.termux/boot/
cat ~/.termux/boot/start-multiproxy
```

اگر فایل وجود ندارد:
```bash
mkdir -p ~/.termux/boot
cat > ~/.termux/boot/start-multiproxy << 'EOF'
#!/data/data/com.termux/files/usr/bin/sh
sleep 10
termux-wake-lock
sv-enable multiproxy
sv up multiproxy
EOF
chmod +x ~/.termux/boot/start-multiproxy
```

4. **غیرفعال کردن Battery Optimization:**
   - Settings → Apps → Termux → Battery → **Unrestricted**

---

### ❓ چگونه فقط یک نوع کانفیگ (مثلا فقط VLESS) دریافت کنم؟

**پاسخ:**
```bash
nano ~/multi-proxy-config-fetcher/src/user_settings.py
```

```python
ENABLED_PROTOCOLS = {
    "wireguard://": False,
    "hysteria2://": False,
    "vless://": True,
    "vmess://": False,
    "ss://": False,
    "trojan://": False,
    "tuic://": False,
}
```

---

### ❓ چطور تعداد کانفیگ‌ها را محدود کنم؟

**پاسخ:**
```bash
nano ~/multi-proxy-config-fetcher/src/user_settings.py
```

```python
USE_MAXIMUM_POWER = False
SPECIFIC_CONFIG_COUNT = 50
```

---

### ❓ چگونه کانفیگ‌ها را در شبکه محلی به اشتراک بگذارم؟

**پاسخ:**
```bash
cd ~/multi-proxy-config-fetcher/configs
python -m http.server 8080
```

**پیدا کردن IP:**
```bash
ifconfig wlan0 | grep "inet " | awk '{print $2}'
```

**لینک اشتراک‌گذاری:**
```
http://YOUR_IP:8080/proxy_configs_tested.txt
```

---

### ❓ چگونه لاگ‌های قدیمی را پاک کنم؟

**پاسخ:**
```bash
bash manage.sh clean
```

یا:
```bash
find ~/multi-proxy-config-fetcher/logs -name "*.log" -mtime +7 -delete
```

---

### ❓ چگونه بفهمم کدام کانفیگ کار می‌کند؟

**پاسخ:**

فایل‌های با پسوند `_tested` یا `_secure` تست شده‌اند:
- `proxy_configs_tested.txt` ✅
- `singbox_configs_tested.json` ✅
- `singbox_configs_secure.json` ✅ (امن‌ترین)
- `clash_configs_tested.yaml` ✅
- `clash_configs_secure.yaml` ✅ (امن‌ترین)
- `xray_secure_loadbalanced_config.json` ✅ (امن‌ترین)

---

### ❓ چگونه از GitHub به‌روزرسانی خودکار داشته باشم؟

**پاسخ:**

**روش 1: Fork و Private کردن ریپازیتوری**
1. Fork کنید
2. Private کنید
3. GitHub Actions را فعال کنید
4. از Raw URL استفاده کنید

**روش 2: اضافه کردن به Cron**
```bash
echo "0 0 * * * cd ~/multi-proxy-config-fetcher && git pull origin main" | crontab -
```

---

### ❓ چگونه Interval سرویس Termux را تغییر دهم؟

**پاسخ:**
```bash
nano $PREFIX/var/service/multiproxy/run
```

**تغییر خط:**
```bash
INTERVAL=3600      # 1 ساعت
INTERVAL=21600     # 6 ساعت
INTERVAL=43200     # 12 ساعت
```

**Restart:**
```bash
sv restart multiproxy
```

---

### ❓ چگونه Wake Lock دائمی در Termux فعال کنم؟

**پاسخ:**

**روش 1: دستی**
```bash
termux-wake-lock
```

**روش 2: خودکار در Boot**
```bash
cat >> ~/.termux/boot/start-multiproxy << 'EOF'
termux-wake-lock
EOF
```

**روش 3: اضافه کردن به bashrc**
```bash
echo "termux-wake-lock 2>/dev/null || true" >> ~/.bashrc
```

---

### ❓ چگونه مانیتور کنم که Pipeline با موفقیت اجرا شده؟

**پاسخ:**

**روش 1: بررسی لاگ**
```bash
tail -20 ~/multi-proxy-config-fetcher/logs/cron.log
```

**روش 2: بررسی تاریخ فایل‌ها**
```bash
ls -lt ~/multi-proxy-config-fetcher/configs/
```

**روش 3: نوتیفیکیشن Termux**
```bash
pkg install termux-api
```

اضافه کردن به انتهای `run.sh`:
```bash
termux-notification --title "✅ Multi Wizard" --content "Pipeline completed at $(date)" --priority high
```

**روش 4: ارسال به Telegram Bot**
```bash
TELEGRAM_BOT_TOKEN="YOUR_TOKEN"
TELEGRAM_CHAT_ID="YOUR_ID"
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${TELEGRAM_CHAT_ID}" \
  -d "text=✅ Multi Wizard completed at $(date)"
```

---

### ❓ چگونه فقط کانفیگ‌های کشور خاص را دریافت کنم؟

**پاسخ:**

این قابلیت در حال حاضر وجود ندارد، ولی می‌توانید بعد از دریافت فیلتر کنید:

```bash
grep "🇺🇸" ~/multi-proxy-config-fetcher/configs/proxy_configs_tested.txt > us_configs.txt
grep "🇩🇪" ~/multi-proxy-config-fetcher/configs/proxy_configs_tested.txt > de_configs.txt
```

---

### ❓ چگونه سرعت تست کانفیگ‌ها را افزایش دهم؟

**پاسخ:**
```bash
nano ~/multi-proxy-config-fetcher/src/user_settings.py
```

```python
SINGBOX_TESTER_MAX_WORKERS = 16
XRAY_TESTER_MAX_WORKERS = 16
SINGBOX_TESTER_TIMEOUT_SECONDS = 5
XRAY_TESTER_TIMEOUT_SECONDS = 5
```

⚠️ **هشدار**: در Termux مقدار بالای 8 توصیه نمی‌شود.

---

### ❓ چگونه URL تست را تغییر دهم؟

**پاسخ:**
```bash
nano ~/multi-proxy-config-fetcher/src/user_settings.py
```

```python
SINGBOX_TESTER_URLS = [
    'https://www.google.com/generate_204',
    'https://www.cloudflare.com/cdn-cgi/trace'
]

XRAY_TESTER_URLS = [
    'https://www.google.com/generate_204',
    'https://1.1.1.1'
]
```

---

## 🔐 نکات امنیتی

### 1. استفاده از کانفیگ‌های Secure

**همیشه از فایل‌های secure استفاده کنید:**
- ✅ `xray_secure_loadbalanced_config.json`
- ✅ `singbox_configs_secure.json`
- ✅ `clash_configs_secure.yaml`

**از این فایل‌ها استفاده نکنید:**
- ❌ `proxy_configs.txt` (تست نشده)
- ❌ `singbox_configs_all.json` (تست نشده)
- ❌ `clash_configs_all.yaml` (تست نشده)

---

### 2. رمزنگاری کانفیگ‌ها

```bash
pkg install gnupg
gpg -c ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json
```

**رمزگشایی:**
```bash
gpg ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json.gpg
```

---

### 3. محافظت از ریپازیتوری GitHub

اگر Fork کردید:
1. **حتماً Private کنید**
2. GitHub Actions را فعال کنید
3. از Token دسترسی استفاده کنید (نه password)

---

### 4. محافظت از HTTP Server

```bash
cd ~/multi-proxy-config-fetcher/configs
python -m http.server 8080 --bind 127.0.0.1
```

فقط localhost دسترسی دارد.

---

## 🛠️ عیب‌یابی پیشرفته

### مشکل: Pipeline اجرا می‌شود ولی کانفیگ جدید نمی‌آید

**راه حل:**
```bash
cd ~/multi-proxy-config-fetcher
bash manage.sh logs
```

**بررسی:**
- آیا منابع در دسترس هستند?
- آیا تمام مراحل با موفقیت اجرا شدند?

**تست دستی:**
```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```

---

### مشکل: Xray یا Sing-box نصب نمی‌شود

**Linux:**
```bash
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
bash <(curl -fsSL https://sing-box.app/install.sh)
```

**Termux:**
```bash
pkg install xray sing-box -y
```

**macOS:**
```bash
brew install xray sing-box
```

---

### مشکل: Virtual Environment خطا می‌دهد

```bash
cd ~/multi-proxy-config-fetcher
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

### مشکل: Git Pull خطا می‌دهد

```bash
cd ~/multi-proxy-config-fetcher
git config --global --add safe.directory ~/multi-proxy-config-fetcher
git fetch --all
git reset --hard origin/main
git pull origin main
```

---

### مشکل: Termux Service کار نمی‌کند

```bash
sv status multiproxy
```

**اگر متوقف است:**
```bash
sv up multiproxy
```

**اگر وجود ندارد:**
```bash
mkdir -p $PREFIX/var/service/multiproxy
nano $PREFIX/var/service/multiproxy/run
```

محتوا:
```bash
#!/data/data/com.termux/files/usr/bin/sh
exec 2>&1
INSTALL_DIR="$HOME/multi-proxy-config-fetcher"
INTERVAL=43200
termux-wake-lock 2>/dev/null || true
while true; do
    if [ -d "$INSTALL_DIR" ]; then
        cd "$INSTALL_DIR"
        bash run.sh
    fi
    sleep $INTERVAL
done
```

```bash
chmod +x $PREFIX/var/service/multiproxy/run
sv-enable multiproxy
sv up multiproxy
```

---

### مشکل: فضای دیسک تمام شده

```bash
df -h
du -sh ~/multi-proxy-config-fetcher/*
```

**پاکسازی:**
```bash
cd ~/multi-proxy-config-fetcher
bash manage.sh clean
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find logs -name "*.log" -mtime +3 -delete
```

---

## 📊 بهینه‌سازی عملکرد

### 1. افزایش سرعت تست (سیستم قوی)

```python
SINGBOX_TESTER_MAX_WORKERS = 16
XRAY_TESTER_MAX_WORKERS = 16
SINGBOX_TESTER_TIMEOUT_SECONDS = 5
XRAY_TESTER_TIMEOUT_SECONDS = 5
```

---

### 2. کاهش مصرف منابع (Termux/سیستم ضعیف)

```python
SINGBOX_TESTER_MAX_WORKERS = 4
XRAY_TESTER_MAX_WORKERS = 4
SINGBOX_TESTER_TIMEOUT_SECONDS = 15
XRAY_TESTER_TIMEOUT_SECONDS = 15
```

---

### 3. کاهش تعداد کانفیگ‌ها

```python
USE_MAXIMUM_POWER = False
SPECIFIC_CONFIG_COUNT = 30
```

---

### 4. غیرفعال کردن تست‌ها (فقط دریافت)

```python
ENABLE_XRAY_TESTER = False
ENABLE_SINGBOX_TESTER = False
```

⚠️ **توصیه نمی‌شود**: کانفیگ‌های تست نشده ممکن است کار نکنند.

---

## 🎬 ویدیوهای آموزشی (پیشنهادی)

### قدم به قدم نصب در Termux:

1. نصب F-Droid و Termux
2. به‌روزرسانی پکیج‌ها
3. نصب Multi Wizard
4. اجرای اولین Pipeline
5. کپی کانفیگ‌ها به v2rayNG
6. تنظیم اجرای خودکار
7. استفاده از HTTP Server

---

## 📞 دریافت کمک

### پیش از درخواست کمک:

1. **بررسی لاگ‌ها:**
```bash
bash manage.sh logs
```

2. **بررسی وضعیت:**
```bash
bash manage.sh status
```

3. **تست دستی:**
```bash
bash run.sh
```

---

### راه‌های ارتباطی:

- **GitHub Issues**: https://github.com/4n0nymou3/multi-proxy-config-fetcher/issues
- **Twitter/X**: [@4n0nymou3](https://x.com/4n0nymou3)
- **GitHub Profile**: [@4n0nymou3](https://github.com/4n0nymou3)

---

## 📜 مجوز و سلب مسئولیت

این پروژه تحت مجوز **MIT License** منتشر شده است.

### ⚠️ سلب مسئولیت:
- این ابزار فقط برای اهداف **آموزشی و تحقیقاتی** ارائه شده است
- توسعه‌دهنده مسئولیتی در قبال استفاده نادرست ندارد
- کاربران موظفند قوانین محلی خود را رعایت کنند
- استفاده از کانفیگ‌های عمومی ممکن است ریسک امنیتی داشته باشد

---

## 🙏 تشکر و قدردانی

این پروژه با ❤️ توسط **👽 Anonymous** توسعه یافته است.

### سهم‌گذاران:
- **Xray-core Team** - موتور پروکسی قدرتمند
- **Sing-box Team** - موتور پروکسی جامع
- **Clash/Mihomo Team** - پلتفرم پروکسی مدرن
- **جامعه Open Source** - پشتیبانی و بازخورد

### حمایت از پروژه:
- ⭐ **Star** کردن در GitHub
- 🐛 گزارش باگ‌ها در Issues
- 💡 پیشنهاد ویژگی‌های جدید
- 📖 بهبود مستندات

---

<div align="center">

## 🚀 آماده شروع هستید؟

```bash
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

**ساخته شده با 💚 توسط Anonymous**

---

### 🌟 اگر این پروژه برای شما مفید بود، یک Star بدهید!

[⬆ بازگشت به بالا](#-راهنمای-کامل-multi-wizard)

</div>

</div>