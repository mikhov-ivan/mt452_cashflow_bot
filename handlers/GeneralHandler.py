import telegram

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from Utils import Utils
from Structures import Type


class GeneralHandler:
    @classmethod
    def start(self, bot, update):
        msg = "User {} {} started bot"
        Utils.log(msg.format(update.effective_user["id"], update.message.from_user.first_name))
        
        keyboard = [[
            telegram.KeyboardButton('Groups'),
            telegram.KeyboardButton('Categories'),
            telegram.KeyboardButton('Transactions')]]
        
        markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        msg = "Привет, <b>{}</b>!".format(update.message.from_user.first_name)
        bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=markup, parse_mode="HTML")
        
