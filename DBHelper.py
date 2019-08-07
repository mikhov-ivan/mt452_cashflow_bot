import os
import logging
import mysql.connector
from mysql.connector import errorcode
from Structures import Category

global DB_NAME
global TABLES

global logger

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger()

class DBHelper:
    def connect(self):
        return mysql.connector.connect(
            user=os.environ.get('DB_USER', None),
            password=os.environ.get('DB_PASSWORD', None),
            host=os.environ.get('DB_HOST', None),
            database=os.environ.get('DB_NAME', None)
        )
        
    def disconnect(self, cnx):
        cnx.close()
    
    def get_category_groups(self):
        try:
            query = (
                " SELECT"
                "    cg.ouid AS category_group_ouid,"
                "    cg.code AS category_group_code,"
                "    cg_msg.ru AS category_group_title"
                " FROM category cg"
                "    INNER JOIN msg cg_msg ON cg_msg.OUID = cg.title_msg_ouid"
                " ORDER BY c_msg.ru"
            )
            
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
        return response
    
    def get_categories(self):
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
                " ORDER BY c_msg.ru"
            )
            
            response = {}
            cnx = self.connect()
            cursor = cnx.cursor()
            cursor.execute(query)
            for row in cursor:
                response[row[0]] = Category(row[0], row[1], row[2])
            cursor.close()
            self.disconnect(cnx)
        except mysql.connector.Error as err:
            logger.error(err.msg)
        return response
        
