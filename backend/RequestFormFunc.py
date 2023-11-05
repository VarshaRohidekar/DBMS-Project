import mysql.connector
from mysql.connector import errorcode 
from backend import config
# import config
from datetime import date

# each supervisor's details along some project info

def get_available_supervisors():
    
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
        'batch': date.today().year
    }
    
    cnx_cursor.execute("""with Current (teacher_id) as (select supervisor_id from Supervisor natural join Supervisor_years where batch=2025)
                          select teacher_id, Fname, Lname, email from Current natural join Teacher""", data)
    
    teachers_temp = cnx_cursor.fetchall()
    
    teachers = [list(i) for i in teachers_temp]
    
    for teacher in teachers:
        id=teacher[0]
        cnx_cursor.execute("""SELECT domain FROM Supervisor_Domains WHERE supervisor_id = %(id)s""", {'id': id})
        domains = cnx_cursor.fetchall()
        teacher.append(domains)
        cnx_cursor.execute("""SELECT domain, problem_statement FROM Project WHERE supervisor_id = %(id)s""", {'id': id})
        projects = cnx_cursor.fetchall()
        teacher.append(projects)
    
    cnx.close()
    
    # select supervisor_id, Fname, Lname, email, domain from Supervisor natural join Supervisor_Domains natural join Supervisor_years join Teacher where teacher_id=supervisor_id and batch=2025 and active_projects!=team_limit;
    
    # [(Fname, Lname, Email, (Current Domains) [(Domain, Problem Statement)])]
    
    return teachers
    


def insert_request(team_id, supervisor_ids, domain, idea):
    
    try:
        cnx = mysql.connector.connect(**config)

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
    
    
get_available_supervisors()