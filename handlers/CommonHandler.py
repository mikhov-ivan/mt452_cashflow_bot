import os
import telegram

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from Utils import Utils
from Structures import Type
from Structures import Format
from Structures import CmdPrefix
from Structures import TypePrefix


class CommonHandler:
    @classmethod
    def cgs(cls, bot, update):
        Utils.log_update(update)
        msg = "Список доступных <b>групп</b>"
        markup = cls.get_inline_keyboard(Type.CATEGORY_GROUP)
        update.message.reply_text(msg, reply_markup=markup, parse_mode="HTML")
       
    @classmethod 
    def cats(cls, bot, update):
        Utils.log_update(update)
        msg = "Список доступных <b>категорий</b>"
        markup = cls.get_inline_keyboard(Type.CATEGORY)
        update.message.reply_text(msg, reply_markup=markup, parse_mode="HTML")
        
    @classmethod
    def trans(cls, bot, update):
        Utils.log_update(update)
        html = cls.get_list(Type.TRANSACTION)
        Utils.send(bot, update.message.chat_id, html)
    
    @classmethod
    def get_inline_keyboard(cls, type):
        if type == Type.CATEGORY_GROUP:
            response = Utils.db.get_category_groups()
        elif type == Type.CATEGORY:
            response = Utils.db.get_categories()
        elif type == Type.TRANSACTION:
            response = Utils.db.get_transactions()
        
        line = []
        keyboard = []
        markup = None
        if len(response):
            for row in response.values():
                button = InlineKeyboardButton(row.title, callback_data=row.code)
                if len(line) < 3:
                    line.append(button)
                else:
                    keyboard.append(line)
                    line = [button]
            
            if type == Type.CATEGORY:
                callback = "{}_{}_{}".format(CmdPrefix.CREATE.value, Type.TRANSACTION.value, row.ouid)
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
        
    @classmethod
    def get_list(cls, type):
        if type == Type.CATEGORY_GROUP:
            response = Utils.db.get_category_groups()
            template = "<b>{} category groups</b> are available:{}{}{}"
            
        elif type == Type.CATEGORY:
            response = Utils.db.get_categories()
            template = "<b>{} categories</b> are available:{}{}{}"
            
        elif type == Type.TRANSACTION:
            response = Utils.db.get_transactions()
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

