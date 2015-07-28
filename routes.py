from flask import Flask, render_template, session, request, redirect, url_for
from datetime import timedelta
import json
   
app = Flask(__name__)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1) 


"""
    Routes for main menu
"""
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tutorials')
def tutorials():
    return render_template('tutorials/index.html')
  
@app.route('/about')
def about():
    return render_template('about.html')
  
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/validate_login', methods=['GET', 'POST'])
def validate_login():
    session['username'] = request.form['username']
    print session['username']
    
    session['logged_in'] = True
    
    errorDict = {'message':"OK", 'iserror': False}
    return json.dumps(errorDict)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def registration():
    return render_template('registration.html')

@app.route('/validate_registration', methods=['GET', 'POST'])
def validate_registration():
    response = {'message': "OK", 'iserror': False}
    return json.dumps(response)
  
"""
    Routes for tutorials
"""

@app.route('/tutorials/python')
def python():
    return render_template('tutorials/python.html')

@app.route('/tutorials/java')
def java():
    return render_template('/tutorials/java.html')

@app.route('/tutorials/c')
def c():
    return render_template('/tutorials/c.html')

if __name__ == '__main__':
    app.secret_key = 'This is my supersecret key that nobody knows about, except my butcher!!!'
    app.run(debug=True)