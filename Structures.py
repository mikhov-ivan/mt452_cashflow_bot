import os
import logging
import datetime
from enum import Enum


class Type(Enum):
    CATEGORY_GROUP = 1
    CATEGORY = 2
    TRANSACTION = 3


class TypePrefix(Enum):
    CATEGORY_GROUP      = "CG"
    CATEGORY            = "C"
    TRANSACTION         = "T"


class CmdPrefix(Enum):
    EDIT                = "E"
    DELETE              = "D"


class Format(Enum):
    LOG                 = "%(asctime)s %(levelname)s: %(message)s"
    DATETIME            = "%d.%m.%Y %H:%m"

class Cmd(Enum):
    START                       = "start"
    GET_CATEGORY_GROUP_LIST     = TypePrefix.CATEGORY_GROUP.value
    GET_CATEGORY_LIST           = TypePrefix.CATEGORY.value
    GET_TRANSACTION_LIST        = TypePrefix.TRANSACTION.value
    EDIT_TRANSACTION            = "{}{}".format(CmdPrefix.EDIT.value, TypePrefix.TRANSACTION.value)
    DELETE_TRANSACTION          = "{}{}".format(CmdPrefix.DELETE.value, TypePrefix.TRANSACTION.value)


class CategoryGroup:
    def __init__(self, ouid, code, title):
        self.ouid = ouid
        self.code = code
        self.title = title


class Category:
    def __init__(self, ouid, code, title):
        self.ouid = ouid
        self.code = code
        self.title = title


class Transaction:
    def __init__(self, ouid, execution_date, code, amount, title):
        self.ouid = ouid
        self.execution_date = datetime.datetime.strptime(str(execution_date), "%Y-%m-%d %H:%M:%S")
        self.currency = code
        self.amount = amount
        self.title = title


class Utils(object):
    mode = os.getenv("MODE")
    logging.basicConfig(level=logging.INFO, format=Format.LOG.value)
    logger = logging.getLogger()

    @classmethod
    def log(cls, msg):
        cls.logger.info(msg)
    
    def log_update(update):
        log("{} by {}: {}".format(
            update.update_id,
            update.message.from_user.username,
            update.message.text))

    def send(bot, chat_id, msg):
        bot.sendMessage(chat_id=chat_id, text=msg, parse_mode="HTML")

