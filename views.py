from init import app, mysql
from flask import jsonify, request, render_template, flash, redirect, logging, url_for
import hashlib,time
from input import *
import pandas as pd
from authentication import authenticate_user
# test_data = []

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return  render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == "POST":
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        if username and password:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO users(username, passcode) VALUES (%s, %s)", (username, password))
            mysql.connection.commit()
            cursor.close()
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # global test_data
    if request.method == "POST":
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        captcha = request.form['captcha']
        if username and password and captcha == '.tie5Roanl':
            cursor = mysql.connection.cursor()
            result = cursor.execute("SELECT * FROM users WHERE username = %s", [username])
            if result > 0:
                data = cursor.fetchone()
                if password == data[2]:
                    time.sleep(1)
                    data = pd.read_csv('test_data.csv',header=None)
                    # print('mihir',data.head(5))                    
                    predicted_user = authenticate_user(data.head(1))
                    if predicted_user[0].lower() == username.lower():
                        flash('You are now logged in', 'success')
                    else:
                        flash('Hacker', 'danger')    
                else:
                    flash('Your username and password does not match', 'danger')
    return render_template('login.html')

@app.route('/start_background_script', methods=['GET','POST'])
def background_script():
    start_listener()
    return ""

@app.route('/stop_background_script', methods=['GET','POST'])
def stop_background_script():
    stop_listener()
    return ""