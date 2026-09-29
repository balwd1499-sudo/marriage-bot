import os,json,threading
from flask import Flask
import telegram.ext as te
from telegram import ReplyKeyboardMarkup

T=os.getenv("BOT_TOKEN")
W=Flask(__name__)
A,L,B=range(3)
F="data.json"

def ld():
 if os.path.exists(F):
  try:
   return json.load(open(F,'r',encoding='utf-8'))
  except: pass
 return {"brides":[],"grooms":[]}

def sv(d):
 json.dump(d,open(F,'w',encoding='utf-8'),ensure_ascii=False,indent=2)

@W.route('/')
def h(): return "OK"

def rw():
 W.run(host='0.0.0.0',port=int(os.getenv("PORT",10000)))

async def st(u,c):
 k=[["عروس","عريس"],["بحث"]]
 m=ReplyKeyboardMarkup(k,resize_keyboard=True)
 await u.message.reply_text("مرحبا",reply_markup=m)

async def ty(u,c):
 t=u.message.text
 if "بحث" in t:
  return await sh(u,c)
 if "عروس" in t: c.user_data['t']="brides"
 else: c.user_data['t']="grooms"
 await u.message.reply_text("كم العمر؟")
 return A

async def ag(u,c):
 c.user_data['a']=u.message.text
 await u.message.reply_text("السكن؟")
 return L

async def lo(u,c):
 c.user_data['l']=u.message.text
 await u.message.reply_text("نبذة؟")
 return B

async def bi(u,c):
 d=ld()
 e={"age":c.user_data['a'],"loc":c.user_data['l'],"bio":u.message.text}
 d[c.user_data['t']].append(e)
 sv(d)
 await u.message.reply_text("تم الحفظ")
 return te.ConversationHandler.END

async def sh(u,c):
 d=ld()
 if not d["brides"] and not d["grooms"]:
  await u.message.reply_text("فاضي")
  return te.ConversationHandler.END
 s=""
 for x in d["brides"][-3:]: s+=f"{x['age']}-{x['loc']}\n"
 for x in d["grooms"][-3:]: s+=f"{x['age']}-{x['loc']}\n"
 await u.message.reply_text(s or "فاضي")
 return te.ConversationHandler.END

def main():
 threading.Thread(target=rw,daemon=True).start()
 a=te.Application.builder().token(T).build()
 cv=te.ConversationHandler(entry_points=[te.MessageHandler(te.filters.Regex("عروس|عريس"),ty)],states={A:[te.MessageHandler(te.filters.TEXT,ag)],L:[te.MessageHandler(te.filters.TEXT,lo)],B:[te.MessageHandler(te.filters.TEXT,bi)]},fallbacks=[])
 a.add_handler(te.CommandHandler("start",st))
 a.add_handler(cv)
 a.add_handler(te.MessageHandler(te.filters.Regex("بحث"),sh))
 a.run_polling()

if __name__=="__main__": main()
