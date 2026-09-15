import os
import time
import threading
import telebot
from telebot import types
from flask import Flask

TOKEN = os.environ.get('BOT_TOKEN', '8733597181:AAE9JKx6qazg0oFx8MV7k6xu1ePiSjszNwk')
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_start = types.KeyboardButton("🚀 تشغيل البوت")
    btn_smc = types.KeyboardButton("📊 تحليل SMC")
    btn_info = types.KeyboardButton("ℹ️ معلومات الحساب")
    markup.add(btn_start, btn_smc, btn_info)
    return markup

@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == "🚀 تشغيل البوت")
def send_welcome(message):
    text = f"👋 **أهلاً بك!**\n\n🆔 **Chat ID:** `{message.chat.id}`\n🟢 البوت يعمل ومستقر الآن."
    bot.send_message(message.chat.id, text, reply_markup=main_keyboard())

@bot.message_handler(commands=['smc'])
@bot.message_handler(func=lambda message: message.text == "📊 تحليل SMC")
def send_smc_info(message):
    text = "🧠 **مفاهيم SMC:**\n- Order Block\n- Fair Value Gap (FVG)\n- BOS / CHOCH"
    bot.send_message(message.chat.id, text, reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: message.text == "ℹ️ معلومات الحساب")
def send_info(message):
    text = f"👤 **معلوماتك:**\n- Chat ID: `{message.chat.id}`"
    bot.send_message(message.chat.id, text, reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"استلمت: '{message.text}'", reply_markup=main_keyboard())

def start_polling():
    bot.remove_webhook()
    time.sleep(1)
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    t = threading.Thread(target=start_polling)
    t.daemon = True
    t.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
