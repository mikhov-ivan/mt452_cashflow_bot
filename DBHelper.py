import logging
import mysql.connector
from mysql.connector import errorcode

global db
global logger

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

DB_NAME = 'akakich_telegram'

TABLES = {}
TABLES['employees'] = (
    "CREATE TABLE `employees` ("
    "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hire_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") ENGINE=InnoDB")


class DBHelper:
    def __init__(self):
        try:
            db = mysql.connector.connect(
                user='akakich_telegram',
                password='mt452cashflowbot',
                host="localhost",
                database=DB_NAME
            )
        except mysql.connector.Error as err:
            logger.info('Can not open connection to {}'.format(DB_NAME))
        
    def __del__(self):
        try:
            db.close()
        except mysql.connector.Error as err:
            logger.info('Can not close connection to {}'.format(DB_NAME))
    
    def setup(self):
        cursor = db.cursor()
        try:
            cursor.execute('USE {}'.format(DB_NAME))
        except mysql.connector.Error as err:
            logger.info('Database {} does not exists.'.format(DB_NAME))
            exit(1)
            
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                logger.info('Creating table {}: '.format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    logger.info('already exists.')
                else:
                    logger.info(err.msg)
            else:
                logger.info('OK')
        cursor.close()

