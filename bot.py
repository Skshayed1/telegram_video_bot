import os
import logging
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from ffmpeg_command import run_ffmpeg

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

# Dictionary to store user video uploads
user_videos = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "স্বাগতম! শুধু ২টি ভিডিও পাঠাও। একটি তোমার মেইন ভিডিও এবং অন্যটি 'মাই ভিডিও' হিসেবে কাজ করবে। আমি বাকি কাজ করবো!"
    )

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    file = update.message.video or update.message.document
    if not file:
        await update.message.reply_text("একটি ভিডিও পাঠাও। আমি অপেক্ষায় আছি আরেকটির জন্য।")
        return

    # Save video file with unique name
    file_id = str(uuid.uuid4())[:8]
    file_path = f"{user_id}_{file_id}.mp4"
    new_file = await file.get_file()
    await new_file.download_to_drive(file_path)

    user_videos.setdefault(user_id, []).append(file_path)

    if len(user_videos[user_id]) == 2:
        await update.message.reply_text("ভিডিও প্রসেসিং শুরু হচ্ছে...")
        input1, input2 = user_videos[user_id]
        output_path = f"{user_id}_output.mp4"

        try:
            run_ffmpeg(input1, input2, output_path)
            await update.message.reply_video(video=open(output_path, 'rb'))
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")
        finally:
            # Clean up
            for path in user_videos[user_id]:
                if os.path.exists(path):
                    os.remove(path)
            if os.path.exists(output_path):
                os.remove(output_path)
            user_videos[user_id] = []
    else:
        await update.message.reply_text("ধন্যবাদ! এখন আরেকটি ভিডিও পাঠাও প্রসেসিং শুরু করার জন্য।")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))

if __name__ == "__main__":
    app.run_polling()
