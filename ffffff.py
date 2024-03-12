# from telegram import Bot, Update
# from telegram.ext import Updater, CommandHandler, CallbackContext

# def start(update: Update, context: CallbackContext) -> None:
#     chat_id = update.effective_chat.id
#     context.bot.send_message(chat_id=chat_id, text=f"Ваш Telegram ID: {chat_id}")

# def main():
#     TOKEN = ''  # Замените YOUR_BOT_TOKEN на ваш токен от BotFather

#     bot = Bot(TOKEN)
#     updater = Updater(bot=bot)

#     dp = updater.dispatcher
#     dp.add_handler(CommandHandler("start", start))

#     updater.start_polling()
#     updater.idle()

# if __name__ == '__main__':
#     main()
