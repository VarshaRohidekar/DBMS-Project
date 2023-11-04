import mysql.connector
from mysql.connector import errorcode 
import config

def get_available_supervisors():
    
    try:
        cnx = mysql.connector.connect(**config)

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
    
    

def insert_request(team_id, supervisor_id, domain, idea):
    
    try:
        cnx = mysql.connector.connect(**config)

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