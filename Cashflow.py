import os
import re
import telegram

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import RegexHandler
from telegram.ext import CallbackQueryHandler

from Utils import ServerUtils
from Structures import Regexps
from Commands import CmdGet
from Commands import CmdCreate


class Bot:
    def __init__(self):
        self.cmds = {
            "^(get_list.*)$": CmdGet.get_list,      # get_list -type group [-ouid <ouid>]
            Regexps.NUMBER.value: CmdCreate.create  # create transaction by numeric input
        }
    
    def set_handlers(self, dispatcher):
        for cmd, handler in self.cmds.items():
            ServerUtils.log("Register regex command: {}".format(cmd))
            rh = RegexHandler(cmd, handler)
            dispatcher.add_handler(rh)
            
            ServerUtils.log("Register callback handler")
            dispatcher.add_handler(CallbackQueryHandler(self.handle_callback))
    
    def handle_callback(self, bot, update):
        query = update.callback_query
        for cmd, handler in self.cmds.items():
            pattern = re.compile(cmd)
            if pattern.match(query.data):
                ServerUtils.log("Handle callback: {}".format(query.data))
                ServerUtils.log("Handle as: {}".format(cmd))
                query.message.text = query.data
                handler(bot, query, True)

