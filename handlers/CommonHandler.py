import os
import logging
import telegram

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from Structures import Utils
from Structures import Type
from Structures import Format
from Structures import CmdPrefix
from Structures import TypePrefix
from helpers.DBHelper import DBHelper


class CommonHandler:
    def __init__(self):
        self.db = DBHelper()
        
    def cgs(self, bot, update):
        Utils.log_update(update)
        msg = "Список доступных <b>групп</b>"
        markup = self.get_inline_keyboard(Type.CATEGORY_GROUP)
        update.message.reply_text(msg, reply_markup=markup, parse_mode="HTML")
        
    def cats(self, bot, update):
        Utils.log_update(update)
        msg = "Список доступных <b>категорий</b>"
        markup = self.get_inline_keyboard(Type.CATEGORY)
        update.message.reply_text(msg, reply_markup=markup, parse_mode="HTML")
        
    def trans(self, bot, update):
        Utils.log_update(update)
        html = self.get_list(Type.TRANSACTION)
        Utils.send(bot, update.message.chat_id, html)
    
    def get_inline_keyboard(self, type):
        if type == Type.CATEGORY_GROUP:
            response = self.db.get_category_groups()
        elif type == Type.CATEGORY:
            response = self.db.get_categories()
        elif type == Type.TRANSACTION:
            response = self.db.get_transactions()
        
        line = []
        keyboard = []
        if len(response):
            for row in response.values():
                button = InlineKeyboardButton(row.title, callback_data=row.code)
                if len(line) < 3:
                    line.append(button)
                else:
                    keyboard.append(line)
                    line = [button]
            if len(line) > 0 and len(line) < 3:
                keyboard.append(line)
            return InlineKeyboardMarkup(keyboard)
        else:
            return None
        
    def get_list(self, type):
        if type == Type.CATEGORY_GROUP:
            response = self.db.get_category_groups()
            template = "<b>{} category groups</b> are available:{}{}{}"
            
        elif type == Type.CATEGORY:
            response = self.db.get_categories()
            template = "<b>{} categories</b> are available:{}{}{}"
            
        elif type == Type.TRANSACTION:
            response = self.db.get_transactions()
            template = "<b>{} transactions</b> recorded:{}{}{}"
        
        if len(response) > 0:
            msg = ""
            for row in response.values():
                if type == Type.CATEGORY_GROUP or type == Type.CATEGORY:
                    msg += "{} /{} /{}{}".format(
                        row.title,
                        "{}{}{}".format(CmdPrefix.EDIT.value, TypePrefix[type.name].value, row.ouid),
                        "{}{}{}".format(CmdPrefix.DELETE.value, TypePrefix[type.name].value, row.ouid),
                        os.linesep)
                elif type == Type.TRANSACTION:
                    date = row.execution_date.strftime(Format.DATETIME.value)
                    msg += "{}{}".format(
                        "<b>{}</b>: {} {}{}".format(date, row.amount, row.currency, os.linesep),
                        "{} {} {}{}{}".format(
                            row.title, 
                            "/{}{}{}".format(CmdPrefix.EDIT.value, TypePrefix[type.name].value, row.ouid),
                            "/{}{}{}".format(CmdPrefix.DELETE.value, TypePrefix[type.name].value, row.ouid),
                            os.linesep,
                            os.linesep))
            html = template.format(len(response), os.linesep, os.linesep, msg)
        else:
            html = "List is empty"
        return html

