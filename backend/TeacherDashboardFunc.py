import mysql.connector
from mysql.connector import errorcode 
from backend import config


# returning hasTeam and hasResume values in the get_student_details function itself

def get_teacher_details(teacher_id):
    
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
    
    result = cnx_cursor.execute("""SELECT Fname, Lname, email
                                   FROM Teacher where teacher_id = %(teacher_id)s""", {'teacher_id' : teacher_id})
    
    (first_name, last_name, email) = cnx_cursor.fetchone()

    cnx.close()
    
    return (first_name, last_name, email)


# x = get_student_details("PES1UG04MVE50")
# for i in x:
#     print(i)