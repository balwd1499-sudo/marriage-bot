import os
from threading import Thread
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home(): return "Marriage bot is alive!"
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
Thread(target=run_flask, daemon=True).start()

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json, logging
BOT_TOKEN = os.environ.get("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
marriages = {}
try:
    if os.path.exists("marriages.json"):
        with open("marriages.json", "r") as f: marriages = json.load(f)
except: marriages = {}
def save():
    try:
        with open("marriages.json", "w") as f: json.dump(marriages, f)
    except: pass
def start(update, context):
    update.message.reply_text("أهلا! بوت الزواج شغال ❤️\n+بрак @الشخص\nбраки\nстата")
def marry(update, context):
    if not update.message.reply_to_message:
        update.message.reply_text("رد على رسالة الشخص الداير تتزوجو +بрак")
        return
    user1 = update.effective_user.id
    user2 = update.message.reply_to_message.from_user.id
    if user1 == user2:
        update.message.reply_text("ما ممكن تتزوج نفسك 😂")
        return
    pair = f"{min(user1,user2)}_{max(user1,user2)}"
    if pair in marriages:
        update.message.reply_text("انتو متزوجين أصلا! 💍")
        return
    marriages[pair] = {"users": [user1, user2]}
    save()
    update.message.reply_text(f"تم الزواج! 💍❤️ {update.effective_user.first_name} + {update.message.reply_to_message.from_user.first_name}")
def my_marriages(update, context):
    uid = update.effective_user.id
    count = sum(1 for v in marriages.values() if uid in v["users"])
    update.message.reply_text(f"عندك {count} زيجة 💍")
def stats(update, context):
    update.message.reply_text(f"إجمالي الزيجات: {len(marriages)}\nالبوت شغال في Render ✅")
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("браки", my_marriages))
    dp.add_handler(CommandHandler("стата", stats))
    dp.add_handler(MessageHandler(Filters.regex(r"^\+брак"), marry))
    updater.start_polling()
    updater.idle()
if __name__ == "__main__": main()
