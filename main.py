from flask import Flask,render_template,request, redirect, url_for
import mysql.connector
import pandas as pd
app = Flask(__name__, static_url_path='/static')

users = {
    'user1': 'password1',
    'user2': 'password2',
}

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="newyork1176",
    database="art_gallery"
)

# @app.route('/')
# def hello_world():
#     # cursor = db.cursor()
#     # cursor.execute("SELECT * FROM art")
#     # data = cursor.fetchall()
#     # data=pd.DataFrame(data)
#     # cursor.close()
#     # return render_template('index.html', data=data)
#     # return 'Hello, World!'
#     cursor = db.cursor()
#     cursor.execute("SELECT * FROM art")
#     data = cursor.fetchall()
#     # Get the column names from the database cursor
#     column_names = [desc[0] for desc in cursor.description]

#     return render_template('index.html', data=data, column_names=column_names)

# @app.route('/other_page')
# def other_page():
#     cursor = db.cursor()
#     cursor.execute("SELECT * FROM art")
#     data = cursor.fetchall()
#     column_names = [desc[0] for desc in cursor.description]
#     return render_template('other_page.html',data=data,column_names=column_names)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in users and users[username] == password:
        return "Login Successful!"
    else:
        return "Login Failed. Please check your username and password."

if __name__ == '__main__':
    app.run(debug=True,port='3001',host="127.0.0.1")

