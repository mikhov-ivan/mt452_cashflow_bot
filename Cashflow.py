import os
import logging
import datetime
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import RegexHandler
from StateMachine import StateMachine
from DBHelper import DBHelper
from enum import Enum

global DATETIME_FORMAT
DATETIME_FORMAT = "%d.%m.%Y %H:%M"

global logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger()

        
def send(bot, chat_id, msg):
    bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='HTML')

def log_update(update):
    logger.info("{} {}".format(update.update_id, update.message))


class Type(Enum):
    CATEGORY_GROUP = 1
    CATEGORY = 2
    TRANSACTION = 3


class TypePrefix(Enum):
    CATEGORY_GROUP = "cgs"
    CATEGORY = "cs"
    TRANSACTION = "ts"


class CmdPrefix(Enum):
    DELETE = "d"


class GeneralHandler:
    def __init__(self):
        self.db = DBHelper()
    
    def handle_start(self, bot, update):
        logger.info("User {} {} started bot".format(update.effective_user["id"], update.message.from_user.first_name))
        send(bot, update.message.chat_id, "Hello, <b>{}</b>!".format(update.message.from_user.first_name))
        
    def handle_cgs(self, bot, update):
        log_update(update)
        html = self.get_list(Type.CATEGORY_GROUP)
        send(bot, update.message.chat_id, html)
        
    def handle_cats(self, bot, update):
        log_update(update)
        html = self.get_list(Type.CATEGORY)
        send(bot, update.message.chat_id, html)
        
    def handle_trans(self, bot, update):
        log_update(update)
        html = self.get_list(Type.TRANSACTION)
        send(bot, update.message.chat_id, html)
        
    def get_list(self, type):
        if type == Type.CATEGORY_GROUP:
            response = self.db.get_category_groups()
            template = "Following <b>{} category groups</b> are available:{}{}{}"
            
        elif type == Type.CATEGORY:
            response = self.db.get_categories()
            template = "Following <b>{} categories</b> are available:{}{}{}"
            
        elif type == Type.TRANSACTION:
            response = self.db.get_transactions()
            template = "You have <b>{} transactions</b> recorded:{}{}{}"
        
        if len(response) > 0:
            msg = ""
            for row in response.values():
                if type == Type.CATEGORY_GROUP or type == Type.CATEGORY:
                    msg += "{}: /{}{}{}".format(
                        row.title,
                        "{}{}_".format(CmdPrefix.DELETE.value, TypePrefix[type.name].value),
                        row.code,
                        os.linesep)
                elif type == Type.TRANSACTION:
                    msg += "{}: {} {} {} /{}{}".format(
                        row.execution_date.strftime(DATETIME_FORMAT),
                        row.amount,
                        row.currency,
                        row.title,
                        "{}{}_".format(CmdPrefix.DELETE.value, TypePrefix[type.name].value),
                        row.ouid,
                        os.linesep)
            html = template.format(len(response), os.linesep, os.linesep, msg)
        else:
            html = "List is empty"
        return html
    


class Cashflow:
    def __init__(self):
        self.db = DBHelper()
        self.sm = StateMachine()
        self.gh = GeneralHandler()
        
        self.handlers = {
            "start": self.gh.handle_start,
            "cgs": self.gh.handle_cgs,
            "cs": self.gh.handle_cats,
            "ts": self.gh.handle_trans,
            "dts": self.handle_delete_transaction
        }
    
    def set_handlers(self, updater):
        for t in TypePrefix:
            if t in self.handlers:
                updater.dispatcher.add_handler(self.handlers[t])
            for cmd in CmdPrefix:
                prefix = "{}{}".format(cmd.value, t.value)
                if prefix in self.handlers:
                    logger.info("Register regex command: /{}_[a-zA-Z]+".format(prefix))
                    handler = RegexHandler("^(/" + prefix + "_[a-zA-Z]+)$", self.handlers[prefix])
                    updater.dispatcher.add_handler(handler)
    
        logger.info("Register general commands: /start, /cgs, /cgs, /cs, /ts".format(prefix))
        updater.dispatcher.add_handler(CommandHandler("start", self.handlers["start"]))
        updater.dispatcher.add_handler(CommandHandler("cgs", self.handlers["cgs"]))
        updater.dispatcher.add_handler(CommandHandler("cs", self.handlers["cs"]))
        updater.dispatcher.add_handler(CommandHandler("ts", self.handlers["ts"]))
        
    def handle_delete_transaction(self, bot, update):
        log_update(update)
        tmp_split = update.message.text.split("_")
        ouid = tmp_split[len(tmp_split) - 1]
        result = 1
        if result: send(bot, update.message.chat_id, "Transaction {} was deleted".format(ouid))
        else: send(bot, update.message.chat_id, "Transaction {} can not be deleted".format(ouid))
        
    def handle_category_group(self, bot, update):
        log_update(update)
        send(bot, update.message.chat_id, "Category group: <b>{}</b>".format(update.message.text))

    def handle_category(self, bot, update):
        log_update(update)
        send(bot, update.message.chat_id, "Category: <b>{}</b>".format(update.message.text))

