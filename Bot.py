import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import threading
from flask import Flask

# --- Telegram bot ---
TOKEN = "ТВОЙ_ТОКЕН_ОТСЮДА"

logging.basicConfig(level=logging.INFO)

app_bot = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает на Render!")

app_bot.add_handler(CommandHandler("start", start))

def run_bot():
    asyncio.run(app_bot.run_polling())

# --- Flask для Render ---
app = Flask(__name__)

@app.route("/
