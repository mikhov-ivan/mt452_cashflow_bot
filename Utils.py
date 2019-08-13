import os
import logging

from Structures import Format
from helpers.DBHelper import DBHelper


class Utils(object):
    db = DBHelper()
    mode = os.getenv("MODE")
    logging.basicConfig(level=logging.INFO, format=Format.LOG.value)
    logger = logging.getLogger()

    @classmethod
    def log(cls, msg):
        cls.logger.info(msg)
    
    @classmethod
    def log_update(cls, update):
        cls.log("Update_{} was sent by {} {}: {}".format(
            update.update_id,
            update.message.from_user.first_name,
            update.message.from_user.last_name,
            update.message.text))

    @classmethod
    def send(cls, bot, chat_id, msg):
        cls.log("Send msg to chat_{}".format(chat_id))
        bot.sendMessage(chat_id=chat_id, text=msg, parse_mode="HTML")

    @classmethod
    def build_keyboard(cls, items):
        keyboard = [[item] for item in items]
        reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
        return json.dumps(reply_markup)

