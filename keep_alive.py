from flask import Flask
from threading import Thread

carsales = Flask(__name__)
carsales.debug = True

def run():
    carsales.run(host="0.0.0.0", port=3000)

def keep_alive():
    t = Thread(target=run)
    t.start()