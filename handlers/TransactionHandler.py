from Structures import Utils
from Structures import TypePrefix
from helpers.DBHelper import DBHelper


class TransactionHandler:
    def __init__(self):
        self.db = DBHelper()
        self.splitter = TypePrefix.TRANSACTION.value
        
    def create(self, bot, update):
        pass
        
    def edit(self, bot, update):
        Utils.log_update(update)
        
        cmd = update.message.text
        parts = cmd.split(self.splitter)
        ouid = parts[len(parts) - 1]
        
        result = 1
        if result: Utils.send(bot, update.message.chat_id, "Edit transaction {}".format(ouid))
        else: Utils.send(bot, update.message.chat_id, "Transaction {} can not be edited".format(ouid))
        
    def delete(self, bot, update):
        Utils.log_update(update)
        
        cmd = update.message.text
        parts = cmd.split(self.splitter)
        ouid = parts[len(parts) - 1]
        
        result = 1
        if result: Utils.send(bot, update.message.chat_id, "Transaction {} was deleted".format(ouid))
        else: Utils.send(bot, update.message.chat_id, "Transaction {} can not be deleted".format(ouid))

