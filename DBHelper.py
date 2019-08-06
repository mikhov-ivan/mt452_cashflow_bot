import logging
import mysql.connector
from mysql.connector import errorcode

global DB_NAME
global TABLES

global db
global logger

DB_NAME = 'akakich_telegram'

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger()

class DBHelper:
    def __init__(self):
        self.telegram_db = mysql.connector.connect(
            user='akakich_telegram',
            password='mt452cashflowbot',
            host='141.8.193.216',
            database=DB_NAME
        )
        
    def __del__(self):
        self.telegram_db.close()
        
    def get_categories(self):
        try:
            response = array()
            query = "SELECT * FROM category"
            cursor = self.telegram_db.cursor()
            cursor.execute(query)
            for (ouid, code, title) in cursor:
                response[ouid] = {'code': code, 'title': title}
            cursor.close()
            logger.info('OK')
        except mysql.connector.Error as err:
            logger.info(err.msg)
        return response

