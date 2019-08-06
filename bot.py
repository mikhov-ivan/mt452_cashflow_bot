import os
import logging
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from dbhelper import DBHelper

global APP_URL
global APP_KEY
global BOT_URL
global TOKEN
global PORT

APP_URL = 'https://mt452-cashflow-bot.herokuapp.com/'
APP_KEY = '4276eb911ca3133611d23040e1ee439ea21738932dda94e502f37fae0497'
BOT_URL = 'https://api.telegram.org/bot861062365:AAEq3evcJCE5nZCSclev9Z8ki-cAjwdTUqQ/'
TOKEN = '861062365:AAEq3evcJCE5nZCSclev9Z8ki-cAjwdTUqQ'
PORT = int(os.environ.get('PORT', '8443'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def handle_start(bot, update):
    logger.info("User {} started bot".format(update.effective_user["id"]))
    update.message.reply_text("Hello, {}!".format(update.message.from_user.first_name))


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler("start", handle_start))
    updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN, key=APP_KEY)
    updater.bot.set_webhook(APP_URL + TOKEN)

