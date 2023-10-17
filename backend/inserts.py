insert_student = """INSERT INTO Student (srn, pswd, Fname, Lname, semester, cgpa, outgoing_year, email) 
                    VALUES (%(srn)s, %(pswd)s, %(Fname)s, %(Lname)s, %(semester)s, %(cgpa)s, %(outgoing_year)s, %(email)s)"""

insert_teacher = """INSERT INTO Teacher (teacher_id, Fname, Lname, email, floor, cabin_no, pswd)
                    VALUES (%(teacher_id)s, %(Fname)s, %(Lname)s, %(email)s, %(floor)s, %(cabin_no)s, %(pswd)s)"""