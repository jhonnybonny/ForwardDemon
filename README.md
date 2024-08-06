# Telegram ForwardDemon

Этот проект представляет собой Telegram userbot, который отслеживает новые сообщения, их редактирование и удаление в Telegram-чатах (Супергруппы, группы, личные сообщения). Бот сохраняет сообщения в Redis и отправляет уведомления при удалении или редактировании сообщений. 

## Требования

- Python 3.7 или выше
- [Telethon](https://github.com/LonamiWebs/Telethon) - Python клиент для Telegram API
- Redis

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/jhonnybonny/ForwardDemon.git
    cd ForwardDemon
    ```

2. Установите зависимости:
    ```bash
    pip3 install -r requirements.txt
    ```

3. Запустите Redis с помощью Docker Compose:

    Запустите Redis:

    ```bash
    sudo docker-compose up -d
    ```

## Конфигурация

Вам нужно заменить следующие параметры в скрипте на ваши собственные значения:

- `api_id` и `api_hash` - получить эти значения можно, зарегистрировав приложение на [my.telegram.org](https://my.telegram.org).
- `forward_to_chat_id` - ID чата или канала, куда нужно пересылать сообщения.

## Использование

Запустите скрипт:

```bash
python3 bot.py
```

Запустите скрипт в фоне (я использую pm2):

```bash
sudo pm2 start bot.py --interpreter /usr/bin/python3 --name ForwardDemon
sudo pm2 startup
sudo pm2 save 
