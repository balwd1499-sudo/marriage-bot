import os, json, threading
from flask import Flask
from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram.ext import *
TOKEN = os.getenv("BOT_TOKEN")
web = Flask(__name__)
AGE, LOC, BIO = range(3)
FILE = "data.json"
def load():
 if os.path.exists(FILE):
  with open(FILE,'r',encoding='utf-8') as f:
   try: return json.load(f)
   except: pass
 return {"brides":[],"grooms":[]}
def save(d):
 with open(FILE,'w',encoding='utf-8') as f:
  json.dump(d,f,ensure_ascii=False,indent=2)
@web.route('/')
def home(): return "Bot OK"
def run_web():
 p=int(os.environ.get("PORT",10000))
 web.run(host='0.0.0.0',port=p)
async def start(upd,ctx):
 kb=[["👰 عروس","🤵 عريس"],["🔍 بحث"]]
 mk=ReplyKeyboardMarkup(kb,resize_keyboard=True)
 await upd.message.reply_text("Welcome",reply_markup=mk)
async def ask_type(upd,ctx):
 t=upd.message.text
 if "بحث" in t: return await do_search(upd,ctx)
 if "عروس" in t: ctx.user_data['t']='brides'
 else: ctx.user_data['t']='grooms'
 await upd.message.reply_text("كم العمر؟")
 return AGE
async def ask_age(upd,ctx):
 ctx.user_data['a']=upd.message.text
 await upd.message.reply_text("السكن وين؟")
 return LOC
async def ask_loc(upd,ctx):
 ctx.user_data['l']=upd.message.text
 await upd.message.reply_text("نبذة قصيرة")
 return BIO
async def save_bio(upd,ctx):
 d=load()
 e={"age":ctx.user_data['a'],"loc":ctx.user_data['l'],"bio":upd.message.text,"name":upd.effective_user.first_name}
 d[ctx.user_data['t']].append(e)
 save(d)
 await upd.message.reply_text("✅ تم الحفظ!")
 return ConversationHandler.END
async def do_search(upd,ctx):
 d=load()
 if not d['brides'] and not d['grooms']:
  await upd.message.reply_text("لسه مافي بيانات")
  return ConversationHandler.END
 m="👰 عرايس:\n"
 for b in d['brides'][-5:]: m+=f"{b['age']} - {b['loc']} - {b['bio']}\n"
 m+="\n🤵 عرسان:\n"
 for g in d['grooms'][-5:]: m+=f"{g['age']} - {g['loc']} - {g['bio']}\n"
 await upd.message.reply_text(m)
 return ConversationHandler.END
def main():
 threading.Thread(target=run_web,daemon=True).start()
 app=Application.builder().token(TOKEN).build()
 conv=ConversationHandler(entry_points=[MessageHandler(filters.Regex("عروس|عريس"),ask_type)],states={AGE:[MessageHandler(filters.TEXT,ask_age)],LOC:[MessageHandler(filters.TEXT,ask_loc)],BIO:[MessageHandler(filters.TEXT,save_bio)]},fallbacks=[])
 app.add_handler(CommandHandler("start",start))
 app.add_handler(conv)
 app.add_handler(MessageHandler(filters.Regex("بحث"),do_search))
 app.run_polling()
if __name__=="__main__": main()
