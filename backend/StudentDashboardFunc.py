import mysql.connector
from mysql.connector import errorcode 
from backend import config
import base64

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
        
    
    return (first_name, last_name, email, outgoing_year, cgpa, semester, teamEligibility, hasTeam, hasResume, team_id)

def insert_file(username, stream_obj):
    
    # convert file to binary
    file = stream_obj.read()
    try:
        file = base64.b64encode(file)
    except:
        print("couldn't convert file")
    
    
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
    
    result = cnx_cursor.execute("""UPDATE Student SET resume_doc = %(file)s where srn = %(srn)s """, {'file' : file, 'srn' : username})    
    
    cnx.close()
    
    return

# def get_resume(username):

#     try:
#         cnx = mysql.connector.connect(**config.config)

#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Something is wrong with your user name or password")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("Database does not exist")
#         else:
#             print(err)
#     else:
#         print("connected to", cnx._database)        #cnx._database -- value of current database
        
#     cnx_cursor = cnx.cursor()
    
#     cnx_cursor.execute("""SELECT resume_doc FROM Student where srn=%(srn)s""", {'srn': username})
    
#     data = cnx_cursor.fetchall()
#     resume_doc = data[0][0]
    
#     bin_resume_doc = base64.b64decode(resume_doc)
#     print(bin_resume_doc.decode())
    

#     return
# x = get_student_details("PES1UG04MVE50")
# for i in x:
#     print(i)

# get_resume('PES1UG04MVE50')