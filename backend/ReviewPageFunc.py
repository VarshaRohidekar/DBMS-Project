import mysql.connector
from mysql.connector import errorcode 
from backend import config    
    
def get_reviews(team_id):

    try:
        cnx = mysql.connector.connect(**config.config)

    # need to find a better way to handle errors

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
    
    cnx_cursor.execute("""SELECT project_id from Project where team_id=%(team_id)s""", {'team_id': team_id})
    project_id = cnx_cursor.fetchone()[0]
    cnx_cursor.execute("""SELECT * from Review where project_id = %(project_id)s""", {'project_id': project_id})
    
    # cnx_cursor.execute("""SELECT * from Review""")

    res = cnx_cursor.fetchall()
    l = [list(i) for i in res]
    for r in l:
        cnx_cursor.execute("""SELECT reviewer_id, Fname, Lname, feedback FROM Review natural join Reviewed_by join Teacher where project_id=%(id)s and phase=%(phase)s and teacher_id=reviewer_id""", {'id': r[0], 'phase': r[1]})
        reviewers = cnx_cursor.fetchall()
        r.append(reviewers)
    cnx.close()
    print(l)
    return l

# x = verify_login('t', "T1234ASDFGHJ3", "1234ASDFGHKL")
# print(x)


def get_reviewers(reviewer_id):
    try:
        cnx = mysql.connector.connect(**config.config)

    # need to find a better way to handle errors

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
    cnx_cursor.execute(''' SELECT * from Reviewed_by natural join Review where reviewer_id = %(reviewer_id)s''',{'reviewer_id': reviewer_id})

    result = cnx_cursor.fetchall()
    cnx.close()
    return result


def addreviews(project_id, phase, reviewer_id, feedback):
    try:
        cnx = mysql.connector.connect(**config.config)
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return False

    try:
        cnx_cursor = cnx.cursor()
        cnx_cursor.execute(
            """UPDATE Reviewed_by
               SET feedback = %(feedback)s
               WHERE project_id = %(project_id)s
                 AND phase = %(phase)s
                 AND reviewer_id = %(reviewer_id)s""",
            {
                'project_id': project_id,
                'phase': phase,
                'reviewer_id': reviewer_id,
                'feedback': feedback
            }
        )

        # Commit the transaction after the UPDATE
        cnx.commit()
    except mysql.connector.Error as err:
        print("Error executing SQL query:", err)
        cnx.rollback()
        return False

    finally:
        cnx.close()

    return True