from flask import Flask, render_template, request, redirect, url_for,session,jsonify
import mysql.connector
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'dbms'
from backend import LoginPageFunc, StudentDashboardFunc,TeacherDashboardFunc, AdminFunc, TeamFormFunc, TeamPageFunc, ProjectPageFunc, RequestFormFunc, SupervisorFunc,ReviewPageFunc
import pandas as pd
import json
from backend import config
import os

logged_in_users = []

# db = mysql.connector.connect(
#     **config.config
# )

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

    return render_template('login.html')


# Check whether the person logging in is a teacher/student or admin
@app.route('/studentprofile/<username>', methods=['GET', 'POST'])
def studentprofile(username):
    first_name, last_name, email, outgoing_year, cgpa, semester, teamEligibility, hasTeam, hasResume, team_id = StudentDashboardFunc.get_student_details(username)
    resume_link = url_for("showresume", username=username)
    print(url_for("showresume", username=username))
    if request.method == 'POST':

        for field, data in request.files.items():
            print("file recieved")
            print(field)
            # print(data.stream.read())
            StudentDashboardFunc.insert_file(username, data.stream.read())
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
    isStudent=False
    if srn[0]=='P':
        isStudent=True
    (team_id, team_name, rows, cols, hasProject, avg) = TeamPageFunc.team_info(team_id)
    avg=format(avg, ".2f")
    print(hasProject)
    
    return render_template('teampage.html', team_id=team_id, team_name=team_name, srn=srn, rows=rows, cols=cols, hasProject=hasProject, isStudent=isStudent, avg=avg)


@app.route('/teampage/<team_id>/<srn>/requestsform', methods=["GET", "POST"])
def requestsform(team_id,srn):
    domains = RequestFormFunc.get_domains()
    print(domains)
    teachers = RequestFormFunc.get_available_supervisors()
    print(teachers)
    sendingrequestslink = url_for('sendingrequests', team_id=team_id, srn=srn)
    return render_template('requestsform.html', team_id=team_id,srn=srn, teachers=teachers, domains=domains, sendingrequestslink=sendingrequestslink)

@app.route('/teampage/<team_id>/<srn>/sendingrequests', methods=["POST"])
def sendingrequests(team_id, srn):
    
    print("reached")
    if request.method == 'POST':
        content=request.get_data()
        content=content.decode('utf8')
        data = json.loads(content)
        print(data)
        
        RequestFormFunc.insert_request(data['team_id'], data['teachers'], data['domain'], data['idea'])
        # s = json.dumps(data, indent=4, sort_keys=True)
        # print(s)
        # print()
    return url_for('teampage', team_id=team_id, srn=srn)

@app.route('/teampage/<team_id>/<srn>/reviewpage', methods=["GET", "POST"])
def reviewpage(team_id, srn):
    result = ReviewPageFunc.get_reviews(team_id)
    print(result)

    isStudent = False 
    if srn[0]=='P':
        isStudent=True

    return render_template('reviewpage.html',team_id=team_id,srn=srn,result=result,isStudent=isStudent)

@app.route('/teampage/<team_id>/<srn>/requestsstatus', methods=['GET', 'POST'])
def requestsstatus(team_id,srn):
    result = TeamPageFunc.get_requests(team_id)
    redirectlink = url_for('creating_project_page', team_id=team_id, srn=srn)

    print("to creating project: "+ redirectlink)
    return render_template('requestsstatus.html',team_id=team_id,srn=srn,result=result, redirectlink=redirectlink)

@app.route('/creating_project_page/<team_id>/<srn>', methods=["POST", "GET"])
def creating_project_page(team_id, srn):
    print("reached creating project page")
    if request.method == 'POST':
        content=request.get_data()
        content=content.decode('utf8')
        data = json.loads(content)
        print('LASKDFKJLSKJLKJLJ: ', type(data['id']))
        projectid = ProjectPageFunc.create_project(int(data['id']))
        # RequestFormFunc.insert_request(data['team_id'], data['teachers'], data['domain'], data['idea'])
        # s = json.dumps(data, indent=4, sort_keys=True)
        # print(s)
        # print()
        return url_for('project', team_id=team_id, srn=srn)
    # return url_for('requestsstatus', team_id=team_id, srn=srn)


