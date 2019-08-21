import os
import re
import datetime
import calendar

from Utils import AppData
from Utils import TgUtils
from Utils import ServerUtils

from Structures import Types
from Structures import Formats
from Structures import Defaults
from Structures import Constants
from Structures import Regexps
from Structures import ResponseTypes


class CmdGet(object):
    @staticmethod
    def get_list(bot, update, is_callback=False):
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
                response = CmdGet.get_all_groups()
                response_type = ResponseTypes.INLINE_KEYBOARD
        elif type == Types.CATEGORY.value:
            if ouid:
                pass
            else:
                msg = "Список доступных <b>категорий</b>"
                response = CmdGet.get_all_categories(group_ouid)
                response_type = ResponseTypes.INLINE_KEYBOARD
        elif type == Types.TRANSACTION.value:
            if ouid:
                pass
            else:
                msg = "Список <b>транзакций</b>"
                response = CmdGet.get_all_transactions(category_ouid)
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
    
    @staticmethod
    def get_all_groups():
        if not "get_all_groups" in AppData.keyboards:
            keyboard_items = {}
            response = AppData.db.get_category_groups()
            for cg in response.values():
                # Get all available categories in the selected group
                callback = "get_list -type {} -g {}".format(Types.CATEGORY.value, cg.ouid)
                keyboard_items[cg.title] = callback
            keyboard = TgUtils.build_keyboard(keyboard_items)
            AppData.keyboards["get_all_groups"] = keyboard
        keyboard = AppData.keyboards["get_all_groups"]
        return keyboard
    
    @staticmethod
    def get_all_categories(group_ouid):
        keyboard_code = "get_all_categories"
        if group_ouid:
            keyboard_code = "get_all_categories_group_{}".format(group_ouid)
        
        if not "get_all_categories" in AppData.keyboards:
            keyboard_items = {}
            response = AppData.db.get_categories(group_ouid=group_ouid)
            for c in response.values():
                # Get all available categories in the selected group
                callback = "get_list -type {} -c {}".format(Types.TRANSACTION.value, c.ouid)
                keyboard_items[c.title] = callback
            keyboard = TgUtils.build_keyboard(keyboard_items)
            AppData.keyboards[keyboard_code] = keyboard
        keyboard = AppData.keyboards[keyboard_code]
        return keyboard
    
    @staticmethod
    def get_all_transactions(category_ouid):
        response = AppData.db.get_transactions(category_ouid=category_ouid)
        totals = AppData.db.get_transaction_totals(category_ouid=category_ouid)
        template = "{}"
        
        if len(response) > 0:
            msg = ""
            current_date = None
            for row in response.values():
                date = row.execution_date.strftime(Formats.DATE.value)
                if not current_date or date != current_date:
                    if current_date:
                        msg += "{}".format(Formats.TG_BREAK.value)
                    current_date = date
                    weekday = calendar.day_abbr[datetime.datetime.strptime(date, Formats.DATE.value).weekday()]
                    
                    total_rub = 0.0
                    total_eur = 0.0
                    if "1" in totals[date]:
                        total_rub = totals[date]["1"]
                    if "2" in totals[date]:
                        total_eur = totals[date]["2"]
                    
                    msg += "<b>{} {}</b>:<code> {}{}</code> + <code>{}{}</code>".format(
                        date,
                        weekday,
                        ServerUtils.numeric_format(total_eur), "€",
                        ServerUtils.numeric_format(total_rub), "₽",
                        os.linesep)
                msg += "{}<code>{}{}</code> {}".format(
                    os.linesep,
                    ServerUtils.align_right(ServerUtils.numeric_format(row.amount)),
                    AppData.db.get_currency(row.currency).symbol,
                    row.title)
            html = template.format(msg)
        else:
            html = "Ничего не найдено"
        return html


class CmdCreate(object):
    @staticmethod
    def create_transaction(bot, update):
        ServerUtils.log_update(update)
        cmd = update.message.text
        pattern = re.compile(Regexps.NUMBER.value)
        if pattern.match(cmd):
            new_ouid = AppData.db.create_transaction({"amount": cmd})
            if new_ouid > -1:
                AppData.TRANSACTION_OUID = new_ouid
                CmdUpdate.reply_with_transaction(bot, update, False, int(new_ouid))
            else:
                TgUtils.send(bot, update, "Что-то пошло не так (1)")


class CmdUpdate(object):
    @staticmethod
    def update(bot, update, is_callback=False):
        ServerUtils.log_update(update)
        cmd = update.message.text
        args = cmd.split(" ")
        type = None
        
        data = {}
        for type in Types:
            data[type.value] = {}
        
        for i in range(0, len(args)):
            if args[i] == "-type":
                type = args[i+1]
            if args[i] == "-ouid":
                data[type]["ouid"] = args[i+1]
            if args[i] == "-currency":
                data[type]["currency_ouid"] = args[i+1]
        
        if type == Types.TRANSACTION.value:
            CmdUpdate.update_transaction(bot, update, data[type])
            CmdUpdate.reply_with_transaction(bot, update, is_callback, int(data[type]["ouid"]))
        
    @staticmethod
    def update_transaction(bot, update, data):
        type = Types.TRANSACTION.value
        AppData.db.update_transaction(data)
    
    @staticmethod
    def reply_with_transaction(bot, update, is_callback, ouid):
        response = AppData.db.get_transactions(ouid=ouid)
        if len(response) == 1:
            template = "{}"
            msg = ""
            data = response[ouid]
            date = data.execution_date.strftime(Formats.DATETIME.value)
            msg += "{}{}".format(
                "<b>{}</b>: {} {}{}".format(
                    date,
                    ServerUtils.numeric_format(data.amount),
                    AppData.db.get_currency(data.currency).symbol,
                    os.linesep),
                "{}".format(data.title))
            html = template.format(msg)
            
            keyboard_code = "transaction_{}".format(ouid)
            if not keyboard_code in AppData.keyboards:
                if data.currency == Constants.EUR_OUID.value:
                    switch_currency = Constants.RUB_OUID.value
                else:
                    switch_currency = Constants.EUR_OUID.value
                keyboard_items = {
                    "€ &rlarr; ₽": "update -type {} -ouid {} -currency {}".format(
                        Types.TRANSACTION.value,
                        AppData.TRANSACTION_OUID,
                        switch_currency),
                    "Категория": "get_list -type {}".format(Types.CATEGORY.value)}
                keyboard = TgUtils.build_keyboard(keyboard_items, 2, False)
                AppData.keyboards[keyboard_code] = keyboard
            keyboard = AppData.keyboards[keyboard_code]
            
            if is_callback:
                bot.edit_message_text(
                            chat_id=update.message.chat_id,
                            message_id=update.message.message_id,
                            text=html,
                            reply_markup=keyboard,
                            parse_mode="HTML")
            else:
                update.message.reply_text(
                    html,
                    reply_markup=keyboard,
                    parse_mode="HTML")
        else:
            TgUtils.send(bot, update, "Что-то пошло не так (2)")

