from flask import Flask, render_template, request, redirect, url_for,session
import mysql.connector
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'dbms'

# A simple dictionary to store user data (replace with a proper database)

users = {
    'user1': {'password': 'password1', 'name': 'John Doe','auth':1},
    'user2': {'password': 'password2', 'name': 'Jane Smith','auth':2},
    'user3': {'password': 'password3', 'name': 'ADMIN CHECKING','auth':3}
}

logged_in_users = set()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="newyork1176",
    database="art_gallery"
)

@app.route('/')
def home():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM art")
    data = cursor.fetchall()
    # Get the column names from the database cursor
    column_names = [desc[0] for desc in cursor.description]
    return render_template('home.html', data=data, column_names=column_names)

logged_in_users = set()

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username]['password'] == password:
            # Successful login
            session['username'] = username  # Store the username in the session
            auth_level = users[username]['auth']
            if auth_level == 1:
                return redirect(url_for('teacherprofile', username=username))
            elif auth_level==2:
                # The user is a student
                return redirect(url_for('studentprofile', username=username))
            elif auth_level==3:
                return redirect(url_for('adminprofile', username=username))
        else:
            # Invalid username or password
            return "Invalid credentials. Please try again."
    return render_template('login.html')


# Check whether the person logging in is a teacher/student or admin
@app.route('/studentprofile/<username>', methods=['GET', 'POST'])
def studentprofile(username):
    user = users.get(username)
    if not user:
        return "User not found."
    if request.method == 'POST':
        # First name, last name, SRN, CGPA ,Semester and email, upload resume, current YEAR/Batch.
        # If student not in team -> button to create a team (only for 3rd years)
        # If student has a team -> view team button -> on clicking view team redirect to team page.
        # If student has a resume -> view resume, edit resume button
        # If student does not have a resume -> upload resume
        # Batch -> Outgoing Year 
        user['email'] = request.form.get('email')
        user['bio'] = request.form.get('bio')
        return "Profile updated successfully."
    return render_template('studentprofile.html', username=username, user=user)


@app.route('/teacherprofile/<username>', methods=['GET', 'POST'])
def teacherprofile(username):
    user = users.get(username)
    if not user:
        return "User not found."
    if request.method == 'POST':
        # Add teacher-specific logic for updating the profile
        user['email'] = request.form.get('email')
        user['bio'] = request.form.get('bio')
        return "Teacher profile updated successfully."
    return render_template('teacherprofile.html', username=username, user=user)

''' TEACHER PROFILE PAGE '''
# If a teacher is a supervisor -> modify teacher page to supervisor
# TEACHER PAGE -> Teacher ID, Name, GET REVIEWS(SEE LATER)

# Regardless of the year for which a teacher is a supervisor -> redirect to supervisor page
# SUPERVISOR PAGE -> Supervisor ID,Name,Drop down box for checking the batch of team, GET REVIEWS(LATER)
# If the supervisor exists for the current batch (3rd year) -> on view requests -> viewing pending requests(allowed to accept/reject) (x or a tick)
# If the supervisor exists for the final year batch (4th year) -> do not accept requests.
# View Active Teams(button) -> Each team will have "view project" button,List of active project teams with team name,project name,BATCH

'''ADMIN PAGE'''
@app.route('/adminprofile/<username>', methods=['GET', 'POST'])
def adminprofile(username):
    user = users.get(username)
    if not user:
        return "User not found."
    if request.method == 'POST':
        # Add teacher-specific logic for updating the profile
        user['email'] = request.form.get('email')
        user['bio'] = request.form.get('bio')
        return "Teacher profile updated successfully."
    return render_template('adminprofile.html', username=username, user=user)


@app.route('/logout')
def logout():
    # Log the user out by removing them from the logged_in_users set
    username = request.path.split('/')[-1]
    if username in logged_in_users:
        logged_in_users.remove(username)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True,port='3000',host="127.0.0.1")

