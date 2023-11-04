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


def validate_team(srn1, srn2, srn3, srn4):
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
        'srn1':srn1,
        'srn2':srn2,
        'srn3':srn3,
        'srn4':srn4
    }
    cnx_cursor.execute("""SELECT srn FROM Student WHERE srn in (%(srn1)s, %(srn2)s, %(srn3)s, %(srn4)s) and team_id is NULL and semester>=5""", data)
    srns = cnx_cursor.fetchall()
    cnx.close()
    
    if len(srns) != 4:
        # print(len(srns))
        return False 
    else:
        # print(len(srns))
        return True

def add_team(srn1, srn2, srn3, srn4, teamName):
    
    srns = [srn1, srn2, srn3, srn4]
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
    try:
        cnx_cursor.execute("""INSERT INTO Team (team_name) VALUES (%(teamName)s)""", {'teamName': teamName})
        # cnx_cursor.execute(selects.select_team_id, {'teamName': teamName})
        # team_id = cnx_cursor.fetchone()[0]
        team_id = cnx_cursor.lastrowid
        print(team_id)
        info = {
            'team_id': team_id,
            'srn1': srn1,
            'srn2':srn2,
            'srn3':srn3,
            'srn4':srn4
        }
        cnx_cursor.execute("""UPDATE Student
                            SET team_id = %(team_id)s
                            WHERE srn in (%(srn1)s, %(srn2)s, %(srn3)s, %(srn4)s)""", info)
        
        cnx.close()
    
    except:
        # need to handle these errors properly
        
        return (False, None) 
    else:
        return (True, team_id)


add_team('PES1UG04MVE50', 'PES1UG0K93E04', 'PES1UG0W9A363', 'PES1UG0Z51234', 'trialTeam')
v = validate_team('PES1UG04MVE50', 'PES1UG0K93E04', 'PES1UG0W9A363', 'PES1UG0Z51234')
print(v)