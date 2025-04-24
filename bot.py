import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Kirim link video kamu dari YouTube, TikTok, IG, atau Facebook ya!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id

    await update.message.reply_text("⏳ Sabar ya sayangg . . .")

    # Buat folder download
    download_dir = "downloads"
    os.makedirs(download_dir, exist_ok=True)

    # Konfigurasi yt-dlp + aria2c
    ydl_opts = {
        'outtmpl': f'{download_dir}/%(title).70s.%(ext)s',
        'format': 'mp4/best',
        'noplaylist': True,
        'quiet': True,
        'external_downloader': 'aria2c',
        'external_downloader_args': ['-x', '16', '-k', '1M'],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Kirim video ke user
        with open(filename, 'rb') as video_file:
            await context.bot.send_video(chat_id=chat_id, video=video_file)

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text("❌ Yah gagal, pastiin linknya benar yaa . . . ")

if __name__ == '__main__':
    from dotenv import load_dotenv
    import asyncio

    load_dotenv()
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Token dari @BotFather

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🌀 Di proses . . .")
    asyncio.run(app.run_polling())