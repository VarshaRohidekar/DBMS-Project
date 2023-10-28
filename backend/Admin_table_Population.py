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

with open("datasets/Admin.csv", mode='r') as file:
    csvfile = csv.reader(file)
    
    for (admin_id,pswd,email) in csvfile:
        admin_data = {
            'admin_id' : admin_id,
            'pswd' : pswd,
            'email' : email
        }
        cnx_cursor.execute(insert_admin, admin_data)

cnx.close()