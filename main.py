import os
from flask import Flask
import threading
from telegram.ext import Application, CommandHandler

TOKEN = os.getenv("BOT_TOKEN")

# عشان Render ما يقول Failed
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "Bot is running"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

async def start(update, context):
    await update.message.reply_text("البوت شغال ✅")

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
