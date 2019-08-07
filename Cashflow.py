import os
import logging
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from DBHelper import DBHelper

global logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger()

class Cashflow:
    def __init__(self):
        self.db = DBHelper()
        self.state = "main"
    
    def set_handlers(self, updater):
        categories = self.db.get_categories()
        for (
            category_ouid,
            category_code,
            category_title,
            category_group_ouid,
            category_group_title
        ) in categories.values():
            updater.dispatcher.add_handler(CommandHandler(category_code, self.handle_cats))
        updater.dispatcher.add_handler(CommandHandler("start", self.handle_start))
        updater.dispatcher.add_handler(CommandHandler("cats", self.get_categories))

    def handle_start(self, bot, update):
        logger.info("User {} started bot".format(update.effective_user["id"]))
        self.send(bot, update.message.chat_id, "Hello, <b>{}</b>!".format(update.message.from_user.first_name))

    def handle_cats(self, bot, update):
        self.log_update(update)
        self.send(bot, update.message.chat_id, "Category, <b>info</b>")
        
    def get_categories(self, bot, update):
        self.log_update(update)
        categories = self.db.get_categories()
        if len(categories) > 0:
            msg = ""
            for (
                category_ouid,
                category_code,
                category_title,
                category_group_ouid,
                category_group_title
            ) in categories.values():
                msg += "/{} - {}{}".format(code, title, os.linesep)
            html = "Following <b>categories</b> are available:{}{}{}".format(os.linesep, os.linesep, msg)
        else:
            html = "There are <b>no categories</b> available".format(os.linesep)
        self.send(bot, update.message.chat_id, html)
        
    def send(self, bot, chat_id, msg):
        bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='HTML')

    def log_update(self, update):
        logger.info("{} {}".format(update.update_id, update.message))

