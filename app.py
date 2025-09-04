import os
from flask import Flask, request, abort
import telebot
import requests

# ==== ТВОЙ ТОКЕН (как просил — вписан в код) ====
TOKEN = "7549538669:AAF8bFuV0TjQx9KEErnsBF50KtNQZ1xs5_c"
# ==== Укажи свой домен Render (без / в конце) ====
BASE_URL = "https://telega-bot-f5zq.onrender.com"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Хендлеры бота
@bot.message_handler(commands=['start', 'help'])
def cmd_start(message):
    bot.send_message(message.chat.id, "Я на Render и работаю по вебхуку. Команда /ping — проверка.")

@bot.message_handler(commands=['ping'])
def cmd_ping(message):
    bot.reply_to(message, "pong ✅")

# Сервисные эндпоинты
@app.get("/")
def root():
    return "OK", 200

@app.get("/health")
def health():
    return "healthy", 200

# Вебхук — Telegram будет слать POST сюда
@app.post(f"/{TOKEN}")
def receive_update():
    if request.headers.get("content-type") == "application/json":
        update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
        bot.process_new_updates([update])
        return "", 200
    abort(403)

def set_webhook():
    url = f"{BASE_URL}/{TOKEN}"
    try:
        r = requests.get(
            f"https://api.telegram.org/bot{TOKEN}/setWebhook",
            params={"url": url, "drop_pending_updates": "true"},
            timeout=10,
        )
        print("setWebhook ->", r.text)
    except Exception as e:
        print("setWebhook error:", e)

if __name__ == "__main__":
    # Локальный запуск (на Render всё равно стартует gunicorn из Procfile)
    set_webhook()
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
