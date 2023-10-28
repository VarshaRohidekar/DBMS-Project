insert_student = """INSERT INTO Student (srn, pswd, Fname, Lname, semester, cgpa, outgoing_year, email) 
                    VALUES (%(srn)s, %(pswd)s, %(Fname)s, %(Lname)s, %(semester)s, %(cgpa)s, %(outgoing_year)s, %(email)s)"""

insert_teacher = """INSERT INTO Teacher (teacher_id, Fname, Lname, email, floor, cabin_no, pswd)
                    VALUES (%(teacher_id)s, %(Fname)s, %(Lname)s, %(email)s, %(floor)s, %(cabin_no)s, %(pswd)s)"""

insert_admin = """INSERT INTO Admin (admin_id, pswd, email)
                 VALUES (%(admin_id)s, %(pswd)s, %(email)s)"""
                 
insert_supervisor = """INSERT INTO Supervisor (supervisor_id, team_limit, active_projects)
                       VALUES (%(supervisor_id)s, %(team_limit)s, %(active_projects)s)"""
                       
insert_supervisor_years = """INSERT INTO Supervisor_years (supervisor_id, batch)
                             VALUES (%(supervisor_id)s, %(batch)s)"""

insert_supervisor_domain = """INSERT INTO Supervisor_Domains (supervisor_id, domain)
                              VALUES (%(supervisor_id)s, %(domain)s)"""