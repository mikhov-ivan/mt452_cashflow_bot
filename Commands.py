import os
import re

from Utils import AppData
from Utils import TgUtils
from Utils import ServerUtils
from Structures import Types
from Structures import Formats
from Structures import Regexps
from Structures import Actions
from Structures import ResponseTypes


class CmdGet(object):
    @classmethod
    def get_list(cls, bot, update, is_callback=False):
        ServerUtils.log_update(update)
        cmd = update.message.text
        args = cmd.split(" ")
        is_ok = True
        
        ouid = None
        type = None
        group_ouid = None
        category_ouid = None
        transaction_ouid = None
        
        for i in range(0, len(args)):
            if args[i] == "-type": type = args[i+1]
            if args[i] == "-ouid": ouid = args[i+1]
            if args[i] == "-g": group_ouid = args[i+1]
            if args[i] == "-c": category_ouid = args[i+1]
            if args[i] == "-t": transaction_ouid = args[i+1]
        
        response = None
        response_type = None
        if type == Types.GROUP.value:
            if ouid:
                pass
            else:
                msg = "Список доступных <b>групп</b>"
                response = cls.get_all_groups()
                response_type = ResponseTypes.INLINE_KEYBOARD
        elif type == Types.CATEGORY.value:
            if ouid:
                pass
            else:
                msg = "Список доступных <b>категорий</b>"
                response = cls.get_all_categories(group_ouid)
                response_type = ResponseTypes.INLINE_KEYBOARD
        elif type == Types.TRANSACTION.value:
            if ouid:
                pass
            else:
                msg = "Список <b>транзакций</b>"
                response = cls.get_all_transactions(category_ouid)
                response_type = ResponseTypes.HTML
        
        if response:
            if response_type == ResponseTypes.INLINE_KEYBOARD:
                if is_callback:
                    bot.edit_message_text(
                        chat_id=update.message.chat_id,
                        message_id=update.message.message_id,
                        text=msg,
                        reply_markup=response,
                        parse_mode="HTML")
                else:
                    update.message.reply_text(
                        msg,
                        reply_markup=response,
                        parse_mode="HTML")
            elif response_type == ResponseTypes.HTML:
                if is_callback:
                    bot.edit_message_text(
                        chat_id=update.message.chat_id,
                        message_id=update.message.message_id,
                        text=response,
                        parse_mode="HTML")
                else:
                    TgUtils.send(bot, update, response)
        else:
            TgUtils.send(bot, update, "Что-то пошло не так")
    
    @classmethod
    def get_all_groups(cls):
        if not "get_all_groups" in AppData.keyboards:
            keyboard_items = {}
            response = AppData.db.get_category_groups()
            for cg in response.values():
                # Get all available categories in the selected group
                callback = "get_list -type category -g {}".format(cg.ouid)
                keyboard_items[cg.title] = callback
            keyboard = TgUtils.build_keyboard(keyboard_items)
            AppData.keyboards["get_all_groups"] = keyboard
        keyboard = AppData.keyboards["get_all_groups"]
        return keyboard
    
    @classmethod
    def get_all_categories(cls, group_ouid):
        keyboard_code = "get_all_categories"
        if group_ouid:
            keyboard_code = "get_all_categories_group_{}".format(group_ouid)
        
        if not "get_all_categories" in AppData.keyboards:
            keyboard_items = {}
            response = AppData.db.get_categories(group_ouid=group_ouid)
            for c in response.values():
                # Get all available categories in the selected group
                callback = "get_list -type transaction -c {}".format(c.ouid)
                keyboard_items[c.title] = callback
            keyboard = TgUtils.build_keyboard(keyboard_items)
            AppData.keyboards[keyboard_code] = keyboard
        keyboard = AppData.keyboards[keyboard_code]
        return keyboard
    
    @classmethod
    def get_all_transactions(cls, category_ouid):
        response = AppData.db.get_transactions(category_ouid=category_ouid)
        template = "<b>Транзакций</b> записано: {}{}{}{}"
        
        if len(response) > 0:
            msg = ""
            for row in response.values():
                date = row.execution_date.strftime(Formats.DATETIME.value)
                msg += "{}{}".format(
                    "<b>{}</b>: {} {}{}".format(date, row.amount, row.currency, os.linesep),
                    "{}{}{}".format(row.title, os.linesep, os.linesep))
            html = template.format(len(response), os.linesep, os.linesep, msg)
        else:
            html = "Ничего не найдено"
        return html


class CmdCreate(object):
    @classmethod
    def create(cls):
        pass
    
    @classmethod
    def create_transaction(cls, bot, update):
        ServerUtils.log_update(update)
        cmd = update.message.text
        
        pattern = re.compile(Regexps.NUMBER.value)
        if pattern.match(cmd):
            new_ouid = AppData.db.create_transaction(amount=cmd)
            if new_ouid > -1:
                response = AppData.db.get_transactions(ouid=new_ouid)
                template = "<b>Транзакция</b> создана:{}{}"
        
                if len(response) == 1:
                    msg = ""
                    row = response[new_ouid]
                    date = row.execution_date.strftime(Formats.DATETIME.value)
                    msg += "{}{}".format(
                        "<b>{}</b>: {} {}{}".format(date, row.amount, row.currency, os.linesep),
                        "{}".format(row.title))
                    html = template.format(os.linesep, msg)
                    TgUtils.send(bot, update, response)
                else:
                    TgUtils.send(bot, update, "Что-то пошло не так")
            else:
                TgUtils.send(bot, update, "Что-то пошло не так")

