select_students = """SELECT srn, Fname, Lname, semester, cgpa, email, outgoing_year, team_id
                     FROM Student
                     WHERE semester = %(sem)s"""
                     
select_teachers = """SELECT teacher_id, Fname, Lname, email, floor, cabin_no
                    FROM Teacher"""
                    
select_pending_requests = """SELECT *
                             FROM Request
                             WHERE supervisor_id = %(id)s"""