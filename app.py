from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
app = Flask(__name__, static_url_path='/static')

# A simple dictionary to store user data (replace with a proper database)

users = {
    'user1': {'password': 'password1', 'name': 'John Doe'},
    'user2': {'password': 'password2', 'name': 'Jane Smith'},
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
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Dropdown box -> teacher,student,admin -> pass it to db and get true/false
        if username in users and users[username]['password'] == password:
            if username in logged_in_users:
                return redirect(url_for('profile', username=username))
            logged_in_users.add(username)
            return redirect(url_for('profile', username=username))
        else:
            return "Login failed. Please check your credentials."
    return render_template('login.html')

# Check whether the person logging in is a teacher/student or admin
@app.route('/studentprofile/<username>', methods=['GET', 'POST'])
def profile(username):
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

''' TEACHER PROFILE PAGE '''
# If a teacher is a supervisor -> modify teacher page to supervisor
# TEACHER PAGE -> Teacher ID, Name, Floor, Cabin, Current Project List

# Regardless of the year for which a teacher is a supervisor -> redirect to supervisor page
# SUPERVISOR PAGE -> Supervisor ID,Name,Drop down box for checking the batch of team
# If the supervisor exists for the current batch (3rd year) -> accept requests
# If the supervisor exists for the final year batch (4th year) -> do not accept requests.
# View Active Teams(button) -> Each team will have "view project" button,List of active project teams with team name,project name

'''ADMIN PAGE'''



@app.route('/logout')
def logout():
    # Log the user out by removing them from the logged_in_users set
    username = request.path.split('/')[-1]
    if username in logged_in_users:
        logged_in_users.remove(username)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True,port='3000',host="127.0.0.1")

