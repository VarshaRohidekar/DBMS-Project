from flask import Flask, render_template, request, redirect, url_for,session,jsonify
import mysql.connector
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'dbms'
from backend import LoginPageFunc, StudentDashboardFunc,TeacherDashboardFunc, AdminFunc, TeamFormFunc, TeamPageFunc, ProjectPageFunc, RequestFormFunc
import pandas as pd
from backend import config
import os
# A simple dictionary to store user data (replace with a proper database)

# users = {
#     'user1': {'password': 'password1', 'name': 'John Doe','auth':'t'},
#     'user2': {'password': 'password2', 'name': 'Jane Smith','auth':'s'},
#     'user3': {'password': 'password3', 'name': 'ADMIN CHECKING','auth':'a'}
# }

logged_in_users = []

db = mysql.connector.connect(
    **config.config
)

@app.route('/', methods=['POST', 'GET'])
def home():
    
    return render_template('home.html')

# logged_in_users = set()

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        role = request.form.get('role')      # need to get this from the form
        username = request.form.get('username')     # srn or teacher_id
        password = request.form.get('password')
        # print(role)
        result = LoginPageFunc.verify_login(role, username, password)
        if type(result) == bool:
            if result:
                if role=='t':
                    return redirect(url_for('teacherprofile', username=username))
                elif role=='s':
                    return redirect(url_for('studentprofile', username=username))
                else:
                    return redirect(url_for('adminprofile', username=username))
                # redirect to the respective role's page
            else:
                print("password invalid")
                return render_template('login.html')
                #pop-up on login page saying that password is wrong
        
        else:
            print(result)
            return render_template('login.html')
            #pop-up on login page printing the 'result' string

        # if username in users and users[username]['password'] == password:
        #     # Successful login
        #     session['username'] = username  # Store the username in the session
        #     auth_level = users[username]['auth']
        #     if role == 1:
        #         return redirect(url_for('teacherprofile', username=username))
        #     elif auth_level==2:
        #         # The user is a student
        #         return redirect(url_for('studentprofile', username=username))
        #     elif auth_level==3:
        #         return redirect(url_for('adminprofile', username=username))
        # else:
        #     # Invalid username or password
        #     return "Invalid credentials. Please try again."

    return render_template('login.html')




# Check whether the person logging in is a teacher/student or admin
@app.route('/studentprofile/<username>', methods=['GET', 'POST'])
def studentprofile(username):
    first_name, last_name, email, outgoing_year, cgpa, semester, teamEligibility, hasTeam, hasResume, team_id = StudentDashboardFunc.get_student_details(username)
    


    resume_link = url_for("showresume", username=username)
    # if teamEligibility:
    #     # needs to redirect to 2 different pages depending upon state of team formation
    #     if hasTeam:
    #         return "go to team page"        # a button
    #     else:
    #         return "create team"            # a button
    
    # else:
    #     return None
    print(url_for("showresume", username=username))
    if request.method == 'POST':
        # First name, last name, SRN, CGPA ,Semester and email, upload resume, current YEAR/Batch.
        # If student not in team -> button to create a team (only for 3rd years)
        # If student has a team -> view team button -> on clicking view team redirect to team page.
        # If student has a resume -> view resume, edit resume button
        # If student does not have a resume -> upload resume
        # Batch -> Outgoing Year 
        # user['email'] = request.form.get('email')
        # user['bio'] = request.form.get('bio')
        for field, data in request.files.items():
            print("file recieved")
            print(field)
            print(data.stream.read())
            StudentDashboardFunc.insert_file(username, data.stream)
        # resume = form['resume']
        # if resume:
        #     print(resume)
        # else:
        #     print("no resume")
        
        # return "Profile updated successfully."
    return render_template('studentprofile.html', username=username, first_name=first_name, last_name=last_name, email_id=email,outgoing_year=outgoing_year,cgpa=cgpa,semester=semester, hasResume=hasResume, teamEligibility = teamEligibility, hasTeam=hasTeam, resume_page = resume_link, team_id=team_id)

@app.route('/studentprofile/<username>/resume', methods = ['GET', 'POST'])
def showresume(username):
    
    print("reached resume")
    return render_template('resume.html', username=username)


@app.route('/teamformpage/<srn>', methods=['GET','POST'])
def teamformpage(srn):
    # print(url_for('teamformpage', srn=srn))
    if request.method=="POST":
        srn1 = request.form.get('srn1')
        srn2 = request.form.get('srn2')
        srn3 = request.form.get('srn3')
        srn4 = request.form.get('srn4')
        TeamName = request.form.get('TeamName')

        print(srn1)
        print(srn2)
        print(srn3)
        print(srn4)
        value = TeamFormFunc.validate_team(srn1,srn2,srn3,srn4)
        if value==True:
            print("Team valid")
            (i,teamid)=TeamFormFunc.add_team(srn1,srn2,srn3,srn4,TeamName)
            if i==True:
                print("Team formed")
                return redirect(url_for('teampage', team_id=teamid, srn=srn))
        if value==False:
            print("Team not valid")
            # return render
    return render_template('teamformpage.html', to_check=url_for('teamformpage', srn=srn))

