import mysql.connector
from mysql.connector import errorcode 
import config 
from inserts import * 
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

# srn = "PES1IG21CS695"
# pswd = "Happy123"
# Fname = "Vaishnavi"
# Lname = "Venu"
# email = "vaishnavigv.sn@gmail.com"
# semester = "5"
# cgpa = "8.55"
# outgoing_year = "2025" 


# student_data = {
#     'srn' : srn,
#     'pswd' : pswd,
#     'Fname' : Fname,
#     'Lname' : Lname,
#     'email' : email,
#     'semester' : semester,
#     'cgpa' : cgpa,
#     'outgoing_year' : outgoing_year
# }

# cnx_cursor.execute(insert_student, student_data)
# display_table_contents(cnx_cursor, "Student")
# cnx_cursor.execute("delete from Student")
# Student = "Student"

# try:
#     cnx_cursor.execute("SELECT * FROM " + Student)
# except:
#     print("unable to execute")
# else:
#     for x in cnx_cursor:
#         print(x)

with open("datasets/Student.csv", mode='r') as file:
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

        cnx_cursor.execute(insert_student, student_data)

cnx.close()