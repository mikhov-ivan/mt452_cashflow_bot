import logging
import mysql.connector
from mysql.connector import errorcode

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
    MYSQL = None

    def __init__():
        MYSQL = mysql.connector.connect(
            user='akakich_telegram',
            password='mt452cashflowbot',
            host='141.8.193.216',
            database=DB_NAME
        )
        
    def __del__(self): 
        MYSQL.close()
    
    def setup(self):
        cursor = MYSQL.cursor()
        try:
            cursor.execute("USE {}".format(DB_NAME))
        except mysql.connector.Error as err:
            logger.info("Database {} does not exists.".format(DB_NAME))
            exit(1)
            
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                logger.info("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    logger.info("already exists.")
                else:
                    logger.info(err.msg)
            else:
                logger.info("OK")
        cursor.close()

