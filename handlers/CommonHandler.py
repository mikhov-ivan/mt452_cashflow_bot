import logging
import Structures

from Structures import Utils
from helpers.DBHelper import DBHelper


class CommonHandler:
    def __init__(self):
        self.db = DBHelper()
        
    def cgs(self, bot, update):
        Utils.log_update(update)
        html = self.get_list(Type.CATEGORY_GROUP)
        Utils.send(bot, update.message.chat_id, html)
        
    def cats(self, bot, update):
        Utils.log_update(update)
        html = self.get_list(Type.CATEGORY)
        Utils.send(bot, update.message.chat_id, html)
        
    def trans(self, bot, update):
        Utils.log_update(update)
        html = self.get_list(Type.TRANSACTION)
        Utils.send(bot, update.message.chat_id, html)
        
    def get_list(self, type):
        if type == Type.CATEGORY_GROUP:
            response = self.db.get_category_groups()
            template = "<b>{} category groups</b> are available:{}{}{}"
            
        elif type == Type.CATEGORY:
            response = self.db.get_categories()
            template = "<b>{} categories</b> are available:{}{}{}"
            
        elif type == Type.TRANSACTION:
            response = self.db.get_transactions()
            template = "<b>{} transactions</b> recorded:{}{}{}"
        
        if len(response) > 0:
            msg = ""
            for row in response.values():
                if type == Type.CATEGORY_GROUP or type == Type.CATEGORY:
                    msg += "{} /{} /{}{}".format(
                        row.title,
                        "{}{}{}".format(CmdPrefix.EDIT.value, TypePrefix[type.name].value, row.ouid),
                        "{}{}{}".format(CmdPrefix.DELETE.value, TypePrefix[type.name].value, row.ouid),
                        os.linesep)
                elif type == Type.TRANSACTION:
                    date = row.execution_date.strftime(DATETIME_FORMAT)
                    msg += "{}{}".format(
                        "<b>{}</b>: {} {}{}".format(date, row.amount, row.currency, os.linesep),
                        "{} {} {}{}{}".format(
                            row.title, 
                            "/{}{}{}".format(CmdPrefix.EDIT.value, TypePrefix[type.name].value, row.ouid),
                            "/{}{}{}".format(CmdPrefix.DELETE.value, TypePrefix[type.name].value, row.ouid),
                            os.linesep,
                            os.linesep))
            html = template.format(len(response), os.linesep, os.linesep, msg)
        else:
            html = "List is empty"
        return html

