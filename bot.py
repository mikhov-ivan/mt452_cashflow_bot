import os
import logging
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from Cashflow import Cashflow

global APP_URL
global APP_KEY
global BOT_URL
global TOKEN
global PORT

APP_URL = "https://mt452-cashflow-bot.herokuapp.com/"
APP_KEY = "4276eb911ca3133611d23040e1ee439ea21738932dda94e502f37fae0497"
BOT_URL = "https://api.telegram.org/bot861062365:AAEq3evcJCE5nZCSclev9Z8ki-cAjwdTUqQ/"
TOKEN = "861062365:AAEq3evcJCE5nZCSclev9Z8ki-cAjwdTUqQ"
PORT = int(os.environ.get("PORT", "8443"))

global app
app = Cashflow()

if __name__ == "__main__":
    updater = Updater(TOKEN)
    app.set_handlers(updater)
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, key=APP_KEY)
    updater.bot.set_webhook(APP_URL + TOKEN)
