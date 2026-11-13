import os
import telebot

# বটের টোকেন এনভায়রনমেন্ট থেকে রিড করবে
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! আমাকে যেকোনো ভিডিওর লিংক দিন, আমি ডাউনলোড করার চেষ্টা করব।")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "t.me" in url or "http" in url:
        bot.reply_to(message, f"⏳ আপনার লিংকটি প্রসেস করা হচ্ছে: {url}\n\n(ডাউনলোড কাজ চলছে...)")
    else:
        bot.reply_to(message, "দয়া করে একটি সঠিক লিংক পাঠান।")

if __name__ == "__main__":
    print("🤖 টেলিগ্রাম বট সফলভাবে চালু হয়েছে...")
    bot.infinity_polling()
