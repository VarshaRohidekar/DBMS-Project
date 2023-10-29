import mysql.connector
from mysql.connector import errorcode 
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

with open("../datasets/Teacher.csv", mode='r') as file:
    csvfile = csv.reader(file)
    
    for (teacher_id, fname, lname, email, floor, cabin_no, pswd) in csvfile:
        teacher_data = {
            'teacher_id' : teacher_id,
            'pswd' : pswd,
            'Fname' : fname,
            'Lname' : lname,
            'email' : email,
            'floor' : floor,
            'cabin_no' : cabin_no
        }

        cnx_cursor.execute(inserts.insert_teacher, teacher_data)

cnx.close()