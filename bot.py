import os
import logging
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from DBHelper import DBHelper

global APP_URL
global APP_KEY
global BOT_URL
global TOKEN
global PORT

global db
global logger

APP_URL = "https://mt452-cashflow-bot.herokuapp.com/"
APP_KEY = "4276eb911ca3133611d23040e1ee439ea21738932dda94e502f37fae0497"
BOT_URL = "https://api.telegram.org/bot861062365:AAEq3evcJCE5nZCSclev9Z8ki-cAjwdTUqQ/"
TOKEN = "861062365:AAEq3evcJCE5nZCSclev9Z8ki-cAjwdTUqQ"
PORT = int(os.environ.get("PORT", "8443"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger()
db = DBHelper()


def log_update(update):
    logger.info("{} {}".format(update.update_id, update.message))
    
def send(bot, chat_id, msg):
    bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='HTML')

def handle_start(bot, update):
    logger.info("User {} started bot".format(update.effective_user["id"]))
    update.message.reply_text("Hello, {}!".format(update.message.from_user.first_name))
    
def get_categories(bot, update):
    msg = ""
    log_update(update)
    categories = db.get_categories()
    for c in categories: msg += "[{}] {} {}\n".format(c.ouid, c.code, c.title)
    html = "Following <b>categories</b> are available:{}%0A".format(msg)
    send(bot, update.message.chat_id, html)


if __name__ == "__main__":
    logger.info("Starting bot")
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler("start", handle_start))
    updater.dispatcher.add_handler(CommandHandler("categories", get_categories))
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, key=APP_KEY)
    updater.bot.set_webhook(APP_URL + TOKEN)
