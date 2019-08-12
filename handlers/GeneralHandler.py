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
        msg = "User {} {} started bot".format(update.effective_user["id"]
        Utils.log(msg, update.message.from_user.first_name))
        
        keyboard = [[
            telegram.KeyboardButton('Groups'),
            telegram.KeyboardButton('Categories'),
            telegram.KeyboardButton('Transactions')]]
        
        markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        msg = "Hello, <b>{}</b>!".format(update.message.from_user.first_name)
        bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=markup, parse_mode="HTML")
        
