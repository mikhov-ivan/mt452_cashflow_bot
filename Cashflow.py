import os
import re
import telegram

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import RegexHandler
from telegram.ext import CallbackQueryHandler

from Utils import ServerUtils
from Commands import Cmd


class Bot:
    def __init__(self):
        self.cmds = {
            "get_list": Cmd.get_list # get_list -type group [-ouid <ouid>]
        }
    
    def set_handlers(self, dispatcher):
        for cmd, handler in self.cmds.items():
            ServerUtils.log("Register regex command: {}".format(cmd))
            rh = RegexHandler("^(" + cmd + ".*)$", handler)
            dispatcher.add_handler(rh)
            
            ServerUtils.log("Register callback handler")
            dispatcher.add_handler(CallbackQueryHandler(self.handle_callback))
    
    def handle_callback(self, bot, update):
        query = update.callback_query
        for cmd, handler in self.cmds.items():
            pattern = re.compile("^(" + cmd + ".*)$")
            if pattern.match(query.data):
                ServerUtils.log("Handle callback: {}".format(query.data))
                ServerUtils.log("Handle as: {}".format(cmd))
                query.message.text = query.data
                handler(bot, query, True)
                
                
                
                
    # def handle_get(self
            
        
        # get_list -t category -g 452
        
        # self.general_handler        = GeneralHandler()
        # self.common_handler         = CommonHandler()
        # self.transaction_handler    = TransactionHandler()
        
        # self.cmd = {
            # "start":                           {"handler": self.general_handler.start,      "reg": None},
            # Cmd.GET_CATEGORY_GROUP_LIST.value: {"handler": self.common_handler.cgs,         "reg": "{}"},
            # Cmd.GET_CATEGORY_LIST.value:       {"handler": self.common_handler.cats,        "reg": "{}"},   
            # Cmd.GET_TRANSACTION_LIST.value:    {"handler": self.common_handler.trans,       "reg": "{}"},
            # Cmd.CREATE_TRANSACTION.value:      {"handler": self.transaction_handler.create, "reg": "{}"},
            # Cmd.EDIT_TRANSACTION.value:        {"handler": self.transaction_handler.edit,   "reg": "/{}[0-9]+"},
            # Cmd.DELETE_TRANSACTION.value:      {"handler": self.transaction_handler.delete, "reg": "/{}[0-9]+"}
        # }
    
    # def set_handlers(self, dispatcher):
        # for cmd, val in self.cmd.items():
            # if val["reg"]:
                # cm = val["reg"].format(cmd).upper()
                # uc = val["reg"].format(cmd).upper()
                # lc = val["reg"].format(cmd).lower()
                # Utils.log("Register regex command: {}".format(val["reg"].format(cmd)))
                # cmh = RegexHandler("^(" + val["reg"].format(cmd) + ")$", val["handler"])
                # uch = RegexHandler("^(" + uc + ")$", val["handler"])
                # lch = RegexHandler("^(" + lc + ")$", val["handler"])
                # dispatcher.add_handler(cmh)
                # dispatcher.add_handler(uch)
                # dispatcher.add_handler(lch)
            # else:
                # Utils.log("Register command: /{}".format(cmd))
                # dispatcher.add_handler(CommandHandler(cmd, val["handler"]))

