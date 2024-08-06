import logging
import redis
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError, UserNotParticipantError
from telethon.utils import get_display_name

# Устанавливаем логирование
logging.basicConfig(level=logging.INFO)

# Конфигурация Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6666
REDIS_PASSWORD = 'TG_-WATCHER-_B0T'

# Создаём клиент Redis
redis_client = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

# Замените 'YOUR_API_ID' и 'YOUR_API_HASH' на ваши значения
api_id = 'XXXXXXX'
api_hash = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
# Замените 'CHAT_ID_WHERE_MESSAGES_WILL_BE_FORWARDED' на ID чата или канала, куда нужно пересылать сообщения
forward_to_chat_id = XXXXXXXXXXXXXXXXXX

# Создаём клиент
client = TelegramClient('userbot', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        chat_id = event.chat_id or event.message.peer_id.user_id or event.message.peer_id.channel_id
        message_id = event.message.id
        sender_id = event.message.sender_id

        logging.info(f"New message received: chat_id={chat_id}, message_id={message_id}, sender_id={sender_id}")

        sender = await event.get_sender()
        sender_name = get_display_name(sender)

        # Сохраняем сообщение и информацию о пользователе в Redis
        redis_client.set(f"message:{message_id}:original", event.message.message)
        redis_client.set(f"message:{message_id}", event.message.message)
        redis_client.set(f"message:{message_id}:sender", sender_name)
        saved_message = redis_client.get(f"message:{message_id}")
        logging.info(f"Message saved in Redis: {saved_message}")

        if sender_id != await client.get_peer_id(forward_to_chat_id):
            try:
                await client.forward_messages(forward_to_chat_id, event.message)
                logging.info(f"Message forwarded: chat_id={chat_id}, message_id={message_id}")
            except FloodWaitError as e:
                logging.warning(f"FloodWaitError: {e}")
            except UserNotParticipantError as e:
                logging.warning(f"UserNotParticipantError: {e}")
            except Exception as e:
                logging.error(f"Error while forwarding message: {e}")

    except Exception as e:
        logging.error(f"Error in handler: {e}")

@client.on(events.MessageDeleted())
async def delete_handler(event):
    try:
        for msg_id in event.deleted_ids:
            cache_key = f"message:{msg_id}:original"
            sender_key = f"message:{msg_id}:sender"
            logging.info(f"Trying to get message with key: {cache_key}")
            original_message = redis_client.get(cache_key)
            sender_name = redis_client.get(sender_key)
            logging.info(f"Fetched message from Redis: {original_message}")

            if original_message and sender_name:
                try:
                    await client.send_message(
                        forward_to_chat_id,
                        f'<b>Сообщение с ID <a href="tg://openmessage?chat_id={msg_id}&message_id={msg_id}">{msg_id}</a> было удалено.</b>\n\n'
                        f"<b>Отправитель:</b> {sender_name}\n\n"
                        f"<b>Удаленное сообщение:</b>\n{original_message}",
                        parse_mode='html'
                    )
                    logging.info(f"Message deleted: message_id={msg_id}")

                    redis_client.delete(cache_key)
                    redis_client.delete(sender_key)
                except Exception as e:
                    logging.error(f"Error while sending delete notification: {e}")
            else:
                logging.info(f"Message with ID {msg_id} not found in Redis")

    except Exception as e:
        logging.error(f"Error in delete_handler: {e}")

@client.on(events.MessageEdited())
async def edit_handler(event):
    try:
        chat_id = event.chat_id or event.message.peer_id.user_id or event.message.peer_id.channel_id
        message_id = event.message.id

        original_cache_key = f"message:{message_id}:original"
        edited_cache_key = f"message:{message_id}"
        logging.info(f"Trying to get message with key: {original_cache_key}")
        original_message_text = redis_client.get(original_cache_key)
        logging.info(f"Fetched message from Redis: {original_message_text}")

        if not original_message_text:
            logging.info(f"Message with ID {message_id} not found in Redis")
            return

        if original_message_text == event.message.message:
            return

        try:
            chat_entity = await client.get_entity(chat_id)
            username = ""
            if hasattr(chat_entity, 'username') and chat_entity.username:
                username = f"@{chat_entity.username}"
            elif hasattr(chat_entity, 'title'):
                username = chat_entity.title

            await client.send_message(
                forward_to_chat_id,
                f'<b>Изменение <a href="tg://openmessage?chat_id={chat_id}&message_id={message_id}">{get_display_name(chat_entity)} {username}</a> '
                f'({message_id} in {chat_id})</b>\n\n'
                "<b>Оригинал:</b>\n"
                f"{original_message_text}\n<b>----------</b>\n"
                "<b>Изменено:</b>\n"
                f"{event.message.message}",
                parse_mode='html'
            )
            logging.info(f"Message edited: message_id={message_id}")

            redis_client.set(edited_cache_key, event.message.message)
        except Exception as e:
            logging.error(f"Error while sending edit notification: {e}")

    except Exception as e:
        logging.error(f"Error in edit_handler: {e}")

async def main():
    # Запуск клиента
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())