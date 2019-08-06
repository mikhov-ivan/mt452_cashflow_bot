import telegram
from telegram.ext import Updater

global bot
global APP_URL
global APP_KEY
global BOT_URL
global TOKEN

APP_URL = 'https://mt452-cashflow-bot.herokuapp.com/'
APP_KEY = '4276eb911ca3133611d23040e1ee439ea21738932dda94e502f37fae0497'
BOT_URL = 'https://api.telegram.org/bot861062365:AAEq3evcJCE5nZCSclev9Z8ki-cAjwdTUqQ/'
TOKEN = '861062365:AAEq3evcJCE5nZCSclev9Z8ki-cAjwdTUqQ'


def start(bot, update):
    update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))

if __name__ == '__main__':
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.start_polling()
    updater.idle()
