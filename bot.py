from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8268233353:AAGD_d6IcNo2qOPeRViLzWJTDwkuQhWGa40"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    await update.message.reply_text(
        f"👋 Привет! Я бот Zhanym 🌹\\n\\n"
        f"Твой Telegram ID:\\n`{telegram_id}`\\n\\n"
        f"Скопируй его и вставь в профиле на сайте!",
        parse_mode='Markdown'
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Бот запущен!")
    app.run_polling()
