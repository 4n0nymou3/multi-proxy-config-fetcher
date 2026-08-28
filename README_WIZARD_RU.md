# ⚙️ Anonymous Wizard — руководство по установке на русском

<p align="center">
  <img src="https://img.shields.io/badge/Anonymous-Wizard-blue?style=for-the-badge" />
</p>

Полное пошаговое руководство по установке, запуску и управлению проектом **Multi Proxy Config Fetcher** на вашей локальной системе — включая Termux (Android), Linux, macOS, iSH (iOS) и Windows (через WSL2).

---

## 📋 Содержание

- [Предварительные требования](#-предварительные-требования)
- [Автоматическая установка с Wizard](#-автоматическая-установка-с-wizard)
- [Ручная установка](#-ручная-установка)
- [Запуск проекта](#️-запуск-проекта)
- [Выходные файлы](#-выходные-файлы)
- [Использование конфигураций](#-использование-конфигураций)
- [Скрипт управления](#️-скрипт-управления)
- [Расписание автоматического запуска](#-расписание-автоматического-запуска)
- [Настройка источников и параметров](#-настройка-источников-и-параметров)
- [Настройка конечной точки Fragment](#-настройка-конечной-точки-fragment)
- [Заметки по безопасности](#-заметки-по-безопасности)
- [Решение проблем](#-решение-проблем)
- [Часто задаваемые вопросы](#-часто-задаваемые-вопросы)
- [Обновление](#-обновление)
- [Быстрый старт для Termux](#-быстрый-старт-для-termux)

---

## 📦 Предварительные требования

Wizard устанавливает всё нижеперечисленное автоматически. Если вы устанавливаете вручную, убедитесь, что у вас есть:

| Инструмент | Версия | Назначение |
|-----------|--------|-----------|
| Python | 3.9+ | Запуск пайплайна |
| pip | Последняя | Установка Python-зависимостей |
| git | Любая | Клонирование репозитория |
| curl | Любая | Загрузка Xray/Sing-box |
| cron (Linux) / launchd (macOS) | Любая | Запуск по расписанию |

**Пользователи Windows:** установщик не работает нативно на Windows. Используйте **WSL2** (подсистема Windows для Linux) и выполняйте все команды из этого руководства внутри вашего Linux-дистрибутива WSL2.

---

## 🚀 Автоматическая установка с Wizard

Одна команда определяет вашу платформу и устанавливает всё необходимое: Xray-core, Sing-box, Python-зависимости, сам репозиторий, скрипт запуска, скрипт управления и запланированную задачу (cron / служба Termux / launchd — в зависимости от платформы).

```bash
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

### Что делает Wizard, шаг за шагом:
1. Определяет вашу операционную систему (Termux, Linux или macOS)
2. Устанавливает системные зависимости (git, Python, curl, cron и т.д.)
3. Клонирует (или обновляет) репозиторий в `~/multi-proxy-config-fetcher`
4. Создаёт виртуальное окружение Python и устанавливает `requirements.txt`
5. Устанавливает Xray-core
6. Устанавливает Sing-box
7. Генерирует `run.sh` — скрипт, запускающий весь пайплайн
8. Генерирует `manage.sh` — скрипт для повседневного использования
9. Настраивает автоматическое расписание для вашей платформы (см. [Расписание](#-расписание-автоматического-запуска))

### После установки запустите пайплайн вручную один раз:
```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```

---

## 🔧 Ручная установка

Если вы предпочитаете не запускать однострочную команду, вот что именно она делает "под капотом".

### Шаг 1: Клонирование репозитория
```bash
git clone https://github.com/4n0nymou3/multi-proxy-config-fetcher.git
cd multi-proxy-config-fetcher
```

### Шаг 2: Установка Python-зависимостей
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Шаг 3: Установка Xray-core

**Linux/macOS:**
```bash
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
```

**Termux:** скачайте подходящую сборку для архитектуры вашего процессора напрямую со [страницы релизов Xray-core](https://github.com/XTLS/Xray-core/releases) и поместите бинарный файл `xray` куда-нибудь в `$PATH` (например, `$PREFIX/bin`).

### Шаг 4: Установка Sing-box

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

## ▶️ Запуск проекта

### Шаги пайплайна (в точном порядке):
```
1.  Fetch Configs                    Получение из всех настроенных источников
2.  Enrich Configs                   Определение геолокации серверов
3.  Rename Configs                   Применение описательных тегов
4.  Test with Xray                   Многораундовое тестирование - ядро Xray
5.  Convert to Sing-box              Построение формата JSON для Sing-box
6.  Test with Sing-box               Многораундовое тестирование - ядро Sing-box
7.  Security Filter                  Удаление небезопасных конфигов, пересборка безопасных версий
8.  Generate Clash YAML              Построение конфигураций Clash/Mihomo
9.  Generate Xray Balanced Config     Построение сбалансированной конфигурации Xray
10. Generate Xray Fragment Config     Построение конфигурации Xray с Fragment (анти-DPI)
11. Generate Charts                  Построение диаграмм производительности
12. Generate Pipeline Summary         Вывод количества конфигураций на каждом этапе
```

### Однократный запуск:
```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```

Каждый запуск также создаёт лог-файл с временной меткой в `logs/run_<дата>.log`, а логи старше 7 дней удаляются автоматически.

---

## 📁 Выходные файлы

| Файл | Описание | Совместимые приложения |
|------|----------|------------------------|
| `proxy_configs.txt` | Сырые конфигурации | v2rayNG, v2rayN |
| `proxy_configs_tested.txt` | Протестировано Xray | v2rayNG, v2rayN ⭐ |
| `singbox_configs_all.json` | Все конфигурации, формат Sing-box | SFA, Hiddify, NekoBox |
| `singbox_configs_tested.json` | Протестировано Sing-box | SFA, Hiddify, NekoBox ⭐ |
| `singbox_configs_secure.json` | Протестировано и отфильтровано по безопасности | SFA, Hiddify 🛡️⭐ |
| `clash_configs_all.yaml` | Все конфигурации, формат Clash | Clash Verge, Mihomo |
| `clash_configs_tested.yaml` | Протестировано для Clash | Clash Verge, Mihomo ⭐ |
| `clash_configs_secure.yaml` | Протестировано и отфильтровано по безопасности | Clash Verge, Mihomo 🛡️⭐ |
| `xray_loadbalanced_config.json` | Балансировщик нагрузки Xray | v2rayNG, v2rayN, Nekoray ⭐ |
| `xray_fragment_loadbalanced_config.json` | Балансировщик нагрузки Xray с продвинутой двухэтапной фрагментацией TLS для большей устойчивости к DPI | v2rayNG, v2rayN, Nekoray 🧩⭐ |
| `xray_secure_loadbalanced_config.json` | Безопасный балансировщик нагрузки Xray | v2rayNG, v2rayN, Nekoray 🛡️⭐ |

⭐ = Рекомендуется · 🛡️ = Повышенная безопасность · 🧩 = Фрагментация против цензуры

---

## 📱 Использование конфигураций

### 🐱 Использование в Clash / Mihomo (Android, iOS, Windows, macOS, Linux)

**Способ 1: импорт из локального файла**
```bash
# Termux
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/clash_configs_secure.yaml ~/storage/downloads/
```
В Clash Verge или Mihomo: **Profiles → Import → выбрать файл → `clash_configs_secure.yaml` → Import**

**Способ 2: раздача по HTTP (доступ с любого устройства в вашей сети)**
```bash
cd ~/multi-proxy-config-fetcher/configs
python3 -m http.server 8080
```
Ссылка подписки Clash:
```
http://YOUR_IP:8080/clash_configs_tested.yaml
```

---

### 📦 Использование в приложениях Sing-box (SFA, Hiddify, NekoBox)

**Способ 1: импорт из локального файла**
```bash
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/singbox_configs_secure.json ~/storage/downloads/
```
В Sing-box For Android (SFA): **Profiles → New Profile → Import → `singbox_configs_secure.json` → Import**

**Способ 2: раздача по HTTP**
```bash
cd ~/multi-proxy-config-fetcher/configs
python3 -m http.server 8080
```
Ссылка подписки Sing-box:
```
http://YOUR_IP:8080/singbox_configs_tested.json
```

---

### 🚀 Использование в v2rayNG / v2rayN / Nekoray

**Способ 1: ссылка подписки**
```bash
cd ~/multi-proxy-config-fetcher/configs
python3 -m http.server 8080
```
URL подписки:
```
http://YOUR_IP:8080/proxy_configs_tested.txt
```
В v2rayNG: **Subscription → Add Subscription → ввести URL → Update**

**Способ 2: прямой импорт JSON**
```bash
termux-setup-storage
cp ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json ~/storage/downloads/
```
Нужна более сильная устойчивость к блокировкам? Скопируйте таким же образом `xray_fragment_loadbalanced_config.json`.

---

## 🛠️ Скрипт управления

После установки `manage.sh` — ваш основной инструмент для повседневной работы:

```bash
bash ~/multi-proxy-config-fetcher/manage.sh start            # Запустить пайплайн вручную
bash ~/multi-proxy-config-fetcher/manage.sh status           # Показать версии Xray/Sing-box, статус службы, выходные файлы, последние логи
bash ~/multi-proxy-config-fetcher/manage.sh logs             # Показать последний лог
bash ~/multi-proxy-config-fetcher/manage.sh clean            # Удалить логи старше 7 дней
bash ~/multi-proxy-config-fetcher/manage.sh update           # Получить последний код с GitHub
bash ~/multi-proxy-config-fetcher/manage.sh restart-service  # Только Termux: перезапустить фоновую службу
bash ~/multi-proxy-config-fetcher/manage.sh help             # Показать этот список команд
```

**Пример вывода `status`:**
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

## ⏰ Расписание автоматического запуска

Wizard настраивает автоматические запуски за вас, но механизм отличается в зависимости от платформы:

| Платформа | Механизм | Интервал |
|-----------|----------|----------|
| Termux (Android) | Фоновая служба (`sv`), запускается при загрузке | Каждые 12 часов |
| Linux | `cron` | Каждые 12 часов (`0 */12 * * *`) |
| macOS | `launchd` (LaunchAgent) | Дважды в день, в 08:00 и 20:00 (по местному времени системы) |

### ⚠️ Termux — критически важный дополнительный шаг

Фоновая служба Termux **не** переживает перезагрузку телефона сама по себе. Чтобы автоматические запуски продолжали работать после перезагрузки, необходимо:
1. Установить **Termux:Boot** из F-Droid (не из Google Play)
2. **Один раз** открыть приложение Termux:Boot, чтобы Android его зарегистрировал
3. Перейти в **Настройки Android → Приложения → Termux → Батарея → Без ограничений**, чтобы Android не убивал фоновую службу

Без этих трёх шагов служба перестаёт работать после каждой перезагрузки, и вам придётся снова вручную запускать `bash run.sh`.

### Изменение интервала

**Linux (cron):**
```bash
crontab -e
```
Отредактируйте строку, добавленную установщиком, например, чтобы запускать каждые 6 часов вместо 12:
```
0 */6 * * * /bin/bash ~/multi-proxy-config-fetcher/run.sh >> ~/multi-proxy-config-fetcher/logs/cron.log 2>&1
```

**Termux:** отредактируйте `INTERVAL=43200` (в секундах) внутри файла `$PREFIX/var/service/multiproxy/run`, затем выполните `bash manage.sh restart-service`.

**macOS:** отредактируйте блок `StartCalendarInterval` внутри `~/Library/LaunchAgents/com.anonymous.multiproxy.plist`, затем выполните:
```bash
launchctl unload ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
launchctl load ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
```

---

## 🎛️ Настройка источников и параметров

Отредактируйте `src/user_settings.py`, чтобы контролировать поведение сборщика:

```python
SOURCE_URLS = [
    "https://t.me/s/your_channel",
    "https://raw.githubusercontent.com/user/repo/main/configs.txt",
]

USE_MAXIMUM_POWER = True   # Получать максимально возможное количество конфигураций
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

После редактирования просто снова запустите `bash run.sh` (или дождитесь следующего запланированного запуска), чтобы применить изменения.

---

## 🧩 Настройка конечной точки Fragment

`xray_fragment_loadbalanced_config.json` применяет продвинутую двухэтапную фрагментацию TLS ClientHello к каждой конфигурации, что может помочь против фильтрации на основе DPI. Все её параметры находятся в `src/fragment_settings.py`:

```python
FRAGMENT_ENABLED = True
FRAGMENT_STAGE_1 = {"packets": "tlshello", "lengths": ["5", "94", "1"], "delays": ["0"], "max_split": "0"}
FRAGMENT_STAGE_2_ENABLED = True
FRAGMENT_STAGE_2 = {"packets": "1-1", "lengths": ["109", "1"], "delays": ["1"], "max_split": "355"}
FRAGMENT_TLS_FINGERPRINT = "unsafe"
FRAGMENT_TLS_CIPHER_SUITES = "TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:..."
```

Измените значения здесь и снова запустите `bash run.sh`, чтобы пересобрать файл с вашими собственными настройками фрагментации.

---

## 🔒 Заметки по безопасности

**Отдавайте предпочтение этим файлам:**
- ✅ `xray_secure_loadbalanced_config.json`
- ✅ `singbox_configs_secure.json`
- ✅ `clash_configs_secure.yaml`

**Избегайте прямого использования этих файлов** (они содержат непротестированные или неотфильтрованные конфигурации):
- ❌ `proxy_configs.txt`
- ❌ `singbox_configs_all.json`
- ❌ `clash_configs_all.yaml`

### Что удаляет фильтр безопасности:
- Конфигурации Shadowsocks с не-AEAD (небезопасными) шифрами
- Конфигурации VMess с устаревшим, ненулевым `alterId`
- Конфигурации VLESS/Trojan без TLS
- Конфигурации с `insecure=true` (отключена проверка сертификата)
- Конфигурации VMess с `security=none`

---

## 🔧 Решение проблем

### Xray не найден
```bash
which xray
```
**Решение:**
```bash
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
```

### Sing-box не найден
```bash
which sing-box
```
**Решение (Termux):**
```bash
pkg install sing-box -y
```
**Решение (Linux):**
```bash
bash <(curl -fsSL https://sing-box.app/install.sh)
```

### Ошибки Python
```bash
source ~/multi-proxy-config-fetcher/venv/bin/activate
pip install -r ~/multi-proxy-config-fetcher/requirements.txt --upgrade
```

### Нет выходных файлов / пайплайн, похоже, прервался на середине
```bash
ls -la ~/multi-proxy-config-fetcher/configs/
tail -100 ~/multi-proxy-config-fetcher/logs/run_*.log
```
Последний лог-файл точно покажет, на каком шаге произошёл сбой.

### Запланированные запуски не выполняются
```bash
# Linux
crontab -l
systemctl status cron

# Termux
sv status multiproxy
```

---

## ❓ Часто задаваемые вопросы

**В: Какой файл конфигурации мне на самом деле использовать?**
Любой файл с суффиксом `_tested` или `_secure` прошёл тесты работоспособности. Для наибольшей уверенности используйте файлы `_secure`, либо `xray_fragment_loadbalanced_config.json`, если вам нужна повышенная устойчивость к блокировкам.

**В: Как часто обновляются конфигурации?**
По умолчанию каждые 12 часов на Linux/Termux, или дважды в день (08:00/20:00) на macOS. См. [Расписание](#-расписание-автоматического-запуска), чтобы изменить это.

**В: Сколько конфигураций собирает система?**
Зависит от `USE_MAXIMUM_POWER` в `src/user_settings.py`. При значении `True` собирается максимально возможное количество из ваших настроенных источников.

**В: Могу ли я добавить свои источники?**
Да — добавьте их в `SOURCE_URLS` в `src/user_settings.py` (см. [Настройка источников и параметров](#-настройка-источников-и-параметров)).

**В: Работает ли это на старых телефонах Android?**
Да, протестировано на Android 7+. Вам нужно установить Termux из **F-Droid**, а не из Google Play (версия из Play Store устарела и больше не поддерживается самой командой Termux).

**В: В чём разница между выходными файлами Xray, Sing-box и Clash?**
- Файлы **Xray** работают с v2rayNG, v2rayN, Nekoray
- Файлы **Sing-box** работают с SFA, Hiddify, NekoBox
- Файлы **Clash/Mihomo** работают с Clash Verge, Mihomo, Clash Meta

Все три генерируются из одного и того же списка прокси и функционально эквивалентны — выбирайте тот, что подходит вашему клиентскому приложению.

**В: Что именно делает вывод Fragment по-другому?**
Он строит ту же сбалансированную конфигурацию Xray, что и `xray_loadbalanced_config.json`, но разбивает TLS-рукопожатие на небольшие фрагменты с задержками, в два этапа. Это может затруднить распознавание соединения системами DPI, блокирующими по паттернам TLS ClientHello.

---

## 🔄 Обновление

```bash
cd ~/multi-proxy-config-fetcher
bash manage.sh update
```

Или вручную:
```bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

---

## 🤝 Вклад в проект

Вклады приветствуются:
1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Отправьте Pull Request

---

## 🙏 Благодарности

- **Команда Xray-core** — высокопроизводительный прокси-движок
- **Команда Sing-box** — универсальный прокси-движок
- **Команда Clash/Mihomo** — современная прокси-платформа
- **Сообщество open source** — поддержка и обратная связь

---

## 📚 Ресурсы

- **Основной репозиторий**: https://github.com/4n0nymou3/multi-proxy-config-fetcher
- **Веб-страница конфигураций**: https://4n0nymou3.github.io/Anonymous-Proxy-Hub/
- **Xray-core**: https://github.com/XTLS/Xray-core
- **Sing-box**: https://sing-box.sagernet.org
- **Clash/Mihomo**: https://github.com/MetaCubeX/mihomo
- **v2rayNG**: https://github.com/2dust/v2rayNG
- **Termux**: https://termux.dev
- **Crontab Guru** (проверка синтаксиса cron): https://crontab.guru

---

## 📄 Лицензия

Лицензия MIT — см. файл [LICENSE](LICENSE) для подробностей.

---

## 📬 Контакты

- **GitHub**: https://github.com/4n0nymou3
- **Twitter/X**: https://x.com/4n0nymou3

---

## ⚡ Быстрый старт для Termux

Для новых пользователей, которые хотят начать немедленно:

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

Затем не забудьте выполнить три критически важных шага Termux:Boot из раздела [Расписание](#-расписание-автоматического-запуска), чтобы автоматические запуски работали после перезагрузки телефона.

---

> 🎉 **Поздравляем!** Ваш сборщик прокси-конфигураций установлен и работает. При любых проблемах проверьте логи с помощью `bash manage.sh logs`.