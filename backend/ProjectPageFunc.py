'''
verify team
create team

or should verification be done in the create function


'''

import mysql.connector
from mysql.connector import errorcode 
from backend import config
# import config
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
    cnx_cursor.execute("""SELECT project_id, team_id, problem_statement, domain, start_d, end_d, cur_phase FROM Project WHERE team_id=%(team_id)s""", data)
    # print(cnx_cursor.fetchall())
    info = cnx_cursor.fetchall()[0]
    send = [i for i in info]
    print(info)
    cnx.close()
    if send[4] is None:
        send[4]=""
    if send[5] is None:
        send[5]=""
    
    return send
    
# display_projectdetails(23)
