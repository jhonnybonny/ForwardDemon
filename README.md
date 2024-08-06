# Telegram ForwardDemon

This project is a Telegram userbot that tracks new messages, edits, and deletions in Telegram chats (supergroups, groups, and personal messages). The bot saves messages in Redis and sends notifications when messages are deleted or edited.

## Requirements

- Python 3.7 or higher
- [Telethon](https://github.com/LonamiWebs/Telethon) - A Python client for the Telegram API
- Redis

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/jhonnybonny/ForwardDemon.git
    cd ForwardDemon
    ```

2. Install the dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```

3. Start Redis using Docker Compose:

    Start Redis:

    ```bash
    sudo docker-compose up -d
    ```

## Configuration

You need to replace the following parameters in the script with your own values:

- `api_id` and `api_hash` - you can get these values by registering an application on [my.telegram.org](https://my.telegram.org).
- `forward_to_chat_id` - the ID of the chat or channel where you want to forward messages.

## Usage

Run the script:

```bash
python3 bot.py
```


Run the script in the background (I use pm2):

```bash
sudo pm2 start bot.py --interpreter /usr/bin/python3 --name ForwardDemon
sudo pm2 startup
sudo pm2 save 
```

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
