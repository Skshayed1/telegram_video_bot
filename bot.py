import os
import logging
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from ffmpeg_command import run_ffmpeg

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
user_videos = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 স্বাগতম! আপনি শুধু দুইটি ভিডিও পাঠান:
"
        "1️⃣ একটি আপনার মেইন ভিডিও
"
        "2️⃣ একটি আপনার 'মাই ভিডিও'

"
        "আমি আপনার জন্য অসাধারণ কিছু তৈরি করে পাঠিয়ে দেব!"
    )

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    file = update.message.video or update.message.document
    if not file:
        await update.message.reply_text("⚠️ দয়া করে একটি বৈধ ভিডিও পাঠান।")
        return

    file_id = str(uuid.uuid4())[:8]
    file_path = f"{user_id}_{file_id}.mp4"
    new_file = await file.get_file()
    await new_file.download_to_drive(file_path)

    user_videos.setdefault(user_id, []).append(file_path)

    if len(user_videos[user_id]) == 2:
        await update.message.reply_text("⏳ আপনার ভিডিও প্রসেস করা হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...")
        input1, input2 = user_videos[user_id]
        output_path = f"{user_id}_output.mp4"
        try:
            run_ffmpeg(input1, input2, output_path)
            await update.message.reply_text("✅ প্রসেসিং সম্পন্ন! নিচে আপনার ভিডিও:")
            await update.message.reply_video(video=open(output_path, 'rb'))
        except Exception as e:
            await update.message.reply_text(f"❌ সমস্যা হয়েছে: {e}")
        finally:
            for path in user_videos[user_id]:
                if os.path.exists(path):
                    os.remove(path)
            if os.path.exists(output_path):
                os.remove(output_path)
            user_videos[user_id] = []
    else:
        await update.message.reply_text("📥 একটি ভিডিও পেয়েছি! এখন আরেকটি পাঠান প্রসেসিং শুরু করার জন্য।")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))

if __name__ == "__main__":
    app.run_polling()
