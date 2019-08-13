import os
import datetime
from enum import Enum


class Type(Enum):
    CATEGORY_GROUP = 1
    CATEGORY = 2
    TRANSACTION = 3


class TypePrefix(Enum):
    CATEGORY_GROUP      = "Groups"
    CATEGORY            = "Categories"
    TRANSACTION         = "Transactions"


class CmdPrefix(Enum):
    CREATE              = "Create"
    EDIT                = "Edit"
    DELETE              = "Delete"


class Format(Enum):
    LOG                 = "%(asctime)s %(levelname)s: %(message)s"
    DATETIME            = "%d.%m.%Y %H:%m"

class Cmd(Enum):
    START                       = "start"                                                               # /start
    GET_CATEGORY_GROUP_LIST     = TypePrefix.CATEGORY_GROUP.value                                       # /cg
    GET_CATEGORY_LIST           = TypePrefix.CATEGORY.value                                             # /c
    GET_TRANSACTION_LIST        = TypePrefix.TRANSACTION.value                                          # /t
    CREATE_TRANSACTION          = "{}{}".format(CmdPrefix.EDIT.value, TypePrefix.TRANSACTION.value)     # /ct
    EDIT_TRANSACTION            = "{}{}".format(CmdPrefix.EDIT.value, TypePrefix.TRANSACTION.value)     # /et452
    DELETE_TRANSACTION          = "{}{}".format(CmdPrefix.DELETE.value, TypePrefix.TRANSACTION.value)   # /dt452


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
        self.execution_date = datetime.datetime.strptime(str(execution_date), "%Y-%m-%d %H:%M:%S")
        self.currency = code
        self.amount = amount
        self.title = title

