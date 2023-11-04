import mysql.connector
from mysql.connector import errorcode 
import config
from queries import selects

def get_requests(supervisor_id):
    
    try:
        cnx = mysql.connector.connect(**config.config)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print("connected to", cnx._database)        #cnx._database -- value of current database
        
    cnx_cursor = cnx.cursor()
    
    result = cnx_cursor.execute(selects.select_pending_requests, {'id': supervisor_id})
    
    content = cnx_cursor.fetchall()
    cnx.close()
    
    if content is None:
        return ()
    
    print(content)

get_requests()