import os
import logging
import datetime
import mysql.connector

from datetime import date, datetime
from mysql.connector import errorcode

from Structures import Formats
from Structures import Defaults
from Structures import CategoryGroup
from Structures import Category
from Structures import Transaction

global DB_NAME
global TABLES
global logger

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger()

class DBHelper:
    def __init__(self):
        self.mode = os.getenv("MODE")
    
    def connect(self):
        return mysql.connector.connect(
            user=os.environ.get('DB_USER', None),
            password=os.environ.get('DB_PASSWORD', None),
            host=os.environ.get('DB_HOST', None),
            database=os.environ.get('DB_NAME', None))
        
    def disconnect(self, cnx):
        cnx.close()
    
    def get_category_groups(self):
        if self.mode == "prod":
            try:
                query = (
                    " SELECT"
                    "    cg.ouid AS category_group_ouid,"
                    "    cg.code AS category_group_code,"
                    "    cg_msg.ru AS category_group_title"
                    " FROM category_group cg"
                    "    INNER JOIN msg cg_msg ON cg_msg.OUID = cg.title_msg_ouid"
                    " ORDER BY cg_msg.ru")
                
                response = {}
                cnx = self.connect()
                cursor = cnx.cursor()
                cursor.execute(query)
                for row in cursor:
                    response[row[0]] = CategoryGroup(row[0], row[1], row[2])
                cursor.close()
                self.disconnect(cnx)
            except mysql.connector.Error as err:
                logger.error(err.msg)
        else:
            response = {
                "452": CategoryGroup("452", "test_group_1", "Group 1"),
                "453": CategoryGroup("453", "test_group_2", "Group 2"),
                "454": CategoryGroup("454", "test_group_3", "Group 3"),
                "455": CategoryGroup("455", "test_group_4", "Group 4")
            }
        return response
    
    def get_categories(self, ouid=None, group_ouid=None):
        if self.mode == "prod":
            try:
                query = (
                    " SELECT"
                    "    c.ouid AS category_ouid,"
                    "    c.code AS category_code,"
                    "    c_msg.ru AS category_title,"
                    "    cg.ouid AS category_group_ouid,"
                    "    cg.code AS category_group_code,"
                    "    cg_msg.ru AS category_group_title"
                    " FROM category c"
                    "    INNER JOIN msg c_msg ON c_msg.OUID = c.title_msg_ouid"
                    "    INNER JOIN category_group cg ON cg.OUID = c.category_group_ouid"
                    "        INNER JOIN msg cg_msg ON cg_msg.OUID = cg.title_msg_ouid"
                    " WHERE 1 = 1 {}"
                    " ORDER BY c_msg.ru")
                
                where = ""
                if group_ouid:
                    where += "AND cg.OUID = {}".format(group_ouid)
                query = query.format(where)
                logger.info("{}".format(group_ouid))
                
                response = {}
                cnx = self.connect()
                cursor = cnx.cursor()
                cursor = cnx.cursor()
                cursor.execute(query)
                for row in cursor:
                    response[row[0]] = Category(row[0], row[1], row[2])
                cursor.close()
                self.disconnect(cnx)
            except mysql.connector.Error as err:
                logger.error(err.msg)
        else:
            response = {
                "552": CategoryGroup("552", "test_category_1", "Category 1"),
                "553": CategoryGroup("553", "test_category_2", "Category 2"),
                "554": CategoryGroup("554", "test_category_3", "Category 3"),
                "555": CategoryGroup("555", "test_category_4", "Category 4")
            }
        return response
    
    def get_transactions(self, ouid=None, category_ouid=None):
        if self.mode == "prod":
            try:
                query = self.get_transaction_q(ouid, category_ouid)
                
                response = {}
                cnx = self.connect()
                cursor = cnx.cursor()
                cursor.execute(query)
                for row in cursor:
                    response[row[0]] = Transaction(row[0], row[1], row[3], row[4], row[5])
                cursor.close()
                self.disconnect(cnx)
            except mysql.connector.Error as err:
                logger.error(err.msg)
        else:
            response = {
                "652": Transaction("652", "2019-08-12 08:23:15", "€", 452, "Transaction 1"),
                "653": Transaction("653", "2019-08-13 09:23:15", "€", 452, "Transaction 2"),
                "654": Transaction("654", "2019-08-14 10:23:15", "€", 452, "Transaction 3"),
                "655": Transaction("655", "2019-08-14 11:23:15", "€", 452, "Transaction 4")
            }
        return response
    
    def get_transaction_totals(self, ouid=None, category_ouid=None):
        if self.mode == "prod":
            try:
                query = (
                    " SELECT"
                    "     t.transaction_execution_date,"
                    "     t.currency_ouid,"
                    "     SUM(t.transaction_amount) AS total_amount"
                    " FROM ({}) t"
                    " GROUP BY CAST(t.transaction_execution_date AS DATE), t.currency_ouid"
                    " ORDER BY t.transaction_execution_date").format(self.get_transaction_q(ouid, category_ouid))
                
                response = {}
                cnx = self.connect()
                cursor = cnx.cursor()
                cursor.execute(query)
                for row in cursor:
                    date = row[0].strftime(Formats.DATE.value)
                    if not date in response:
                        response[date] = {}
                    if not str(row[1]) in response[date]:
                        response[date][str(row[1])] = 0.0
                    response[date][str(row[1])] += row[2]
                cursor.close()
                self.disconnect(cnx)
            except mysql.connector.Error as err:
                logger.error(err.msg)
        else:
            response = {
                "12.08.2019": {"1": 100.5, "2": 0.0},
                "13.08.2019": {"1": 100.5, "2": 202.7},
                "14.08.2019": {"1": 780.5, "2": 452.0}
            }
        return response
    
    def get_transaction_q(self, ouid, category_ouid):
        query = (
            " SELECT"
            "    t.ouid AS transaction_ouid,"
            "    t.execution_date AS transaction_execution_date,"
            "    cur.ouid AS currency_ouid,"
            "    cur.symbol AS currency_symbol,"
            "    t.amount AS transaction_amount,"
            "    t.title AS transaction_title"
            " FROM transaction t"
            "    INNER JOIN currency cur ON cur.OUID = t.currency_ouid"
            "    LEFT JOIN category c ON c.OUID = t.category_ouid"
            " WHERE 1 = 1 {}"
            " ORDER BY t.execution_date, t.OUID")
        
        where = ""
        if ouid:
            where += " AND t.OUID = {}".format(ouid)
        if category_ouid:
            where += " AND c.OUID = {}".format(category_ouid)
        query = query.format(where)
        return query
    
    def create_transaction(self, data):
        if not "execution_date" in data or not data["execution_date"]:
            data["execution_date"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if not "category_ouid" in data or not data["category_ouid"]:
            data["category_ouid"] = ""
        
        if not "currency_ouid" in data or not data["currency_ouid"]:
            data["currency_ouid"] = Defaults.CURRENCY.value
        
        if not "amount" in data or not data["amount"]:
            data["amount"] = ""
        
        if not "title" in data or not data["title"]:
            data["title"] = "Назначение неизвестно"
        
        query = (
            " INSERT INTO transaction (execution_date, category_ouid, currency_ouid, amount, title)"
            " VALUES (%(execution_date)s, %(category_ouid)s, %(currency_ouid)s, %(amount)s, %(title)s)")
        
        if self.mode == "prod":
            try:
                cnx = self.connect()
                cursor = cnx.cursor()
                cursor.execute(query, data)
                new_ouid = cursor.lastrowid
                cnx.commit()
                cursor.close()
                self.disconnect(cnx)
                return new_ouid
            except mysql.connector.Error as err:
                logger.error(err.msg)
        else:
            logger.info(query)
            return 0
        return -1
    
    def update_transaction(self, data):
        pass
        
