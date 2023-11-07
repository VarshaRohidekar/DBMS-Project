import mysql.connector
from mysql.connector import errorcode 
from backend import config
import sys
import os 
queries_path = os.path.abspath("queries/selects.py")
sys.path.append(queries_path)
# import selects
# from queries.selects import * 


# returning hasTeam and hasResume values in the get_student_details function itself

cnx = None

def log_in():
    global cnx
    try:
        cnx = mysql.connector.connect(**config.config)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return "Something is wrong with your user name or password"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            return "Database does not exist"
        else:
            return err
    else:
        print("connected to", cnx._database)        #cnx._database -- value of current database   

def get_admin_details(id):
    global cnx
    cnx_cursor = cnx.cursor()
    
    result = cnx_cursor.execute(""" SELECT email FROM Admin where admin_id = %(id)s""", {'id' : id})
    (email) = cnx_cursor.fetchone()
    # cnx.close()
    
    return email

def get_student_details():
    global cnx
    cnx_cursor = cnx.cursor()
    # result = cnx_cursor.execute(selects.select_students, {'sem': semester})
    result = cnx_cursor.execute("""SELECT srn, Fname, Lname, semester, cgpa, email, outgoing_year, team_id
                                   FROM Student
                                   """)
    data = cnx_cursor.fetchall()
    column_names = [desc[0] for desc in cnx_cursor.description]
    
    return (data, column_names)

def get_teacher_details():
    global cnx
    cnx_cursor = cnx.cursor()
    # result = cnx_cursor.execute(selects.select_teachers)
    result = cnx_cursor.execute("""SELECT teacher_id, Fname, Lname, email, floor, cabin_no FROM Teacher""")
    data = cnx_cursor.fetchall()
    column_names = [desc[0] for desc in cnx_cursor.description]
   
    return (data, column_names)

def get_query(query):
    global cnx 
    cnx_cursor = cnx.cursor()
    try:
        cnx_cursor.execute(query)
        data = cnx_cursor.fetchall()
        if data != []:
            column_names = [desc[0] for desc in cnx_cursor.description]
        else:
            x = query.split()[0]
            return (x+" successful").upper()
    except:
            return "INCORRECT QUERY"
    else:
        return (data, column_names)

def log_out():
    global cnx
    cnx.close()
    cnx=None