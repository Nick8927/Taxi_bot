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
