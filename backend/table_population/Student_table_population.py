import mysql.connector
from mysql.connector import errorcode 
# from backend.config import config 
import sys
import os 
queries_path = os.path.abspath("../queries")
sys.path.append(queries_path)
backend_path = os.path.abspath("../../backend")
sys.path.append(backend_path)
# from inserts import * 
import inserts
import config
import csv

def show_tables(c):
    c.execute("show tables")
    for x in c:
        print(x)
    return

def display_table_contents(c, table_name):
    # print(table_name)
    try:    
        result = c.execute("SELECT * FROM " + table_name)
    except:
        print("unable to execute")
    else:
        rows = c.fetchall()
        for row in rows:
            print(row)
    return

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
show_tables(cnx_cursor)

with open("../datasets/Student.csv", mode='r') as file:
    csvfile = csv.reader(file)
    
    for (srn, fname, lname, sem, pswd, cgpa, year, email) in csvfile:
        student_data = {
            'srn' : srn,
            'pswd' : pswd,
            'Fname' : fname,
            'Lname' : lname,
            'email' : email,
            'semester' : sem,
            'cgpa' : cgpa,
            'outgoing_year' : year
        }

        cnx_cursor.execute(inserts.insert_student, student_data)

cnx.close()