# Настройка Telegram Mini App с постоянным Cloudflare Tunnel

## Шаг 0. Предварительные условия

Убедись, что на компьютере установлены:

* Python (3.10+)
* Node.js и npm (для альтернатив, если решишь использовать localtunnel)
* Cloudflared (скачано с официального сайта)
* Telegram Bot (бот создан в BotFather)
* Зарегистрирован аккаунт на Cloudflare

---

## Шаг 1. Создание Mini App в BotFather

1. Открой Telegram → BotFather → выбери своего бота.
2. В разделе **Mini Apps** → **Main App** → пока оставляем пустым (ссылка появится позже).

---

## Шаг 2. Подготовка локального проекта

1. Создай папку для веб-приложения (если ещё нет):

```cmd
C:\Taxi_bot\webapp
```

2. В эту папку положи `index.html` или другой frontend-код мини-приложения.

3. Запусти локальный сервер:

```cmd
cd C:\Taxi_bot\webapp
python -m http.server 8000
```

* Проверка: [http://localhost:8000](http://localhost:8000) должна открываться в браузере.

---

## Шаг 3. Установка и проверка Cloudflared

1. Скачай Windows-версию: `cloudflared-windows-amd64.exe`.
2. Проверим версию:

```cmd
C:\cloudflared\cloudflared-windows-amd64.exe version
```

* Должен быть вывод с версией, например: `cloudflared version 2025.11.1`.

---

## Шаг 4. Создание постоянного туннеля в Cloudflare

1. Войдите в аккаунт Cloudflare и авторизуйся:

```cmd
C:\cloudflared\cloudflared-windows-amd64.exe login
```

2. После открытия браузера, выбери домен (можно создать бесплатный поддомен `trycloudflare.com`).
3. Создай именованный туннель:

```cmd
C:\cloudflared\cloudflared-windows-amd64.exe tunnel create taxi_tunnel
```

* Запомни сгенерированное имя туннеля и ID.

4. Создай конфигурационный файл `config.yml` в папке `C:\cloudflared\`:

```yaml
tunnel: taxi_tunnel
credentials-file: C:\Users\пк\.cloudflared\<tunnel-id>.json

ingress:
  - hostname: taxiapp.trycloudflare.com
    service: http://localhost:8000
  - service: http_status:404
```

5. Запусти туннель:

```cmd
C:\cloudflared\cloudflared-windows-amd64.exe tunnel run taxi_tunnel
```

* Теперь URL `https://taxiapp.trycloudflare.com` будет постоянным.

---

## Шаг 5. Настройка DNS в Cloudflare

1. В Cloudflare → домен → DNS.
2. Добавь CNAME:

   * **Name:** taxiapp
   * **Target:** `your-tunnel-id.cfargotunnel.com`
3. Подтверди, что статус проксирования включен (оранжевый облачок).

---

## Шаг 6. Подключение Mini App в BotFather

1. В Telegram → BotFather → Mini Apps → Main App → вставь постоянный URL `https://taxiapp.trycloudflare.com`.
2. Сохраняем.

---

## Шаг 7. Открытие Mini App в Telegram

1. Открой чат с ботом.
2. В левом нижнем углу должна появиться кнопка **Mini App**.
3. Нажми → откроется твоя локальная страница через Cloudflare Tunnel.

---

## Шаг 8. Алгоритм повторного запуска проекта

1. Поднимаем локальный сервер:

```cmd
cd C:\Taxi_bot\webapp
python -m http.server 8000
```

2. Запускаем постоянный Cloudflare Tunnel:

```cmd
C:\cloudflared\cloudflared-windows-amd64.exe tunnel run taxi_tunnel
```

3. Mini App URL не меняется, обновлять в BotFather не нужно.

---

### ⚡ Примечания

* Для разработки можно использовать Quick Tunnel (`trycloudflare.com`), но URL меняется при каждом запуске.
* Для продакшена используем именованный туннель с постоянным поддоменом.
* Все настройки HTTPS и проксирования обрабатывает Cloudflare автоматически.
* Локальный сервер (`python -m http.server`) должен быть запущен при открытии Mini App.




# Настройка Telegram Mini App с использованием Cloudflare Quick Tunnel (постоянно меняется ссылка)


---

## 1. Подготовка проекта

1. Убедитесь, что ваш бот работает локально.
2. В папке проекта (`C:\Taxi_bot`) должна быть папка `webapp`, где хранится ваш `index.html` (или другой фронтенд для мини-приложения).
3. Убедитесь, что Python установлен и активирована виртуальная среда (`venv`).

Пример запуска локального сервера:

```powershell
cd C:\Taxi_bot\webapp
python -m http.server 8000
```

Откройте в браузере: [http://localhost:8000](http://localhost:8000) и убедитесь, что страница загружается.

---

## 2. Установка Cloudflared

1. Скачайте последнюю версию для Windows: [cloudflared-windows-amd64](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation) (если ссылка недоступна, скачайте с официального сайта Cloudflare).
2. Распакуйте в папку, например `C:\cloudflared`
3. Проверьте работоспособность:

```cmd
C:\cloudflared\cloudflared-windows-amd64.exe version
```

---

## 3. Запуск Quick Tunnel

1. В командной строке откройте папку с cloudflared:

```cmd
cd C:\cloudflared
```

2. Запустите Quick Tunnel, указывая URL вашего локального сервера:

```cmd
cloudflared-windows-amd64.exe tunnel --url http://localhost:8000
```

3. После запуска в консоли появится строка с публичным URL, например:

```
https://structured-commands-corresponding-implied.trycloudflare.com
```

> Этот URL меняется при каждом новом запуске Quick Tunnel.

4. Откройте URL в браузере, убедитесь, что открывается ваша локальная страница.

---

## 4. Настройка Mini App в Telegram BotFather

1. Откройте BotFather и выберите вашего бота.
2. В настройках бота найдите `Mini Apps` → `Main App URL`.
3. Вставьте URL Quick Tunnel, полученный на шаге 3.
4. Сохраните настройки.

> ⚠️ При каждом перезапуске Quick Tunnel нужно обновлять URL в BotFather.

---

## 5. Перезапуск проекта

1. Остановите текущий локальный сервер и tunnel.
2. Запустите сервер снова:

```powershell
cd C:\Taxi_bot\webapp
python -m http.server 8000
```

3. Запустите Quick Tunnel снова:

```cmd
cd C:\cloudflared
cloudflared-windows-amd64.exe tunnel --url http://localhost:8000
```

4. Скопируйте новый URL и обновите его в BotFather (`Mini Apps → Main App URL`).

---

## 6. Разработка Mini App

* Теперь ваш мини-приложение доступно через Telegram, при нажатии кнопки `Open` слева в чате бота.
* Можно писать фронтенд-логику на HTML/JS/CSS, обновлять файлы в `webapp`, перезапускать сервер и tunnel.

> ⚠️ Помните: Quick Tunnel предназначен только для разработки и тестирования, для продакшн нужно создавать постоянный Tunnel через Cloudflare с аккаунтом.

---

**Конец инструкции.**
