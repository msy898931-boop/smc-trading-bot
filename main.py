import os
import time
import threading
import pandas as pd
import yfinance as yf
import telebot
from flask import Flask, request

# 1. إعدادات التليجرام والسيرفر
TOKEN = os.environ.get('BOT_TOKEN', '8733597181:AAE9JKx6qazg0oFx8MV7k6xu1ePiSjszNwk')
CHAT_ID = "933571066"  # Chat ID الخاص بك

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")
app = Flask(__name__)

# 2. الصفحة الرئيسية للسيرفر
@app.route('/')
def home():
    return "SMC Trading Bot is Active & Running Fully Automated!"

# 3. معالجة الـ Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    return "Unsupported", 415

# 4. أوامر البوت المباشرة
@bot.message_handler(commands=['start'])
def start_cmd(message):
    text = (
        "👋 **أهلاً بك في بوت إشارات SMC الآلي!**\n\n"
        f"🆔 **Chat ID:** `{message.chat.id}`\n\n"
        "🟢 البوت يعمل الآن تلقائياً في الخلفية ويفحص الأسواق (الذهب والعملات) لإرسال التنبيهات مباشرة."
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['smc'])
def smc_cmd(message):
    text = (
        "🧠 **مفاهيم SMC المعتمدة في التحليل الآلي:**\n\n"
        "1️⃣ **FVG (Fair Value Gap):** الفجوات السعرية الناتجة عن الزخم القوي.\n"
        "2️⃣ **Order Block (OB):** مناطق تجميع السيولة للمؤسسات المالية."
    )
    bot.reply_to(message, text)

# 5. خوارزمية الفحص الآلي للأسواق (SMC Scanner)
def analyze_smc(symbol_name, ticker_symbol):
    try:
        # جلب أحدث بيانات السعر (فريم 15 دقيقة)
        df = yf.download(tickers=ticker_symbol, period="2d", interval="15m", progress=False)
        if len(df) < 5:
            return

        # تنظيف الأعمدة
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        c_close = df['Close'].iloc[-1]
        
        # فحص فجوة FVG الشرائية (Bullish FVG)
        # الشمعة الأولى أدنى سعرها أعلى من أعلى سعر للشمعة الثالثة
        high_3 = df['High'].iloc[-3]
        low_1 = df['Low'].iloc[-1]
        
        if low_1 > high_3:
            gap_size = round(low_1 - high_3, 2)
            alert_msg = (
                f"🚨 **إشارة SMC جديدة (Fair Value Gap)!**\n\n"
                f"📌 **الزوج:** {symbol_name}\n"
                f"📈 **النوع:** فجوة شرائية (Bullish FVG)\n"
                f"💰 **السعر الحالي:** {round(c_close, 2)}\n"
                f"📏 **حجم الفجوة:** {gap_size}\n"
                f"⏰ **التوقيت:** تلقائي من السيرفر"
            )
            bot.send_message(CHAT_ID, alert_msg)
    except Exception as e:
        print(f"Error scanning {symbol_name}: {e}")

# 6. المراقبة المستمرة (تشتغل كل 5 دقائق)
def background_scanner():
    symbols = {
        "الذهب (XAU/USD)": "GC=F",
        "اليورو/دولار (EUR/USD)": "EURUSD=X",
        "الباوند/دولار (GBP/USD)": "GBPUSD=X"
    }
    
    # انتظار دقيقة واحدة عند الإقلاع
    time.sleep(60)
    
    while True:
        for name, ticker in symbols.items():
            analyze_smc(name, ticker)
            time.sleep(5)  # فاصل بسيط بين الأزواج
            
        time.sleep(300)  # إعادة الفحص كل 5 دقائق

# تشغيل الفحص في الخلفية
thread = threading.Thread(target=background_scanner, daemon=True)
thread.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
