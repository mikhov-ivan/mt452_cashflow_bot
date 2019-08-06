import telegram
from telegram.ext import Updater

global bot
global APP_URL = 'https://mt452-cashflow-bot.herokuapp.com/'
global APP_KEY = '4276eb911ca3133611d23040e1ee439ea21738932dda94e502f37fae0497'
global TOKEN = 'bot861062365:AAEq3evcJCE5nZCSclev9Z8ki-cAjwdTUqQ'

# @app.route('/' + TOKEN, methods=['POST'])
# def webhook_handler():
    # if request.method == 'POST':
        # update = telegram.Update.de_json(request.get_json(force=True))
        # chat_id = update.message.chat.id
        # text = update.message.text.encode('utf-8')
        # bot.sendMessage(chat_id=chat_id, text=text)
    # return 'ok'

bot = telegram.Bot(token=TOKEN)

updater = Updater(TOKEN)
PORT = int(os.environ.get('PORT', '8443'))
updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN, key=APP_KEY)
updater.bot.set_webhook(APP_URL + TOKEN)
updater.idle()