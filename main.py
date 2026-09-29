import os
from threading import Thread
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is alive!"
def run_web(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
Thread(target=run_web, daemon=True).start()
