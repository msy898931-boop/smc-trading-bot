import os
import time
import telebot
from telebot import types

TOKEN = os.environ.get('BOT_TOKEN', '8733597181:AAE9JKx6qazg0oFx8MV7k6xu1ePiSjszNwk')
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

# إنشاء الأزرار التفاعلية الجاهزة
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_start = types.KeyboardButton("🚀 تشغيل البوت")
    btn_smc = types.KeyboardButton("📊 تحليل SMC")
    btn_info = types.KeyboardButton("ℹ️ معلومات الحساب")
    markup.add(btn_start, btn_smc, btn_info)
    return markup

# الاستجابة لأمر /start أو زر التحديث
@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == "🚀 تشغيل البوت")
def send_welcome(message):
    text = (
        "👋 **أهلاً بك في بوت إشارات SMC!**\n\n"
        f"🆔 **معرّف المحادثة (Chat ID):** `{message.chat.id}`\n"
        "🟢 **الحالة:** البوت متصل وجاهز للعمل فوراً.\n\n"
        "اختر من الأزرار في الأسفل للتحكم:"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_keyboard())

# الاستجابة لزر تحليل SMC
@bot.message_handler(commands=['smc'])
@bot.message_handler(func=lambda message: message.text == "📊 تحليل SMC")
def send_smc_info(message):
    text = (
        "🧠 **مفاهيم Smart Money Concepts (SMC):**\n\n"
        "1️⃣ **Order Block (OB):** مناطق تجميع السيولة والمؤسسات المالية.\n"
        "2️⃣ **Fair Value Gap (FVG):** الفجوات السعرية الناتجة عن الزخم السريع.\n"
        "3️⃣ **BOS / CHOCH:** كسر الهيكل وتغير اتجاه السوق."
    )
    bot.send_message(message.chat.id, text, reply_markup=main_keyboard())

# الاستجابة لزر معلومات الحساب
@bot.message_handler(func=lambda message: message.text == "ℹ️ معلومات الحساب")
def send_info(message):
    text = f"👤 **معلوماتك:**\n- **Chat ID:** `{message.chat.id}`\n- **الاسم:** {message.from_user.first_name}"
    bot.send_message(message.chat.id, text, reply_markup=main_keyboard())

# الرد على أي نص آخر
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"استلمت رسالتك: '{message.text}'\nاستخدم الأزرار في الأسفل للتحكم.", reply_markup=main_keyboard())

if __name__ == "__main__":
    # إلغاء أي Webhook قديم لتفادي التعارض
    bot.remove_webhook()
    time.sleep(1)
    print("Bot is polling...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
