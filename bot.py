import requests
import telegram
from telegram.ext import Updater
from bottle import Bottle, response, request as bottle_request

global bot
global APP_URL
global APP_KEY
global BOT_URL
global TOKEN

APP_URL = 'https://mt452-cashflow-bot.herokuapp.com/'
APP_KEY = '4276eb911ca3133611d23040e1ee439ea21738932dda94e502f37fae0497'
BOT_URL = 'https://api.telegram.org/bot861062365:AAEq3evcJCE5nZCSclev9Z8ki-cAjwdTUqQ/'
TOKEN = '861062365:AAEq3evcJCE5nZCSclev9Z8ki-cAjwdTUqQ'


class BotHandlerMixin:
    def get_chat_id(self, data):
        chat_id = data['message']['chat']['id']
        return chat_id

    def get_message(self, data):
        message_text = data['message']['text']
        return message_text

    def send_message(self, prepared_data):
        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=prepared_data)


class TelegramBot(BotHandlerMixin, Bottle):
    def __init__(self, *args, **kwargs):
        super(TelegramBot, self).__init__()
        self.route('/', callback=self.post_handler, method="POST")

    def post_handler(self):
        data = telegram.Update.de_json(request.get_json(force=True))
        answer_data = self.prepare_data_for_answer(data)
        self.send_message(answer_data)
        return response

    def prepare_data_for_answer(self, data):
        message = self.get_message(data)
        answer = self.change_text_message(message)
        chat_id = self.get_chat_id(data)
        
        return {
            "chat_id": chat_id,
            "text": answer,
        }

    def change_text_message(self, text):
        return text[::-1]


if __name__ == '__main__':
    updater = Updater(TOKEN)
    PORT = int(os.environ.get('PORT', '5000'))
    updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN, key=APP_KEY)
    updater.bot.set_webhook(APP_URL + TOKEN)
    updater.idle()

    app = TelegramBot()
    app.run(host=(APP_URL + TOKEN), port=PORT)
