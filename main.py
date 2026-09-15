import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "SMC Bot is Active!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and 'chat_id' in data and 'message' in data:
        bot.send_message(data['chat_id'], data['message'], parse_mode="Markdown")
    return "OK", 200

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "مرحباً بك! بوت تنبيهات SMC يعمل بنجاح وجاهز لاستقبال الإشارات.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
