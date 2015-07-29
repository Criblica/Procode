from flask import Flask, render_template, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
#from datetime import timedelta, datetime
import json

   
app = Flask(__name__)


"""
    Database
"""
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///development.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False, unique=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(255), nullable=False, unique=False)
    code = db.Column(db.Text, nullable=False, unique=False)
    explanation = db.Column(db.Text, nullable=False, unique=False)
    author =  db.Column(db.String(16), nullable=False, unique=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow, unique=False)
    
    def __init__(self, language, code, explanation, author, date):
        self.language = language
        self.code = code
        self.explanation = explanation
        self.author = author
        self.date = date
    
    def to_json(self):
        return dict(language=self.language, code=self.code, explanation=self.explanation, author=self.author, date=self.date)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False, unique=False)
    author =  db.Column(db.String(16), nullable=False, unique=False) #use user id as primary key instead and do a lookup in users to get username
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow, unique=False)
    
    def __init__(self, message, author, date):
        self.message = message
        self.author = author
        self.date = date
        
    def to_json(self):
        return dict(message=self.message, author=self.author, date=self.date)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=False)
    message = db.Column(db.Text, nullable=False, unique=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow, unique=False)
    
    def __init__(self, title, message, date):
        self.title = title
        self.message = message
        self.date = date
        
    def to_json(self):
        return dict(title=self.title, message=self.message, date=self.date)

db.create_all()


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(hours=12) 


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
    user = User.query.filter_by(username=request.form['username']).first()
    if user:
        if user.password == request.form['password']:
            session['logged_in'] = True
            session['username'] = user.username
            return json.dumps({'message':"OK", 'iserror': False})
        else:
            return json.dumps({'message': "Wrong password. Please try again!", 'iserror': True})
    else:
        return json.dumps({'message': "This username does not exist!", 'iserror': True})
    
    

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
    user = User.query.filter_by(username=request.form['username']).first()
    if user:
        message = "This username is taken. Please try another one!"
        return json.dumps({'message': message, 'iserror': True})
    
    db.session.add(User(request.form['username'], request.form['password']))
    db.session.commit()

    return json.dumps({'message': "OK", 'iserror': False})
  
"""
    Routes for tutorials
"""
@app.route('/tutorials/add')
def add_tutorial():
    return render_template('tutorials/add.html')

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