@app.route('/teampage/<team_id>/<srn>', methods=["GET", "POST"])
def teampage(team_id, srn):
    print(srn)
    (team_id, team_name, rows, cols, hasProject) = TeamPageFunc.team_info(team_id)
    print(hasProject)
    
    return render_template('teampage.html', team_id=team_id, team_name=team_name, srn=srn, rows=rows, cols=cols, hasProject=hasProject)


@app.route('/teampage/<team_id>/<srn>/requestsform', methods=["GET", "POST"])
def requestsform(team_id,srn):
    teachers = RequestFormFunc.get_available_supervisors()
    return render_template('requestsform.html', team_id=team_id,srn=srn, teachers=teachers)

@app.route('/teampage/<team_id>/<srn>/requestsstatus', methods=["GET", "POST"])
def requestsstatus(team_id, srn):
    return render_template('requestsstatus.html', team_id=team_id, srn=srn)


@app.route('/teampage/<team_id>/<srn>/reviewpage', methods=["GET", "POST"])
def reviewpage(team_id, srn):
    return render_template('reviewpage.html',team_id=team_id,srn=srn)

@app.route('/teampage/<team_id>/<srn>/project', methods=["GET", "POST"])
def project(team_id, srn):
    project_id,team_id,problem_statement, domain, start_d, end_d, cur_phase = ProjectPageFunc.display_projectdetails(team_id)
    return render_template('project.html', project_id=project_id,team_id=team_id, srn=srn,problem_statement=problem_statement,domain=domain,start_d=start_d,end_d=end_d,cur_phase=cur_phase)
@app.route('/teacherprofile/<username>', methods=['GET', 'POST'])
def teacherprofile(username):
    # user = users.get(username)
    first_name,last_name,email = TeacherDashboardFunc.get_teacher_details(username)
    print(first_name,last_name,email)
    return render_template('teacherprofile.html', username=username, first_name=first_name,last_name=last_name,email_id=email)

''' TEACHER PROFILE PAGE '''
# If a teacher is a supervisor -> modify teacher page to supervisor
# TEACHER PAGE -> Teacher ID, Name, GET REVIEWS(SEE LATER)

# Regardless of the year for which a teacher is a supervisor -> redirect to supervisor page
# SUPERVISOR PAGE -> Supervisor ID,Name,Drop down box for checking the batch of team, GET REVIEWS(LATER)
# If the supervisor exists for the current batch (3rd year) -> on view requests -> viewing pending requests(allowed to accept/reject) (x or a tick)
# If the supervisor exists for the final year batch (4th year) -> do not accept requests.
# View Active Teams(button) -> Each team will have "view project" button,List of active project teams with team name,project name,BATCH

'''ADMIN PAGE'''
# @app.route('/adminprofile', methods=['GET', 'POST'])
# def adminprofile():
#     # user = users.get(username)
#     # if not user:
#     #     return "User not found."
#     # if request.method == 'POST':
#     #     # Add teacher-specific logic for updating the profile
#     #     user['email'] = request.form.get('email')
#     #     user['bio'] = request.form.get('bio')
#     #     return "Teacher profile updated successfully."
#     return render_template('adminprofile.html')

@app.route('/adminprofile/<username>', methods=['GET', 'POST'])
def adminprofile(username):
    
    logged_in_users.append(username)
    AdminFunc.log_in()
    email = AdminFunc.get_admin_details(username)
    adminteacherlink = url_for('adminteacher', username=username)
    adminstudentlink = url_for('adminstudent', username=username)
    adminquerylink = url_for('adminquery', username=username)
    return render_template('adminprofile.html', email=email, admin_id=username, adminteacherlink=adminteacherlink, adminstudentlink=adminstudentlink, adminquerylink=adminquerylink)

@app.route('/adminprofile/<username>/adminstudent', methods=['GET', 'POST'])
def adminstudent(username):
    AdminFunc.log_in()
    (data, cols) = AdminFunc.get_student_details()
    return render_template('adminstudent.html', username=username, data=data, cols=cols)

@app.route('/adminprofile/<username>/adminteacher', methods=['GET', 'POST'])
def adminteacher(username):
    AdminFunc.log_in()
    (data, cols) = AdminFunc.get_teacher_details()
    return render_template('adminteacher.html',username=username, data=data, cols=cols)

@app.route('/adminprofile/<username>/adminquery', methods=["POST", 'GET'])
def adminquery(username):
    AdminFunc.log_in()
    data=None
    cols=None
    err=None
    if request.method=="POST":
        query = request.form.get('query')
        # cursor = db.cursor()

        # cursor.execute(query)
        # data = cursor.fetchall()
        # # Get the column names from the database cursor
        # cols = [desc[0] for desc in cursor.description]
        result = AdminFunc.get_query(query)
        if type(result)!= str:
            (data, cols) = result
        else:
            err=result

    return render_template('adminquery.html', username=username, data=data, cols=cols, err=err)

@app.route('/logout')
def logout():
    # Log the user out by removing them from the logged_in_users set
    username = request.path.split('/')[-1]
    if username in logged_in_users:
        AdminFunc.log_out()
        logged_in_users.remove(username)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True,port='8628',host="127.0.0.1")

