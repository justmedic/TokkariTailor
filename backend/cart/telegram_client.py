# from django.conf import settings
# from telegram import Bot
# from telegram.error import TelegramError


# bot = Bot(token=settings.TELEGRAM_TOKEN)

# def send_telegram_message(message, file_path=None):
#     for chat_id in settings.TELEGRAM_CHAT_ID:
#         try:
#             if file_path:
#                 with open(file_path, 'rb') as file:
#                     bot.send_document(chat_id=chat_id, document=file, caption=message)
#             else:
#                 bot.send_message(chat_id=chat_id, text=message, caption=chat_id)

#         except TelegramError as e:
#             print(f"Ошибка при отправке сообщения в Telegram: {e}")
