import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")
app = Flask(__name__)

@app.route('/')
def home():
    return "SMC Trading Bot is Live & Ready!"

# استقبال التحديثات من تليجرام وتمريرها للبوت
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    return "Unsupported Media Type", 415

# أمر /start
@bot.message_handler(commands=['start'])
def start_cmd(message):
    welcome_text = (
        "📊 **مرحباً بك في بوت تداول SMC** 📊\n\n"
        "البوت يعمل الآن ومربوط بنجاح 24/7.\n"
        f"معرّف المحادثة الخاص بك (Chat ID):\n`{message.chat.id}`\n\n"
        "احفظ هذا الرقم لاستخدامه في إرسال التنبيهات التلقائية."
    )
    bot.reply_to(message, welcome_text)

# أمر /smc
@bot.message_handler(commands=['smc'])
def smc_info(message):
    smc_text = (
        "🧠 **ملخص مفاهيم Smart Money Concepts (SMC):**\n\n"
        "1️⃣ **Order Blocks (OB):** مناطق تجميع العقود للمؤسسات المالية.\n"
        "2️⃣ **Fair Value Gap (FVG):** الفجوات السعرية الناتجة عن الحركة السريعة.\n"
        "3️⃣ **Break of Structure (BOS):** كسر الهيكل لاستمرار الاتجاه.\n"
        "4️⃣ **Change of Character (CHOCH):** تغيير الاتجاه والتحول الهيكلي."
    )
    bot.reply_to(message, smc_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
