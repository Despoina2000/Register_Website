from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
#from passlib.hash import sha256_crypt
import hashlib
import mysql.connector as mariadb
import os
import re
import operator
app = Flask(__name__)
mariadb_connect = mariadb.connect(user='myserver', password='3180146', database='GDPR')

@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mariadb_connect.cursor(buffered=True)
        cursor.execute('SELECT * FROM users WHERE username = %s;', (username))
        # Fetch one record and return result
        account = cursor.fetchone()
                # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            verify=account['password']
            salt= account['salt']
            cursor.execute('SELECT fails FROM logging WHERE uid=%i;',(account['uid']))
            fails=cursor.fetchone()
            if verify==hashlib.pbkdf2_hmac('sha256', password,salt , 10000)and(fails<=3):
              session['loggedin'] = True
              session['uid'] = account['uid']
              session['username'] = account['username']
              result='successfully!'
            else:
                cursor.execute('UPDATE logging SET fails = fails+1, last_try=CURDATE() WHERE uid = %i;'(account['uid']))
                mariadb_connect.commit()
                result='failed'  
            # check for passwords' last update
            
            cursor.execute('SELECT MONTH(last_update) FROM logging;')
            lastupdate=cursor.fetchone()
            cursor.execute('SELECT MONTH(CURDATE());')
            month=cursor.fetchone()
            warning=''
            if month>lastupdate:
              warning='!WARNING! You should change your password for better security!'

            
            return 'Logged in '+ result +warning
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'The user does not exist!'
            
    return render_template('index.html', msg='')
#@app.route('/')
#def home():
#  if not session.get('logged_in'):
#    return render_template('login.html')
#  else:
#    return render_template('index.html')

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect('/login')

@app.route('/logout')
def logout():
  session['logged_in'] = False
  return home()

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        salt = os.urandom(32)
        while not unique_salt(salt):
            salt = os.urandom(32)
        cursor = mariadb_connect.cursor(buffered=True)
        username = request.form['username']
        password =hashlib.pbkdf2_hmac('sha256', request.form['password'],salt , 10000) 
        # Check if account exists using MySQL
        
        data=cursor.execute('SELECT * FROM users WHERE username = %s', (username))
        account = cursor.fetchone()[1]
        # If account exists show error and validation checks
        if account==username:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password :
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO users VALUES (%s, %s,%s);', (username, password,salt))
            mariadb_connect.commit()
            cursor.execute('SELECT uid FROM users WHERE username=%s;', (username))
            uid=cursor.fetchone()
            cursor.execute('INSERT INTO logging VALUES (%i, %i,NULL,CURDATE());', (uid, 0))
            mariadb_connect.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

if __name__ == "__main__":
  app.secret_key = os.urandom(12)
  app.run(debug=False,host='0.0.0.0', port=5000)

def unique_salt(_salt):
    cursor = mariadb_connect.cursor(buffered=True)
    cursor.execute('SELECT salt FROM users;')
    salts=cursor.fetchone()
    for salt in salts:
        if _salt==salt:
            return False
    return True
