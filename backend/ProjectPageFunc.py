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
import datetime
# from inserts import insert_team

def create_project(request_id):
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
        print("connected to", cnx._database)       
        
    cnx_cursor = cnx.cursor()

    cnx_cursor.execute("""SELECT * FROM Request WHERE request_id=%(id)s""", {'id': request_id})
    data = cnx_cursor.fetchone()
    print(data)

    # (9, 3, 'T1ZXCVBNM7890', 'Natural Language Processing', 'Here is my idea', 1)

    cnx_cursor.execute("""INSERT INTO Project (team_id, supervisor_id, start_d, cur_phase, domain, problem_statement) 
                          VALUES (%(team_id)s, %(supervisor_id)s, %(d)s, 1, %(domain)s, %(idea)s)""", {'team_id': data[1], 'supervisor_id': data[2], 'd': datetime.datetime.now().strftime("%Y-%m-%d"), 'domain': data[3], 'idea': data[4]})

    project_id = cnx_cursor.lastrowid

    # taken care of by the view
    # cnx_cursor.execute("""UPDATE Supervisor SET active_projects = active_projects +1 WHERE supervisor_id=%(id)s""", {'id':data[2]})

    return project_id


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
    cnx_cursor.execute("""SELECT project_id, team_id, supervisor_id, problem_statement, domain, start_d, end_d, cur_phase FROM Project WHERE team_id=%(team_id)s""", data)
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
