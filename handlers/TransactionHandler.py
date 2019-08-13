from Utils import Utils
from Structures import TypePrefix


class TransactionHandler:
    splitter = TypePrefix.TRANSACTION.value
        
    @classmethod
    def create(cls, bot, update):
        pass
    
    @classmethod
    def edit(cls, bot, update):
        Utils.log_update(update)
        
        cmd = update.message.text
        parts = cmd.split(cls.splitter)
        ouid = parts[len(parts) - 1]
        
        result = 1
        if result: Utils.send(bot, update.message.chat_id, "Edit transaction {}".format(ouid))
        else: Utils.send(bot, update.message.chat_id, "Transaction {} can not be edited".format(ouid))
        
    @classmethod
    def delete(cls, bot, update):
        Utils.log_update(update)
        
        cmd = update.message.text
        parts = cmd.split(self.splitter)
        ouid = parts[len(parts) - 1]
        
        result = 1
        if result: Utils.send(bot, update.message.chat_id, "Transaction {} was deleted".format(ouid))
        else: Utils.send(bot, update.message.chat_id, "Transaction {} can not be deleted".format(ouid))

