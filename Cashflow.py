import os
import logging
import telegram

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import RegexHandler

from handlers.GeneralHandler import GeneralHandler
from handlers.CommonHandler import CommonHandler
from handlers.TransactionHandler import TransactionHandler

from Structures import Utils
from Structures import Cmd


class Cashflow:
    def __init__(self):
        self.general_handler        = GeneralHandler()
        self.common_handler         = CommonHandler()
        self.transaction_handler    = TransactionHandler()
        
        self.cmd = {
            "start":                           {"handler": self.general_handler.start,      "reg": None},
            Cmd.GET_CATEGORY_GROUP_LIST.value: {"handler": self.common_handler.cgs,         "reg": None},
            Cmd.GET_CATEGORY_LIST.value:       {"handler": self.common_handler.cats,        "reg": None},   
            Cmd.GET_TRANSACTION_LIST.value:    {"handler": self.common_handler.trans,       "reg": None},
            Cmd.CREATE_TRANSACTION.value:      {"handler": self.transaction_handler.create, "reg": None},
            Cmd.EDIT_TRANSACTION.value:        {"handler": self.transaction_handler.edit,   "reg": "/{}[0-9]+"},
            Cmd.DELETE_TRANSACTION.value:      {"handler": self.transaction_handler.delete, "reg": "/{}[0-9]+"}
        }
    
    def set_handlers(self, updater):
        for cmd, val in self.cmd.items():
            if val["reg"]:
                uc = val["reg"].format(cmd).upper()
                lc = val["reg"].format(cmd).lower()
                Utils.log("Register regex command: {}".format(val["reg"].format(cmd)))
                uch = RegexHandler("^(" + uc + ")$", val["handler"])
                lch = RegexHandler("^(" + lc + ")$", val["handler"])
                updater.dispatcher.add_handler(uch)
                updater.dispatcher.add_handler(lch)
            else:
                Utils.log("Register command: /{}".format(cmd))
                updater.dispatcher.add_handler(CommandHandler(cmd, val["handler"]))

