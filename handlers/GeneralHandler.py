import telegram

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from Structures import Utils


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
        pass
    
    def start(self, bot, update):
        Utils.log("User {} {} started bot".format(update.effective_user["id"], update.message.from_user.first_name))
        Utils.send(bot, update.message.chat_id, "Hello, <b>{}</b>!".format(update.message.from_user.first_name))
        update.message.reply_text("Main menu", reply_markup=main_menu_keyboard())
        
        kb = [[
            telegram.KeyboardButton('GRP'),
            telegram.KeyboardButton('CAT'),
            telegram.KeyboardButton('TRZ'),
            telegram.KeyboardButton('€'),
            telegram.KeyboardButton('$'),
            telegram.KeyboardButton('₽')]]
        
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

