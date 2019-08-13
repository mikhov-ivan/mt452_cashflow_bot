import os
import telegram
import Utils

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import RegexHandler

from handlers.GeneralHandler import GeneralHandler
from handlers.CommonHandler import CommonHandler
from handlers.TransactionHandler import TransactionHandler

from Structures import Cmd


class Bot:
    def __init__(self):
        self.general_handler        = GeneralHandler()
        self.common_handler         = CommonHandler()
        self.transaction_handler    = TransactionHandler()
        
        self.cmd = {
            "start":                           {"handler": self.general_handler.start,      "reg": None},
            Cmd.GET_CATEGORY_GROUP_LIST.value: {"handler": self.common_handler.cgs,         "reg": "{}"},
            Cmd.GET_CATEGORY_LIST.value:       {"handler": self.common_handler.cats,        "reg": "{}"},   
            Cmd.GET_TRANSACTION_LIST.value:    {"handler": self.common_handler.trans,       "reg": "{}"},
            Cmd.CREATE_TRANSACTION.value:      {"handler": self.transaction_handler.create, "reg": "{}"},
            Cmd.EDIT_TRANSACTION.value:        {"handler": self.transaction_handler.edit,   "reg": "/{}[0-9]+"},
            Cmd.DELETE_TRANSACTION.value:      {"handler": self.transaction_handler.delete, "reg": "/{}[0-9]+"}
        }
    
    def set_handlers(self, dispatcher):
        for cmd, val in self.cmd.items():
            if val["reg"]:
                cm = val["reg"].format(cmd).upper()
                uc = val["reg"].format(cmd).upper()
                lc = val["reg"].format(cmd).lower()
                Utils.log("Register regex command: {}".format(val["reg"].format(cmd)))
                cmh = RegexHandler("^(" + val["reg"].format(cmd) + ")$", val["handler"])
                uch = RegexHandler("^(" + uc + ")$", val["handler"])
                lch = RegexHandler("^(" + lc + ")$", val["handler"])
                dispatcher.add_handler(cmh)
                dispatcher.add_handler(uch)
                dispatcher.add_handler(lch)
            else:
                Utils.log("Register command: /{}".format(cmd))
                dispatcher.add_handler(CommandHandler(cmd, val["handler"]))

