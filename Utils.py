import os
import logging
import telegram

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from Structures import Formats
from Structures import Types
from helpers.DBHelper import DBHelper


class TgUtils(object):
    @classmethod
    def send(cls, bot, update, msg):
        chat_id = update.message.chat_id
        ServerUtils.log("Send msg to chat_{}".format(chat_id))
        bot.sendMessage(chat_id=chat_id, text=msg, parse_mode="HTML")

    @classmethod
    def build_keyboard(cls, items):
        keyboard = [[item] for item in items]
        reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
        return json.dumps(reply_markup)
    
    @classmethod
    def build_keyboard(cls, items):
        line = []
        keyboard = []
        markup = None
        if len(items):
            for title, callback in items.items():
                button = InlineKeyboardButton(title, callback_data=callback)
                if len(line) < 3:
                    line.append(button)
                else:
                    keyboard.append(line)
                    line = [button]
            
            if type == Types.CATEGORY:
                callback = "{}_{}_{}".format(CmdPrefix.CREATE.value, TypePrefix.TRANSACTION.value, row.ouid)
                Utils.log("Register callback: {}".format(callback))
            
            button = InlineKeyboardButton("Создать", callback_data=callback)
            if len(line) > 0 and len(line) < 3:
                line.append(button)
                keyboard.append(line)
            else:
                line = [button]
                keyboard.append(line)
            markup = InlineKeyboardMarkup(keyboard)
        return markup


class ServerUtils(object):
    logging.basicConfig(level=logging.INFO, format=Formats.LOG.value)
    logger = logging.getLogger()

    @classmethod
    def log(cls, msg):
        cls.logger.info(msg)
    
    @classmethod
    def log_update(cls, update):
        cls.log("Update_{} was sent by {} {}: {}".format(
            update.message.message_id,
            update.message.from_user.first_name,
            update.message.from_user.last_name,
            update.message.text))
    
    @classmethod
    def align_right(cls, value):
        return "{:4.1f}".format(value)


class AppData(object):
    db = DBHelper()
    keyboards = {}


class Preferences(object):
    mode = os.getenv("MODE")

