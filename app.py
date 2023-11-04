from flask import Flask, render_template, request, redirect, url_for,session,jsonify
import mysql.connector
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'dbms'
from backend import LoginPageFunc, StudentDashboardFunc,TeacherDashboardFunc, AdminFunc, TeamFormFunc
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
    first_name, last_name, email, outgoing_year, cgpa, semester, teamEligibility, hasTeam, hasResume = StudentDashboardFunc.get_student_details(username)
    


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
    return render_template('studentprofile.html', username=username, first_name=first_name, last_name=last_name, email_id=email,outgoing_year=outgoing_year,cgpa=cgpa,semester=semester, hasResume=hasResume, teamEligibility = teamEligibility, hasTeam=hasTeam, resume_page = resume_link)

@app.route('/studentprofile/<username>/resume', methods = ['GET', 'POST'])
def showresume(username):
    
    print("reached resume")
    return render_template('resume.html', username=username)


@app.route('/teamformpage', methods=['GET','POST'])
def teamformpage():
    if request.method=="POST":
        srn1 = request.form.get('srn1')
        srn2 = request.form.get('srn2')
        srn3 = request.form.get('srn3')
        srn4 = request.form.get('srn4')

        print(srn1)
        print(srn2)
        print(srn3)
        print(srn4)
    
    return render_template('teamformpage.html')

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
    return render_template('adminprofile.html', email=email, admin_id=username)

@app.route('/logout')
def logout():
    # Log the user out by removing them from the logged_in_users set
    username = request.path.split('/')[-1]
    if username in logged_in_users:
        AdminFunc.log_out()
        logged_in_users.remove(username)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True,port='3000',host="127.0.0.1")

