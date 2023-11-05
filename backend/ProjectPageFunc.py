'''
verify team
create team

or should verification be done in the create function


'''

import mysql.connector
from mysql.connector import errorcode 
# from backend import config
import config
import sys
import os 
queries_path = os.path.abspath("queries/inserts.py")
sys.path.append(queries_path)
# from inserts import insert_team


def display_projectdetails(team_id):
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
    data = {
        'team_id' : team_id
    }
    cnx_cursor.execute("""SELECT project_id,team_id,problem_statement,domain,start_d,end_d from Project where team_id="%(team_id)s""", data)
    srns = cnx_cursor.fetchall()
    print(srns)
    cnx.close()
