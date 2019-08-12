import telegram

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from Structures import Utils
from Structures import Type
from helpers.DBHelper import DBHelper


def main_menu_keyboard():
  keyboard = [
        [InlineKeyboardButton('Option 1', callback_data='m1'),
         InlineKeyboardButton('Option 2', callback_data='m2'),
         InlineKeyboardButton('Option 2', callback_data='m2'),
         InlineKeyboardButton('Option 2', callback_data='m2')],
    
        [InlineKeyboardButton('Option 2', callback_data='m2'),
         InlineKeyboardButton('Option 2', callback_data='m2'),
         InlineKeyboardButton('Option 2', callback_data='m2'),
         InlineKeyboardButton('Option 2', callback_data='m2')],
        
        [InlineKeyboardButton('Option 3', callback_data='m3'),
         InlineKeyboardButton('Option 2', callback_data='m2'),
         InlineKeyboardButton('Option 2', callback_data='m2'),
         InlineKeyboardButton('Option 2', callback_data='m2')]]
  return InlineKeyboardMarkup(keyboard)


class GeneralHandler:
    def __init__(self):
        self.db = DBHelper()
    
    def start(self, bot, update):
        Utils.log("User {} {} started bot".format(update.effective_user["id"], update.message.from_user.first_name))
        Utils.send(bot, update.message.chat_id, "Hello, <b>{}</b>!".format(update.message.from_user.first_name))
        #update.message.reply_text("Main menu", reply_markup=main_menu_keyboard())
        markup = self.list_keyboard(Type.CATEGORY_GROUP)
        update.message.reply_text("Main menu", reply_markup=markup)
        
        kb = [[
            telegram.KeyboardButton('Groups'),
            telegram.KeyboardButton('Categories'),
            telegram.KeyboardButton('Transactions')]]
        
        kb_markup = telegram.ReplyKeyboardMarkup(kb,
                         resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id,
                         text="your message",
                         reply_markup=kb_markup)


        # query = update.callback_query
        # bot.edit_message_text(
            # chat_id=query.message.chat_id,
            # message_id=query.message.message_id,
            # text="asdasd",
            # reply_markup=main_menu_keyboard())
    
    def list_keyboard(self, type):
        if type == Type.CATEGORY_GROUP:
            response = self.db.get_category_groups()
        elif type == Type.CATEGORY:
            response = self.db.get_categories()
        elif type == Type.TRANSACTION:
            response = self.db.get_transactions()
        
        i = 0
        line = 0
        keyboard = [[]]
        if len(response):
            for row in response:
                if i < 4:
                    keyboard[line].append(InlineKeyboardButton(row.title, callback_data=row.code))
                    i += 1
                else:
                    keyboard.append([])
                    line += 1
                    i = 0
            return InlineKeyboardMarkup(keyboard)
        else:
            return None
        
