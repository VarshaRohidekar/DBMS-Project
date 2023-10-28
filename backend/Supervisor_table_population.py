import mysql.connector
from mysql.connector import errorcode 
import config 
# from inserts import *
from backend import inserts

supervisor_info = [['T1ZXCVBNM7890',[2025], 4, 2, ['Natural Language Processing']], ['TQWERTYUIOP67', [2025], 4, 0, ['Machine Learning and Arrificial Intelligence']], ['TQRSTUVWX8901', [2024, 2025], 6, 3, ['Natural Language Processing', 'Machine Learning and Arrificial Intelligence'] ]]

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

for (id, years, limit, current, domains) in supervisor_info:
    cnx_cursor.execute(inserts.insert_supervisor, {'supervisor_id': id, 'team_limit': str(limit), 'active_projects' : str(current)})
    for year in years:
        cnx_cursor.execute(inserts.insert_supervisor_years, {'supervisor_id' : id, 'batch': str(year)})
    for domain in domains:
        cnx_cursor.execute(inserts.insert_supervisor_domain, {'supervisor_id': id, 'domain': domain})
    
    

display_table_contents(cnx_cursor, 'Supervisor')    
display_table_contents(cnx_cursor, 'Supervisor_years')

cnx_cursor.close()
