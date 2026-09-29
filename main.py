import os, json, threading
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = os.getenv("BOT_TOKEN")
app_flask = Flask(__name__)

# حالات المحادثة
AGE, LOCATION, BIO, TYPE = range(4)
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"brides": [], "grooms": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app_flask.route('/')
def home(): return "Bot is running OK"
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["👰 عروس", "🤵 عريس"], ["🔍 بحث"]]
    await update.message.reply_text(
        "Welcome to Omdurman Marriage Bot\nاختار:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def ask_type(update, context):
    text = update.message.text
    if "عروس" in text: context.user_data['type'] = 'brides'
    elif "عريس" in text: context.user_data['type'] = 'grooms'
    else: return await search(update, context)
    
    if 'بحث' in text: return await search(update, context)
    
    await update.message.reply_text("كم العمر؟")
    return AGE

async def ask_age(update, context):
    context.user_data['age'] = update.message.text
    await update.message.text and update.message.reply_text("السكن وين؟ (مثلا: أمدرمان الثورة)")
    return LOCATION

async def ask_location(update, context):
    context.user_data['location'] = update.message.text
    await update.message.reply_text("اكتب نبذة قصيرة عنك (عملك، مواصفات)")
    return BIO

async def save_bio(update, context):
    data = load_data()
    new_entry = {
        "id": update.effective_user.id,
        "name": update.effective_user.first_name,
        "age": context.user_data['age'],
        "location": context.user_data['location'],
        "bio": update.message.text,
        "username": update.effective_user.username
    }
    data[context.user_data['type']].append(new_entry)
    save_data(data)
    await update.message.reply_text("✅ تم الحفظ! بياناتك دخلت النظام. استخدم 🔍 بحث عشان تشوف ناس تانية.")
    return ConversationHandler.END

async def search(update, context):
    data = load_data()
    text = "👰 العرايس:\n"
    for b in data['brides'][-5:]: # اخر 5
        text += f"- {b['age']} سنة - {b['location']} - {b['bio']}\n"
    text += "\n🤵 العرسان:\n"
    for g in data['grooms'][-5:]:
        text += f"- {g['age']} سنة - {g['location']} - {g['bio']}\n"
    if not data['brides'] and not data['grooms']:
        text = "لسه مافي بيانات مسجلة."
    await update.message.reply_text(text)
    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("تم الالغاء")
    return ConversationHandler.END

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    
    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^(👰 عروس|🤵 عريس|🔍 بحث)$"), ask_type)],
        states={
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_location)],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.Regex("^🔍 بحث$"), search))
    
    app.run_polling()

if __name__ == "__main__":
    main()