@app.route('/teampage/<team_id>/<srn>/project', methods=["GET", "POST"])
def project(team_id, srn):          # srn can be student id or supervisor id
    project_id,team_id,supervisor_id, problem_statement, domain, start_d, end_d, cur_phase = ProjectPageFunc.display_projectdetails(team_id)
    isStudent=False
    if srn[0]=='P':
        isStudent=True
    Fname, Lname, email = TeacherDashboardFunc.get_teacher_details(supervisor_id)
    return render_template('project.html', project_id=project_id,team_id=team_id, srn=srn,problem_statement=problem_statement,domain=domain,start_d=start_d,end_d=end_d,cur_phase=cur_phase, isStudent=isStudent,supervisor_id=supervisor_id,Fname=Fname,Lname=Lname)


@app.route('/teacherprofile/<username>', methods=['GET', 'POST'])
def teacherprofile(username):
    # user = users.get(username)
    print(username)
    isSupervisor = TeacherDashboardFunc.is_Supervisor(username)
    requestslink = url_for('viewrequests', username=username)
    first_name,last_name,email = TeacherDashboardFunc.get_teacher_details(username)
    print(first_name,last_name,email)
    team_limit = None 
    active_projects = None
    accepted_requests = None
    activeSupervisor = None 
    if isSupervisor:
        stuff = SupervisorFunc.get_supervisor_info(username)
        activeSupervisor = stuff[0]
        team_limit = stuff[1]
        active_projects = stuff[2]
        accepted_requests = stuff[3]
        print(stuff)
        
    return render_template('teacherprofile.html', username=username, first_name=first_name,last_name=last_name,
                           email_id=email, isSupervisor=isSupervisor, requestslink=requestslink, team_limit=team_limit, 
                           active_projects=active_projects, accepted_requests=accepted_requests, activeSupervisor=activeSupervisor)

@app.route('/teacherprofile/<username>/viewrequests', methods=['GET', 'POST'])
def viewrequests(username):
    content = SupervisorFunc.get_requests(username)
    requests = []
    redirectlink = url_for('process_request', username=username)

    for request in content:
        # Extract relevant information from the request
        request_id = request[0]
        team_id = request[1]
        interested_domain = request[2]
        idea = request[3]
        req_status = request[4]

        team_info = TeamPageFunc.team_info(team_id)
        print(team_info)
        requests.append({
            'request_id': request_id,
            'team_id': team_id,
            'interested_domain': interested_domain,
            'idea': idea,
            'req_status': req_status,
            'team_info': team_info, 
        })
        # need to handle avg value added in the end

    return render_template('viewrequests.html', username=username, requests=requests, redirectlink=redirectlink)

@app.route('/teacherprofile/<username>/viewactiveprojects', methods=['GET', 'POST'])
def viewactiveprojects(username):

    if request.method=='POST':
        content=request.get_data()
        content=content.decode('utf8')
        data = json.loads(content)
        if 'project_id' in data.keys():
            # need to end project
            print("project ended for project id: ", data['project_id'])
            SupervisorFunc.end_project(data['project_id'])
            return url_for('viewactiveprojects', username=username)
        return url_for('project', srn=username, team_id=data['team_id'])

    result = SupervisorFunc.get_projects(username)
    print("This is ",result)
    requests = []
    for req in result:
            # Extract relevant information from the request
            project_id = req[0]
            team_id = req[1]
            supervisor_name = req[2]
            start_date = req[3]
            end_date = req[4]
            cur_phase = req[5]
            domain=req[6]
            idea = req[7]

            # need to handle avg in team_info
            team_info = TeamPageFunc.team_info(team_id)
            print(team_info)
            requests.append({
                'project_id': project_id,
                'team_id': team_id,
                'supervisor_name' : supervisor_name,
                'start_date':start_date,
                'end_date': end_date,
                'cur_phase':cur_phase,
                'domain':domain,
                'idea':idea,
                'team_info':team_info
                
            })


    
    return render_template('viewactiveprojects.html',username=username,requests=requests)

