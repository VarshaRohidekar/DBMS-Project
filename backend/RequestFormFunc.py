import mysql.connector
from mysql.connector import errorcode 
import config

# each supervisor's details along some project info

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
    
    
    
    # select supervisor_id, Fname, Lname, email, domain from Supervisor natural join Supervisor_Domains natural join Supervisor_years join Teacher where teacher_id=supervisor_id and batch=2025 and active_projects!=team_limit;
    
    # [(Fname, Lname, Email, (Current Domains) [(Domain, Problem Statement)])]
    
    


def insert_request(team_id, supervisor_ids, domain, idea):
    
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