import mysql.connector
from mysql.connector import errorcode 
from backend.table_population import config
import datetime
# from queries import selects

def get_supervisor_info(id):
    
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
    
    cnx_cursor.execute("""SELECT * FROM supervisor_projects WHERE supervisor_id=%(id)s""", {'id':id})
    result=cnx_cursor.fetchone()
    print(result)
    cnx_cursor.execute("""SELECT * FROM Supervisor_years WHERE supervisor_id=%(id)s and batch=%(year)s""", {'id': id, 'year': datetime.datetime.now().year + 2})
    activeSupervisor = False 
    if cnx_cursor.fetchone() is not None:
        activeSupervisor = True
    if result is None:
        return (activeSupervisor, None, None, None, None)
    else:
        (supervisor_id, team_limit, active_projects, accepted_requests) = result
        return (activeSupervisor, team_limit, active_projects, accepted_requests)

def get_completed_projects(s_id):

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
    cnx_cursor.execute("""SELECT * FROM Project WHERE supervisor_id=%(id)s and end_d is not NULL""", {'id': s_id})

    x = cnx_cursor.fetchall()
    cnx.close()
    if x is None:
        print("this teacher does not have any completed projects")
    

    return x

def get_requests(supervisor_id):
    
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
    
    result = cnx_cursor.execute("""SELECT request_id,team_id,interested_domain,idea,req_status
                             FROM Request
                             WHERE supervisor_id = %(id)s and req_status=0""", {'id': supervisor_id})
    
    content = cnx_cursor.fetchall()
    cnx.close()
    
    return content

# get_requests()

def modify_request(action, request_id):
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
    
    cnx_cursor.execute("""UPDATE Request SET req_status = %(action)s WHERE request_id = %(request_id)s""", {'action': action, 'request_id': request_id})
    
    cnx.close()

def get_projects(userid):
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

    cnx_cursor.execute("""SELECT * FROM Project WHERE supervisor_id=%(id)s and end_d is NULL""", {'id': userid})

    result = cnx_cursor.fetchall()

    cnx.close()
    return result

def end_project(project_id):
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

    cnx_cursor.execute("""UPDATE Project SET end_d=%(d)s where project_id=%(id)s""", {'d': datetime.datetime.now().strftime("%Y-%m-%d"), 'id': project_id})

    # cnx_cursor.execute("""CALL decrement_active_projects(%(id)s)""", {'id': project_id})

    cnx.close()
    return

def get_reviews(supervisor_id):
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
    # need all the active projects under the supervisor and their corresponding reviews for the current phase
    #f with reviewed_projects (project_id, phase) as 
    # ( select project_id, phase from  (select project_id, cur_phase as phase from Project) as projects natural join (select * from Review) as reviews ) 
    # select project_id, cur_phase as phase from Project 
    # where (project_id, cur_phase) not in (select project_id, phase from reviewed_projects);
    # need to only send those projects that don't have grade yet    
    # cnx_cursor.execute("""SELECT project_id, cur_phase FROM Project WHERE supervisor_id=%(id)s""", {'id': supervisor_id})
    
    cnx_cursor.execute("""WITH reviewed_projects (project_id, phase)
                          AS (
                              SELECT project_id, phase 
                              FROM
                              (SELECT project_id, cur_phase as phase FROM Project) AS projects
                              NATURAL JOIN
                              (SELECT * FROM Review) as reviews
                              )
                           SELECT project_id, cur_phase as phase
                           FROM Project
                           WHERE supervisor_id = %(id)s AND (project_id, cur_phase) NOT IN (SELECT project_id, phase FROM reviewed_projects)""", {'id': supervisor_id})
    projects = cnx_cursor.fetchall()
    print(projects)
    # get reviews for cur_phase
    reviews = []
    for i in projects:
        reviews.append([i[0], i[1]])
        cnx_cursor.execute("""SELECT reviewer_id, feedback FROM Reviewed_by WHERE project_id = %(id)s AND phase = %(phase)s""", {'id': i[0], 'phase': i[1]})
        content = cnx_cursor.fetchall()
        reviews[-1].append(content)

    cnx.close()

    # [[project_id, phase, (reveiws)]]

    return reviews

def assign_grade(data):
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
    
    cnx_cursor.execute("""INSERT INTO Review (project_id, phase, grade) VALUES (%(project_id)s, %(phase)s, %(grade)s)""", data)
    
    cnx.close()

    return