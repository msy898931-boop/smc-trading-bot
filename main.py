import os
import time
import threading
import telebot
from telebot import types
from flask import Flask

# 1. إعداد التليجرام و Flask
TOKEN = os.environ.get('BOT_TOKEN', '8733597181:AAE9JKx6qazg0oFx8MV7k6xu1ePiSjszNwk')
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")
app = Flask(__name__)

# 2. نقطة فحص حياة السيرفر (تمنع Render من إيقاف الخدمة)
@app.route('/')
def home():
    return "Bot is alive and polling continuously!"

# 3. لوحة الأزرار التفاعلية
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_start = types.KeyboardButton("🚀 تشغيل البوت")
    btn_smc = types.KeyboardButton("📊 تحليل SMC")
    btn_info = types.KeyboardButton("ℹ️ معلومات الحساب")
    markup.add(btn_start, btn_smc, btn_info)
    return markup

# 4. معالجة أوامر البوت
@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == "🚀 تشغيل البوت")
def send_welcome(message):
    text = (
        "👋 **أهلاً بك في بوت إشارات SMC!**\n\n"
        f"🆔 **معرّف المحادثة (Chat ID):** `{message.chat.id}`\n"
        "🟢 **الحالة:** البوت متصل ومستقر 100%.\n\n"
        "اختر من الأزرار في الأسفل للتحكم:"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_keyboard())

@bot.message_handler(commands=['smc'])
@bot.message_handler(func=lambda message: message.text == "📊 تحليل SMC")
def send_smc_info(message):
    text = (
        "🧠 **مفاهيم Smart Money Concepts (SMC):**\n\n"
        "1️⃣ **Order Block (OB):** مناطق تجميع السيولة للمؤسسات.\n"
        "2️⃣ **Fair Value Gap (FVG):** الفجوات السعرية الناتجة عن الزخم.\n"
        "3️⃣ **BOS / CHOCH:** كسر الهيكل وتغير الاتجاه."
    )
    bot.send_message(message.chat.id, text, reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: message.text == "ℹ️ معلومات الحساب")
def send_info(message):
    text = f"👤 **معلوماتك:**\n- **Chat ID:** `{message.chat.id}`\n- **الاسم:** {message.from_user.first_name}"
    bot.send_message(message.chat.id, text, reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"استلمت رسالتك: '{message.text}'", reply_markup=main_keyboard())

# 5. تشغيل البوت في الخلفية (Background Thread)
def start_bot_polling():
    bot.remove_webhook()
    time.sleep(1)
    print("Starting bot polling...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    # تشغيل البوت في Thread منفصل
    t = threading.Thread(target=start_bot_polling)
    t.daemon = True
    t.start()
    
    # تشغيل خادم Flask لربط المنفذ مع Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
