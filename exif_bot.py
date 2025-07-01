from telegram.ext import Updater, MessageHandler, Filters
from PIL import Image
from PIL.ExifTags import TAGS
import os

# Get bot token from environment variable
TOKEN = os.getenv("BOT_TOKEN")

def extract_exif(image_path):
    image = Image.open(image_path)
    exifdata = image._getexif()
    if not exifdata:
        return "❌ No EXIF data found."
    
    result = []
    for tag_id, value in exifdata.items():
        tag = TAGS.get(tag_id, tag_id)
        result.append(f"{tag}: {value}")
    
    return "\n".join(result)

def handle_photo(update, context):
    photo_file = update.message.photo[-1].get_file()
    file_path = f"{photo_file.file_id}.jpg"
    photo_file.download(file_path)

    try:
        result = extract_exif(file_path)
    except Exception as e:
        result = f"Error reading EXIF: {e}"
    
    update.message.reply_text(f"📸 EXIF Metadata:\n\n{result}")
    os.remove(file_path)

def start_bot():
    if not TOKEN:
        print("❌ BOT_TOKEN environment variable not set!")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    updater.start_polling()
    print("🤖 Bot is running... Press Ctrl+C to stop.")
    updater.idle()

if __name__ == "__main__":
    start_bot()
