# just
import os
import requests
from telegram import Update, ReplyKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# START komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🔍 Qidiruv", "📂 Fayl yuborish"],
        ["📤 Fayl yuklash", "ℹ️ Yordam"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Salom! Men sizga quyidagilarni taklif qilaman:", reply_markup=reply_markup)

# Qidiruv funksiyasi
async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Qidiruv so'zini yuboring:")
    context.user_data["awaiting_search"] = True

# Fayl yuborish (botdan foydalanuvchiga)
async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = "sample.txt"
    if os.path.exists(file_path):
        await update.message.reply_text("📎 Mana sizga fayl:")
        with open(file_path, 'rb') as f:
            await update.message.reply_document(InputFile(f, filename="sample.txt"))
    else:
        await update.message.reply_text("❌ Fayl topilmadi.")

# Fayl yuklash (foydalanuvchidan botga)
async def handle_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📤 Iltimos, yuklamoqchi bo‘lgan faylingizni yuboring.")

# Yuklangan faylni saqlash
async def save_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if document:
        file = await context.bot.get_file(document.file_id)
        file_path = f"downloads/{document.file_name}"
        os.makedirs("downloads", exist_ok=True)
        await file.download_to_drive(file_path)
        await update.message.reply_text(f"✅ Fayl saqlandi: {file_path}")
    else:
        await update.message.reply_text("❌ Hech qanday fayl topilmadi.")

# Xabarlarni boshqarish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if context.user_data.get("awaiting_search"):
        query = text.replace(" ", "+")
        url = f"https://www.google.com/search?q={query}"
        await update.message.reply_text(f"🔎 Qidiruv natijasi: {url}")
        context.user_data["awaiting_search"] = False
    elif text == "🔍 Qidiruv":
        await handle_search(update, context)
    elif text == "📂 Fayl yuborish":
        await send_file(update, context)
    elif text == "📤 Fayl yuklash":
        await handle_upload(update, context)
    elif text == "ℹ️ Yordam":
        await update.message.reply_text("🧾 Bot orqali siz fayl yuborishingiz, fayl yuklashingiz yoki internetda qidiruv qilishingiz mumkin.")
    else:
        await update.message.reply_text("🤖 Men bu buyruqni tushunmadim.")

# Botni ishga tushirish
app = ApplicationBuilder().token("7806141272:AAGdCFWoqSmePehBFheGVEeGoAEQDjCVxZI").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Document.ALL, save_file))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✅ Bot ishga tushdi!")
app.run_polling()
