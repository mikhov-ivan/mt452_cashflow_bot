import logging
import mysql.connector
from mysql.connector import errorcode

global DB_NAME
global TABLES

global logger

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger()

class DBHelper:
    def connect(self):
        return mysql.connector.connect(
            user='akakich_telegram',
            password='mt452cashflowbot',
            host='141.8.193.216',
            database='akakich_telegram'
        )
        
    def disconnect(self, cnx):
        cnx.close()
        
    def get_categories(self):
        try:
            response = {}
            query = "SELECT * FROM category"
            cnx = self.connect()
            cursor = cnx.cursor()
            cursor.execute(query)
            for (ouid, code, title) in cursor:
                response[ouid] = {'ouid': ouid, 'code': code, 'title': title}
            cursor.close()
            self.disconnect(cnx)
            logger.info('OK')
        except mysql.connector.Error as err:
            logger.info(err.msg)
        return response

