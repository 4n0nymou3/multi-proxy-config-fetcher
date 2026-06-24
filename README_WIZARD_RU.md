# ⚙️ Anonymous Wizard — Руководство на русском

<p align="center">
  <img src="https://img.shields.io/badge/Anonymous-Wizard-blue?style=for-the-badge" />
</p>

Полное пошаговое руководство по установке, запуску и управлению проектом **Multi Proxy Config Fetcher** на вашей локальной системе — включая Termux (Android), Linux, macOS, iSH (iOS) и Windows (WSL2).

---

## 📋 Содержание

- [Предварительные требования](#предварительные-требования)
- [Автоматическая установка через Wizard](#автоматическая-установка)
- [Ручная установка](#ручная-установка)
- [Запуск проекта](#запуск-проекта)
- [Выходные файлы](#выходные-файлы)
- [Использование конфигураций](#использование-конфигураций)
- [Управление](#управление)
- [Меры безопасности](#меры-безопасности)
- [Устранение неполадок](#устранение-неполадок)
- [FAQ](#faq)
- [Обновление](#обновление)
- [Быстрый старт для Termux](#быстрый-старт-для-termux)

---

## 📦 Предварительные требования

Перед началом убедитесь, что установлены следующие инструменты:

| Инструмент | Версия | Назначение |
|-----------|--------|-----------|
| Python | 3.9+ | Основной язык |
| pip | Последняя | Менеджер пакетов |
| git | Любая | Клонирование репозитория |
| curl | Любая | Загрузка инструментов |
| cron | Любая | Запуск по расписанию |

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

## 🚀 Автоматическая установка через Wizard

Wizard автоматически устанавливает всё одной командой:

```bash
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

### Что делает Wizard:
1. Определяет вашу операционную систему
2. Автоматически устанавливает Xray-core
3. Автоматически устанавливает Sing-box
4. Устанавливает зависимости Python
5. Клонирует репозиторий
6. Создаёт скрипты запуска
7. Настраивает инструменты управления

### После установки:
```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```

---

## 🔧 Ручная установка

Если вы предпочитаете установку вручную:

### Шаг 1: Клонирование репозитория
```bash
git clone https://github.com/4n0nymou3/multi-proxy-config-fetcher.git
cd multi-proxy-config-fetcher
```

### Шаг 2: Установка зависимостей Python
```bash
pip install -r requirements.txt
```

### Шаг 3: Установка Xray-core

**Linux/Termux:**
```bash
bash <(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)
```

### Шаг 4: Установка Sing-box

**Linux:**
```bash
bash <(curl -fsSL https://sing-box.app/deb-install.sh)
```

**Termux:**
```bash
pkg install sing-box -y
```

---

## ▶️ Запуск проекта

### Шаги конвейера:
```
➤ Fetch Configs              ✓ Получение из всех источников
➤ Enrich Configs             ✓ Геолокационное обогащение
➤ Rename Configs             ✓ Переименование с метками
➤ Test with Xray             ✓ Проверка работоспособности - Этап 1
➤ Convert to Sing-box        ✓ Конвертация в формат Sing-box
➤ Test with Sing-box         ✓ Проверка работоспособности - Этап 2
➤ Security Filter            ✓ Фильтрация по безопасности
➤ Generate Clash YAML        ✓ Генерация конфигураций Clash/Mihomo
➤ Generate Balanced          ✓ Генерация балансировщика Xray
➤ Generate Charts            ✓ Генерация графиков
```

### Однократный запуск:
```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```

### Запуск через cron (каждые 12 часов):
```bash
crontab -e
```
Добавьте строку:
```
0 */12 * * * cd ~/multi-proxy-config-fetcher && bash run.sh >> logs/cron.log 2>&1
```

---

## 📁 Выходные файлы

| Файл | Описание | Совместимые клиенты |
|------|---------|-------------------|
| `proxy_configs.txt` | Исходные конфигурации | v2rayNG, v2rayN |
| `proxy_configs_tested.txt` | Проверено Xray | v2rayNG, v2rayN ⭐ |
| `singbox_configs_all.json` | Все Sing-box | SFA, Hiddify, NekoBox |
| `singbox_configs_tested.json` | Sing-box проверено | SFA, Hiddify, NekoBox ⭐ |
| `singbox_configs_secure.json` | Проверено и безопасно | SFA, Hiddify 🛡️⭐ |
| `clash_configs_all.yaml` | Все Clash | Clash Verge, Mihomo |
| `clash_configs_tested.yaml` | Clash проверено | Clash Verge, Mihomo ⭐ |
| `clash_configs_secure.yaml` | Проверено и безопасно | Clash Verge, Mihomo 🛡️⭐ |
| `xray_loadbalanced_config.json` | Балансировщик Xray | v2rayNG, v2rayN ⭐ |
| `xray_secure_loadbalanced_config.json` | Безопасный балансировщик | v2rayNG, v2rayN 🛡️⭐ |

⭐ = Рекомендуется
🛡️ = Высокий уровень безопасности

---

## 📱 Использование конфигураций

---

### 🐱 Использование в Clash / Mihomo (Android, iOS, Windows, macOS, Linux)

#### Способ 1: Импорт из локального файла

```bash
# Termux
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/clash_configs_secure.yaml ~/storage/downloads/
```

**В Clash Verge или Mihomo:**
1. Profiles → Import → Select file
2. Выберите `clash_configs_secure.yaml`
3. Импортируйте

---

#### Способ 2: HTTP-сервер (доступ из сети)

```bash
cd ~/multi-proxy-config-fetcher/configs
python -m http.server 8080
```

**Ссылка на подписку Clash:**
```
http://YOUR_IP:8080/clash_configs_tested.yaml
```

---

### 📦 Использование в приложениях Sing-box

#### Способ 1: Импорт из локального файла

**Termux:**
```bash
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/singbox_configs_secure.json ~/storage/downloads/
```

**В Sing-box For Android (SFA):**
1. Profiles → New Profile → Import
2. Выберите `singbox_configs_secure.json`
3. Импортируйте

---

#### Способ 2: HTTP-сервер

```bash
cd ~/multi-proxy-config-fetcher/configs
python -m http.server 8080
```

**Ссылка на подписку Sing-box:**
```
http://YOUR_IP:8080/singbox_configs_tested.json
```

---

### 🚀 Использование в v2rayNG / v2rayN

#### Способ 1: Ссылка на подписку

```bash
cd ~/multi-proxy-config-fetcher/configs
python -m http.server 8080
```

**URL подписки:**
```
http://YOUR_IP:8080/proxy_configs_tested.txt
```

В v2rayNG:
1. Подписки → Добавить подписку
2. Введите URL
3. Обновить

---

#### Способ 2: Прямой импорт JSON (Xray)

```bash
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json ~/storage/downloads/
```

---

## 🛠️ Управление

### manage.sh

После установки доступен инструмент `manage.sh`:

```bash
bash ~/multi-proxy-config-fetcher/manage.sh status     # Проверить статус
bash ~/multi-proxy-config-fetcher/manage.sh run        # Запустить конвейер
bash ~/multi-proxy-config-fetcher/manage.sh update     # Обновить код
bash ~/multi-proxy-config-fetcher/manage.sh logs       # Просмотр логов
bash ~/multi-proxy-config-fetcher/manage.sh cron       # Управление cron
bash ~/multi-proxy-config-fetcher/manage.sh clean      # Очистить старые файлы
```

**Пример вывода:**
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

### Настройка cron (автозапуск каждые 12 часов)

```bash
bash ~/multi-proxy-config-fetcher/manage.sh cron
```

Или вручную:
```bash
crontab -e
```
Добавьте:
```
0 */12 * * * cd ~/multi-proxy-config-fetcher && bash run.sh >> logs/cron.log 2>&1
```

---

## 🔒 Меры безопасности

**Всегда используйте файлы secure:**
- ✅ `xray_secure_loadbalanced_config.json`
- ✅ `singbox_configs_secure.json`
- ✅ `clash_configs_secure.yaml`

**Не используйте эти файлы:**
- ❌ `proxy_configs.txt` (не проверено)
- ❌ `singbox_configs_all.json` (не проверено)
- ❌ `clash_configs_all.yaml` (не проверено)

### Что делает фильтр безопасности:
- Удаляет конфигурации с недействительным TLS
- Удаляет устаревшее или небезопасное шифрование
- Удаляет устаревшие протоколы
- Создаёт отдельные файлы для безопасных узлов

---

## 🔧 Устранение неполадок

### Xray не найден:
```bash
which xray || ls ~/.local/share/xray/xray 2>/dev/null || ls /usr/local/bin/xray 2>/dev/null
```

**Решение — переустановить:**
```bash
bash <(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)
```

### Sing-box не найден:
```bash
which sing-box || ls ~/go/bin/sing-box 2>/dev/null
```

**Решение — переустановить (Termux):**
```bash
pkg install sing-box -y
```

### Ошибки Python:
```bash
pip install -r requirements.txt --upgrade
```

### Нет выходных файлов:
```bash
ls -la configs/
cat logs/run_*.log | tail -50
```

### Cron не работает:
```bash
crontab -l
service cron status
```

---

## ❓ FAQ

**В: Как понять, какой файл конфигурации работает?**
Файлы с суффиксом `_tested` или `_secure` прошли проверку:
- `proxy_configs_tested.txt` ✅
- `singbox_configs_tested.json` ✅
- `singbox_configs_secure.json` ✅ (наиболее безопасный)
- `clash_configs_tested.yaml` ✅
- `clash_configs_secure.yaml` ✅ (наиболее безопасный)
- `xray_secure_loadbalanced_config.json` ✅ (наиболее безопасный)

---

**В: Как часто обновляются конфигурации?**
При использовании cron — автоматически каждые 12 часов. Интервал можно изменить в crontab.

---

**В: Сколько конфигураций получает система?**
Зависит от `USE_MAXIMUM_POWER` в `src/user_settings.py`. При значении `True` загружается максимально возможное количество.

---

**В: Можно ли добавить собственные источники?**
Да, добавьте их в `SOURCE_URLS` в `src/user_settings.py`:
```python
SOURCE_URLS = [
    "https://t.me/s/your_channel",
    "https://raw.githubusercontent.com/user/repo/main/configs.txt",
]
```

---

**В: Работает ли это на старых Android-устройствах?**
Да. Проверено на Android 7+. Требуется Termux, установленный из F-Droid (не из Google Play).

---

**В: Чем отличаются конфигурации Sing-box, Clash и Xray?**
- **Xray** — совместим с v2rayNG, v2rayN, Nekoray
- **Sing-box** — совместим с SFA, Hiddify, NekoBox
- **Clash/Mihomo** — совместим с Clash Verge, Mihomo, Clash Meta

Все три генерируются из одного списка прокси и функционально эквивалентны.

---

## 🔄 Обновление

```bash
cd ~/multi-proxy-config-fetcher
bash manage.sh update
```

Или вручную:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

## 🤝 Участие в разработке

Мы приветствуем любой вклад:
1. Сделайте fork репозитория
2. Создайте ветку для новой функции
3. Внесите изменения
4. Отправьте Pull Request

---

## 🙏 Благодарности

### Участники:
- **Xray-core Team** — высокопроизводительный прокси-движок
- **Sing-box Team** — универсальный прокси-движок
- **Clash/Mihomo Team** — современная прокси-платформа
- **Сообщество Open Source** — поддержка и обратная связь

---

## 📚 Ресурсы

- **Основной репозиторий**: https://github.com/4n0nymou3/multi-proxy-config-fetcher
- **Веб-страница конфигураций**: https://4n0nymou3.github.io/Anonymous-Proxy-Hub/
- **Xray-core**: https://github.com/XTLS/Xray-core
- **Sing-box**: https://sing-box.sagernet.org
- **Clash/Mihomo**: https://github.com/MetaCubeX/mihomo
- **v2rayNG**: https://github.com/2dust/v2rayNG
- **Termux**: https://termux.dev
- **Crontab Guru** (проверка формата cron): https://crontab.guru

---

## 📄 Лицензия

Лицензия MIT — подробности в файле [LICENSE](LICENSE).

---

## 📬 Контакты

- **GitHub**: https://github.com/4n0nymou3
- **Twitter**: https://x.com/4n0nymou3

---

## ⚡ Быстрый старт для Termux

Для новых пользователей, которые хотят начать немедленно:

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

> 🎉 **Поздравляем!** Ваш загрузчик конфигураций прокси настроен и работает. Конфигурации будут автоматически обновляться каждые 12 часов. При возникновении проблем проверьте логи с помощью `bash manage.sh logs`.
