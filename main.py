import os
import time
import telebot
from flask import Flask, request

# TOKEN و Chat ID الخاص بك
TOKEN = os.environ.get('BOT_TOKEN', '8733597181:AAE9JKx6qazg0oFx8MV7k6xu1ePiSjszNwk')
CHAT_ID = "933571066"

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")
app = Flask(__name__)

@app.route('/')
def home():
    return "SMC Trading Bot is Active & Ready!"

# نقطة استقبال رسائل التليجرام مباشرة عبر Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    return "Unsupported", 415

# أمر /start
@bot.message_handler(commands=['start'])
def start_cmd(message):
    text = (
        "👋 **أهلاً بك في بوت إشارات SMC!**\n\n"
        f"🆔 **معرّف المحادثة (Chat ID):** `{message.chat.id}`\n\n"
        "🟢 البوت يعمل الآن بنجاح ومستعد للتواصل معك 24/7."
    )
    bot.reply_to(message, text)

# أمر /smc
@bot.message_handler(commands=['smc'])
def smc_cmd(message):
    text = (
        "🧠 **ملخص مفاهيم Smart Money Concepts (SMC):**\n\n"
        "1️⃣ **Order Block (OB):** مناطق تجميع السيولة والمؤسسات المالية.\n"
        "2️⃣ **Fair Value Gap (FVG):** الفجوات السعرية الناتجة عن الزخم السريع.\n"
        "3️⃣ **BOS / CHOCH:** كسر الهيكل وتغير اتجاه السوق."
    )
    bot.reply_to(message, text)

# رد على أي رسالة أخرى
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"وصلت رسالتك: '{message.text}'\nاستخدم الأمر /smc للتحليل.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
