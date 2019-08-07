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
    def __init__(self, ouid, execution_date, code, title):
        self.ouid = ouid
        self.execution_date = execution_date
        self.currency = code
        self.title = title

