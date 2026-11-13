import os
from pyrogram import Client, filters

# রেন্ডার বা ক্লাউডের এনভায়রনমেন্ট থেকে ভেরিয়েবলগুলো অটোমেটিক রিড করবে
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ক্লাউড ক্লায়েন্ট ইনিশিয়ালাইজ করা
app = Client(
    "my_bot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.text)
async def downloader_handler(client, message):
    url = message.text
    if not url:
        return

    await message.reply("⏳ লিংক প্রসেস করা হচ্ছে...")

    try:
        # Pyrogram এর মাধ্যমে যেকোনো পাবলিক বা রেস্ট্রিক্টেড লিংক হ্যান্ডেল করার লজিক
        downloaded_file = await client.download_media(url)
        if downloaded_file:
            await client.send_document(chat_id=message.chat.id, document=downloaded_file)
            os.remove(downloaded_file) # সার্ভার ক্লিন রাখার জন্য ফাইল ডিলিট
        else:
            await message.reply("❌ ফাইলটি ডাউনলোড করা সম্ভব হয়নি।")
    except Exception as e:
        await message.reply(f"❌ এরর এসেছে:\n{str(e)}")

if __name__ == "__main__":
    print("🤖 ক্লাউড বট চালু হচ্ছে...")
    app.run()
