from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters
import os

TOKEN = "ТВОЙ_ТОКЕН"
bot = Bot(token=TOKEN)

app = Flask(__name__)

# Диспетчер для обработки апдейтов
dispatcher = Dispatcher(bot, None, workers=0)

# Обработчик сообщений
def echo(update: Update, context):
    update.message.reply_text(f"Ты написал: {update.message.text}")

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok", 200

@app.route("/")
def index():
    return "Бот работает!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