@app.route('/teacherprofile/<username>/viewpastprojects', methods=['GET', 'POST'])
def viewpastprojects(username):
    result = SupervisorFunc.get_completed_projects(username)
    print(result)
    requests = []
    for req in result:
        # Extract relevant information from the request
        project_id = req[0]
        team_id = req[1]
        # supervisor_id = req[2]
        start_date = req[3]
        end_date = req[4]
        # cur_phase = req[5]
        domain = req[6]
        idea = req[7]

        team_info = TeamPageFunc.team_info(team_id)
        requests.append({
            'project_id': project_id,
            'team_id': team_id,
            # 'supervisor_id' : supervisor_id,
            'start_date': start_date,
            'end_date': end_date,
            # 'cur_phase': cur_phase,
            'domain': domain,
            'idea': idea,
            'team_info': team_info
        })

    return render_template('viewpastprojects.html', username=username, requests=requests)


@app.route('/teacherprofile/<username>/makereviews', methods=['GET', 'POST'])
def makereviews(username):
    result = ReviewPageFunc.get_reviewers(username)
    requests = []
    for req in result:
        # Extract relevant information from the request
        project_id = req[0]
        phase = req[1]
        supervisor_id = req[2]
        feedback = req[3]
        grade = req[4]

        requests.append({
            'project_id': project_id,
            'phase': phase,
            'supervisor_id': supervisor_id,
            'feedback' : feedback,
            'grade' : grade
        })

    if request.method == 'POST':
        new_feedback = request.form.get('new_feedback')
        reviewer_id = request.form.get('reviewer_id')
        project_id = request.form.get('project_id')
        phase = request.form.get('phase')

        print(f"Received data: new_feedback={new_feedback}, reviewer_id={reviewer_id}, project_id={project_id}, phase={phase}")

        # Debug statements to check if the route is being reached
        print("Reached POST route")

        # Add validation for new_feedback if needed
        success = ReviewPageFunc.addreviews(project_id, phase, reviewer_id, new_feedback)

        # Debug statement to check if the function is executed
        if success:
            print("Review added successfully")
        else:
            print("Failed to add review")

        return redirect(url_for('makereviews', username=username))

        return redirect(url_for('makereviews', username=username))
    return render_template('makereviews.html',username=username,requests=requests)



@app.route('/process_request/<username>', methods=["POST", "GET"])
def process_request(username):
    print("reached process")
    # get information from the form
    if request.method == 'POST':
        content=request.get_data()
        content=content.decode('utf8')
        data = json.loads(content)
        print(data)
        
        SupervisorFunc.modify_request(data['action'], data['id'])

    # call needed functions
    
    return url_for("viewrequests", username=username)

@app.route('/adminprofile/<username>', methods=['GET', 'POST'])
def adminprofile(username):
    
    logged_in_users.append(username)
    AdminFunc.log_in()
    email = AdminFunc.get_admin_details(username)
    adminteacherlink = url_for('adminteacher', username=username)
    adminstudentlink = url_for('adminstudent', username=username)
    adminquerylink = url_for('adminquery', username=username)
    adminreviewerslink=url_for('assignreviewers', username=username)
    return render_template('adminprofile.html', email=email, admin_id=username, adminteacherlink=adminteacherlink, adminstudentlink=adminstudentlink,
                           adminquerylink=adminquerylink, adminreviewerslink=adminreviewerslink)

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

@app.route('/adminprofile/<username>/assignreviewers', methods=["POST", "GET"])
def assignreviewers(username):
    AdminFunc.log_in()
    result=False
    phase=None
    batches = AdminFunc.get_batches()
    if request.method=="POST" and 'batch' in request.form:
        # print('batch' in request.form)
        batch=request.form.get('batch')
        phase, result=AdminFunc.assign_reviewers(batch)
    else:
        content = request.get_data()
        content = content.decode('utf8')
        content = json.loads(content)
        # content = str(content)
        # content.replace("&#39;", '"')
        # print("printing content: ",content)
        # print("type: ", type(content))
        reviewer_list = content['result']
        p = content['phase']
        # print(p, reviewer_list)
        AdminFunc.add_reviewers(reviewer_list, p)
        pass
    
    print(result)
    return render_template('adminassignreviewers.html', username=username, result=result, batches=batches, phase=phase)

@app.route('/logout')
def logout():
    # Log the user out by removing them from the logged_in_users set
    username = request.path.split('/')[-1]
    if username in logged_in_users:
        AdminFunc.log_out()
        logged_in_users.remove(username)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True,port="8080",host="127.0.0.1")