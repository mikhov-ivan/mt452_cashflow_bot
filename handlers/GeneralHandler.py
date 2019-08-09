from Structures import Utils


class GeneralHandler:
    def __init__(self):
        pass
    
    def start(self, bot, update):
        Utils.log("User {} {} started bot".format(update.effective_user["id"], update.message.from_user.first_name))
        Utils.send(bot, update.message.chat_id, "Hello, <b>{}</b>!".format(update.message.from_user.first_name))

