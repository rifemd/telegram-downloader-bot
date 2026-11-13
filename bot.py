import os
import threading
from flask import Flask
import telebot
import yt_dlp

# ফ্লাস্ক সার্ভার (রেন্ডার ২৪ ঘণ্টা সচল রাখার জন্য)
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
    bot.reply_to(message, "স্বাগতম! আমাকে যেকোনো ইউটিউব বা ভিডিও লিংক দিন, আমি ডাউনলোড করে দিচ্ছি।")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if "http" not in url:
        bot.reply_to(message, "দয়া করে একটি সঠিক লিংক পাঠান।")
        return

    msg = bot.reply_to(message, "⏳ ভিডিও ডাউনলোড হচ্ছে, একটু অপেক্ষা করুন...")

    output_template = "video.mp4"
    
    # আগের কোনো ফাইল থাকলে ডিলিট করে নেওয়া
    if os.path.exists(output_template):
        os.remove(output_template)

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': output_template,
        'max_filesize': 50 * 1024 * 1024, # ফ্রি সার্ভারের জন্য ৫০ মেগাবাইটের মধ্যে সীমাবদ্ধ রাখা ভালো
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if os.path.exists(output_template):
            with open(output_template, 'rb') as vid:
                bot.send_video(message.chat.id, vid, caption="✅ আপনার ভিডিও সফলভাবে ডাউনলোড হয়েছে!")
            os.remove(output_template)
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ ভিডিও ডাউনলোড করা সম্ভব হয়নি।", message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ ত্রুটি ঘটেছে:\n{str(e)}", message.chat.id, msg.message_id)
        if os.path.exists(output_template):
            os.remove(output_template)

if __name__ == "__main__":
    # ব্যাকগ্রাউন্ডে ফ্লাস্ক সার্ভার চালু করা
    t = threading.Thread(target=run_flask)
    t.start()
    
    print("🤖 ফুল-ফাংশনাল ডাউনলোডার বট চালু হয়েছে...")
    bot.infinity_polling()
