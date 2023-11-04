import mysql.connector
from mysql.connector import errorcode 
# from backend.config import config 
import sys
import os 
queries_path = os.path.abspath("../queries")
sys.path.append(queries_path)
backend_path = os.path.abspath("../../backend")
sys.path.append(backend_path)
from TeamFormFunc import add_team
# from queriesinserts import * 
import inserts
import config

teams = [[('PES1UG0K93E04', 'PES1UG3BHYF64', 'PES1UG4R9YME2', 'PES1UG6EAZ187', 'asdfasdf'), 'TQRSTUVWX8901', 'Natural Language Processing', 'sdfghjkl'], 
         [('PES1UG9ZMOC13', 'PES1UGAI4V831', 'PES1UGB5WY781', 'PES1UGB5ZO833', 'asdfsad'), 'TQRSTUVWX8901', 'Machine Learning and Arrificial Intelligence', 'asdfghjkl']]


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
# show_tables(cnx_cursor)

for row in teams:
    print(*(row[0]))
    (value, team_id)=add_team(*(row[0]))
    print(team_id)
    data={
        'team_id':team_id,
        'supervisor_id':row[1],
        'cur_phase':3,
        'domain':row[2],
        'statement':row[3]
    }
    if value==True:
        cnx_cursor.execute("""INSERT INTO Project (team_id, supervisor_id, cur_phase, domain, problem_statement) VALUES (%(team_id)s, %(supervisor_id)s, %(cur_phase)s, %(domain)s, %(statement)s)""", data)
        
    


cnx.close()