import os
import logging
from DBHelper import DBHelper

global logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger()

class Cashflow:
    def __init__(self):
        self.db = DBHelper()
        self.state = "main"
        
    def get_categories(self):
        return self.db.get_categories()

