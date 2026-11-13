import os
import threading
from flask import Flask
import telebot

# ফ্লাস্ক সার্ভার (রেন্ডারের পোর্ট রিকোয়ারমেন্ট পূরণের জন্য)
server = Flask(__name__)

@server.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)

# টেলিগ্রাম বট সেটআপ
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! আমাকে যেকোনো ইউটিউব বা সোশ্যাল মিডিয়ার লিংক দিন, আমি ডাউনলোড করে দিচ্ছি।")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        bot.reply_to(message, f"⏳ আপনার লিংকটি প্রসেস করা হচ্ছে...\n\n(ডাউনলোড কাজ চলছে)")
        # এখানে আপনার yt-dlp বা ডাউনলোডার লজিক বসাতে পারেন
    else:
        bot.reply_to(message, "দয়া করে একটি সঠিক লিংক পাঠান।")

if __name__ == "__main__":
    # ব্যাকগ্রাউন্ডে ফ্লাস্ক সার্ভার রান করানো
    t = threading.Thread(target=run_flask)
    t.start()
    
    print("🤖 টেলিগ্রাম বট এবং ওয়েব সার্ভার সফলভাবে চালু হয়েছে...")
    bot.infinity_polling()
