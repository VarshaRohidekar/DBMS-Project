import mysql.connector
from mysql.connector import errorcode 
from backend import config


# returning hasTeam and hasResume values in the get_student_details function itself

def get_student_details(srn):
    
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
    
    result = cnx_cursor.execute("""SELECT Fname, Lname, email, outgoing_year, cgpa, semester, team_id, resume_doc 
                                   FROM Student where srn = %(srn)s""", {'srn' : srn})
    (first_name, last_name, email, outgoing_year, cgpa, semester, team_id, resume_doc) = cnx_cursor.fetchone()

    cnx.close()
    
    teamEligibility = True
    hasTeam = False
    hasResume = False
    if team_id is not None:
        hasTeam = True
        
    if resume_doc is not None:
        hasResume = True
    
    if int(semester) < 5:
        teamEligibility = False
        
    
    return (first_name, last_name, email, outgoing_year, cgpa, semester, teamEligibility, hasTeam, hasResume)


# x = get_student_details("PES1UG04MVE50")
# for i in x:
#     print(i)