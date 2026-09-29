import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")

app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "OK - Bot is Alive"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

# شغل الموقع في خيط براهو
Thread(target=run_web, daemon=True).start()

async def start(update, context):
    await update.message.reply_text("البوت صاحي 24 ساعة ✅")

async def handle(update, context):
    text = update.message.text or ""
    if "المتواجدون" in text or "المتصلون" in text:
        await update.message.reply_text("👥 المتصلون الآن:\n🟢 انت متصل الآن")

bot_app = ApplicationBuilder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot starting...")
bot_app.run_polling()
