import telegram

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from Structures import Utils
from Structures import Type
from helpers.DBHelper import DBHelper


class GeneralHandler:
    def __init__(self):
        self.db = DBHelper()
    
    def start(self, bot, update):
        Utils.log("User {} {} started bot".format(update.effective_user["id"], update.message.from_user.first_name))
        
        keyboard = [[
            telegram.KeyboardButton('Groups'),
            telegram.KeyboardButton('Categories'),
            telegram.KeyboardButton('Transactions')]]
        
        markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        msg = "Hello, <b>{}</b>!".format(update.message.from_user.first_name)
        bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=markup, parse_mode="HTML")

        markup = self.get_keyboard(Type.CATEGORY_GROUP)
        update.message.reply_text("Main menu", reply_markup=markup)
    
    def get_keyboard(self, type):
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
        
