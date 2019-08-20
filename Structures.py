import os
import datetime
from enum import Enum


class Formats(Enum):
    LOG                 = "%(asctime)s %(levelname)s: %(message)s"
    TG_BREAK            = "#TGBR#"
    DATE                = "%d.%m.%Y"
    TIME                = "%H:%m"
    DATETIME            = "%d.%m.%Y %H:%m"
    DATETIME_DB         = "%Y-%m-%d %H:%M:%S"


class Defaults(Enum):
    CURRENCY = 2


class Constants(Enum):
    RUB_OUID = 1
    EUR_OUID = 2


class Regexps(Enum):
    NUMBER = "^([0-9]*\.?[0-9]+)$"


class Types(Enum):
    GROUP           = "group"
    CATEGORY        = "category"
    TRANSACTION     = "transaction"


class ResponseTypes(Enum):
    INLINE_KEYBOARD = "inline_keyboard"
    HTML            = "html"


class CategoryGroup:
    def __init__(self, ouid, code, title):
        self.ouid = ouid
        self.code = code
        self.title = title


class Category:
    def __init__(self, ouid, code, title):
        self.ouid = ouid
        self.code = code
        self.title = title


class Transaction:
    def __init__(self, ouid, execution_date, code, amount, title):
        self.ouid = ouid
        self.execution_date = datetime.datetime.strptime(str(execution_date), Formats.DATETIME_DB.value)
        self.currency = code
        self.amount = amount
        self.title = title

