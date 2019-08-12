import os
import telegram

from telegram.ext import Updater
from telegram.ext import CommandHandler

from Structures import Utils
from Cashflow import Bot


APP_URL = "https://mt452-cashflow-bot.herokuapp.com/"
APP_KEY = "4276eb911ca3133611d23040e1ee439ea21738932dda94e502f37fae0497"
BOT_URL = "https://api.telegram.org/bot861062365:AAEq3evcJCE5nZCSclev9Z8ki-cAjwdTUqQ/"
TOKEN = "861062365:AAEq3evcJCE5nZCSclev9Z8ki-cAjwdTUqQ"
PORT = int(os.environ.get("PORT", "8443"))


if __name__ == "__main__":
    bot = Bot()
    updater = Updater(token=TOKEN)
    bot.set_handlers(updater.dispatcher)
    
    if Utils.mode == "dev":
        updater.start_polling()
        updater.idle()
    elif Utils.mode == "prod":
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, key=APP_KEY)
        updater.bot.set_webhook(APP_URL + TOKEN)
    
    #game.run(port=PORT)

