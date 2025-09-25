<<<<<<< HEAD
import Flask
=======
from flask import Flask
>>>>>>> 9fe7d417444bfe392f5a9172f8044deba4b9c22f
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
