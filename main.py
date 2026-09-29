import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

TOKEN=os.getenv("BOT_TOKEN")
web=Flask(__name__)
@web.route('/')
def home():return "OK"

def run():
 web.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
Thread(target=run,daemon=True).start()

async def start(update,context):
 await update.message.reply_text("البوت شغال 24 ساعة ✅")

async def handle(update,context):
 if "المتواجدون" in update.message.text:
  await update.message.reply_text("👥 انت متصل الآن 🟢")

bot=ApplicationBuilder().token(TOKEN).build()
bot.add_handler(CommandHandler("start",start))
bot.add_handler(MessageHandler(filters.TEXT,handle))
bot.run_polling()
