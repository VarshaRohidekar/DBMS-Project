import mysql.connector
from mysql.connector import errorcode 
from backend import config    
    
def verify_login(role, id, password):

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
    
    if role == 's':
        result = cnx_cursor.execute(""" SELECT srn, pswd from Student where srn = %(srn)s""", {'srn' : id})
    elif role == 't':
        result = cnx_cursor.execute(""" SELECT teacher_id, pswd from Teacher where teacher_id = %(teacher_id)s""", {'teacher_id' : id})
    else:
        result = cnx_cursor.execute("""SELECT admin_id, pswd FROM Admin where admin_id = %(admin_id)s""", {'admin_id': id})
    content = cnx_cursor.fetchone()
    cnx.close()
    
    if content is None:
        return "ID not found"
    
    else:
        (s,p) = content
        if p == password:
            return True 
        else:
            return False


# x = verify_login('t', "T1234ASDFGHJ3", "1234ASDFGHKL")
# print(x)