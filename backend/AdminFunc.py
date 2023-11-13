import mysql.connector
from mysql.connector import errorcode 
from backend.table_population import config
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

def get_batches():
    global cnx 
    cnx_cursor=cnx.cursor()
    cnx_cursor.execute("""select distinct YEAR(start_d)+2 as batch from Project where end_d is NULL""")
    result=cnx_cursor.fetchall()
    return result

def assign_reviewers(batch):
    global cnx 
    cnx_cursor = cnx.cursor()  
    phase=None 
    cnx_cursor.execute("""SELECT DISTINCT cur_phase FROM Supervisor_years NATURAL JOIN Project WHERE batch=%(batch)s and YEAR(start_d)+2=batch""", {'batch': batch})
    phase = cnx_cursor.fetchone()[0]
    cnx_cursor.execute("""WITH project_phase_supervisor (project_id, phase, supervisor_id)
                          AS (SELECT project_id, cur_phase, supervisor_id FROM Project WHERE cur_phase=%(phase)s)
                          SELECT project_id, domain, problem_statement, teacher_id, Fname, Lname, email
                          FROM (
                            SELECT teacher_id, project_id, phase, supervisor_id, ROW_NUMBER() over (PARTITION BY project_id, phase ORDER BY RAND()) AS rnk
                            FROM Teacher join project_phase_supervisor
                            WHERE teacher_id!=supervisor_id) AS rnked
                          NATURAL JOIN
                          Teacher
                          NATURAL JOIN
                          Project
                          WHERE rnk <=2""", {'phase': phase})
    result=cnx_cursor.fetchall()
    # print("assign reviewers result: ", result)
    project_set=set([i[:3] for i in result])
    # print(project_set)
    reviewer_list = []
    for i in project_set:
            # print(i)
        reviewer_list.append([i])
        l = [j[3:] for j in result if j[0]==i[0]]
        reviewer_list[-1].append(l)    
    
    # for i in result:
    # print(reviewer_list)
    
    return phase, reviewer_list
    
# with temp_phase (project_id, phase, supervisor_id) as (select project_id, cur_phase, supervisor_id from Project where cur_phase=1) 
# select * from (select teacher_id, project_id, phase, supervisor_id, ROW_NUMBER() over (partition by project_id, phase order by RAND()) 
# as rnk from Teacher join temp_phase
# where teacher_id!=supervisor_id) as rnked where rnk <=2;    

# with temp_phase (project_id, phase, supervisor_id) 
# as (select project_id, cur_phase, supervisor_id from Project where cur_phase=1) 
# select project_id, phase, teacher_id, Fname, Lname, email 
# from (select teacher_id, project_id, phase, supervisor_id, ROW_NUMBER() over (partition by project_id, phase order by RAND()) as rnk 
#   from Teacher join temp_phase 
#   where teacher_id!=supervisor_id) as rnked natural join Teacher 
# where rnk <=2;

def add_reviewers(reviewers_list, phase):
    global cnx 
    cnx_cursor = cnx.cursor()
    # print(reviewers_list)
    
    for i in reviewers_list:
        # print(i)
        project = i[0]
        reviewers = i[1]
        print(project, reviewers)
        project_id = project[0]
        reviewer_ids = [i[0] for i in reviewers]
        
        for i in reviewer_ids:
            try:
                cnx_cursor.execute("INSERT INTO Reviewed_by (project_id, phase, reviewer_id) VALUES (%(pid)s, %(phase)s, %(rid)s)", {'pid': project_id, 'phase': phase, 'rid': i})
            except Exception as err:
                pass
        # pass
        

def log_out():
    global cnx
    cnx.close()
    cnx=None