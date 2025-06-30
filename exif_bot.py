from telegram.ext import Updater, MessageHandler, Filters
from PIL import Image
from PIL.ExifTags import TAGS
import os

TOKEN = "8107937727:AAEolVgpq4uz5ibqWEGkaVLXgrbYj3OS_AM"

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
    if update.message.photo:
        # Image sent as normal photo
        photo_file = update.message.photo[-1].get_file()
        file_path = f"{photo_file.file_id}.jpg"
    elif update.message.document and update.message.document.mime_type.startswith("image/"):
        # Image sent as file
        photo_file = update.message.document.get_file()
        file_path = update.message.document.file_name
    else:
        update.message.reply_text("❌ Unsupported file type.")
        return

    photo_file.download(file_path)

    try:
        result = extract_exif(file_path)
    except Exception as e:
        result = f"Error reading EXIF: {e}"
    
    update.message.reply_text(f"📸 EXIF Metadata:\n\n{result}")
    os.remove(file_path)

def start_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    # ✅ Handles both compressed photo and uncompressed image file
    dp.add_handler(MessageHandler(Filters.photo | Filters.document.image, handle_photo))
    updater.start_polling()
    print("🤖 Bot is running... Press Ctrl+C to stop.")
    updater.idle()

if __name__ == "__main__":
    start_bot()
