import os
import logging
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import RegexHandler
from StateMachine import StateMachine
from DBHelper import DBHelper
from enum import Enum

global logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger()


class CmdPrefix(Enum):
    CATEGORY_GROUP = "cg_"
    CATEGORY = "c_"


class Cashflow:
    def __init__(self):
        self.db = DBHelper()
        self.sm = StateMachine()
    
    def set_handlers(self, updater):
        for prefix in CmdPrefix: updater.dispatcher.add_handler(self.get_regex_handler(prefix))
        updater.dispatcher.add_handler(CommandHandler("start", self.handle_start))
        updater.dispatcher.add_handler(CommandHandler("cgs", self.handle_cgs))
        updater.dispatcher.add_handler(CommandHandler("cats", self.handle_cats))
        
    def get_regex_handler(self, prefix):
        if prefix == CmdPrefix.CATEGORY_GROUP: handler = self.handle_category_group
        elif prefix == CmdPrefix.CATEGORY: handler = self.handle_category
        return RegexHandler("^(/" + prefix.value + "[a-zA-Z]+)$", handler)

    def handle_category_group(self, bot, update):
        self.log_update(update)
        self.send(bot, update.message.chat_id, "Category group: <b>{}</b>".format(update.message.text))

    def handle_category(self, bot, update):
        self.log_update(update)
        self.send(bot, update.message.chat_id, "Category: <b>{}</b>".format(update.message.text))
        
    def handle_cats(self, bot, update):
        self.log_update(update)
        categories = self.db.get_categories()
        if len(categories) > 0:
            msg = ""
            for c in categories.values():
                msg += "{}: /{}{}{}".format(c.title, CmdPrefix.CATEGORY.value, c.code, os.linesep)
            html = "Following <b>categories</b> are available:{}{}{}".format(os.linesep, os.linesep, msg)
        else:
            html = "There are <b>no categories</b> available".format(os.linesep)
        self.send(bot, update.message.chat_id, html)
        
    def handle_cgs(self, bot, update):
        self.log_update(update)
        category_groups = self.db.get_category_groups()
        if len(category_groups) > 0:
            msg = ""
            for cg in category_groups.values():
                msg += "{}: /{}{}{}".format(cg.title, CmdPrefix.CATEGORY_GROUP.value, cg.code, os.linesep)
            html = "Following <b>category groups</b> are available:{}{}{}".format(os.linesep, os.linesep, msg)
        else:
            html = "There are <b>no category groups</b> available".format(os.linesep)
        self.send(bot, update.message.chat_id, html)
        
    def handle_start(self, bot, update):
        logger.info("User {} started bot".format(update.effective_user["id"]))
        self.send(bot, update.message.chat_id, "Hello, <b>{}</b>!".format(update.message.from_user.first_name))
        
    def send(self, bot, chat_id, msg):
        bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='HTML')

    def log_update(self, update):
        logger.info("{} {}".format(update.update_id, update.message))

