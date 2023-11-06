import mysql.connector
from mysql.connector import errorcode 
from backend import config
# import config
import sys
import os 
queries_path = os.path.abspath("queries/selects.py")
sys.path.append(queries_path)
# from queries.inserts import insert_team
# from selects import *

def team_info(team_id):

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
    cnx_cursor.execute("""SELECT * FROM Team WHERE team_id=%(team_id)s""", {'team_id':team_id})
    (team_id, team_name) = cnx_cursor.fetchone()
    
    cnx_cursor.execute("""SELECT srn, Fname, Lname, cgpa
                         FROM Student
                         WHERE team_id=%(team_id)s""", {'team_id':team_id})
    rows = cnx_cursor.fetchall()
    column_names = [desc[0] for desc in cnx_cursor.description]
    
    cnx_cursor.execute("""SELECT project_id FROM Project WHERE team_id=%(team_id)s""", {'team_id': team_id})
    content = cnx_cursor.fetchall()
    cnx_cursor.execute("""CALL cumulative(%(team_id)s)""", {'team_id': team_id})
    avg = cnx_cursor.fetchone()[1]
    print(content)
    hasProject = False
    if len(content) != 0:
        hasProject=True
    # if content is not None:
    print(hasProject)
    
    cnx.close()
    for row in rows:
        print(row)   
    
    return (team_id, team_name, rows, column_names, hasProject, avg)


def get_requests(team_id):
    
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
    
    cnx_cursor.execute("""SELECT request_id, Fname, Lname, interested_domain, idea, req_status FROM Request join Teacher WHERE team_id=%(id)s and supervisor_id=teacher_id""", {'id': team_id})
    result = cnx_cursor.fetchall()
    cnx.close()
    
    return result

# team_info(3)