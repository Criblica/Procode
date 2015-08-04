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
    email = db.Column(db.String(60), nullable=False, unique=True)   
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    admin = db.Column(db.Boolean, nullable=False, default=False) 
    
    def __init__(self, username, password, email, confirmed, admin):
        self.username = username
        self.password = password
        self.email = email
        self.confirmed = confirmed
        self.admin = admin
        
class CodeSnippet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(255), nullable=False, unique=False)
    title = db.Column(db.String(255), nullable=False, unique=False)
    code = db.Column(db.Text, nullable=False, unique=False)
    author =  db.Column(db.Integer, nullable=False, unique=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow, unique=False)
    
    def __init__(self, language, title, code, author):
        self.language = language
        self.title = title
        self.code = code
        self.author = author
    
    def to_json(self):
        return dict(language=self.language, title=self.title, code=self.code, author=self.author, date=self.date)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=False)
    author =  db.Column(db.String(16), nullable=False, unique=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow, unique=False)
    question = db.Column(db.Text, nullable=False, unique=False)
    
    def __init__(self, title, question, author):
        self.title = title
        self.question = question
        self.author = author
    
    def to_json(self):
        return dict(title=self.title,question=self.question, author=self.author)

class Findout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=False)
    author =  db.Column(db.String(16), nullable=False, unique=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow, unique=False)
    findout = db.Column(db.Text, nullable=False, unique=False)
    
    def __init__(self, title, findout, author):
        self.title = title
        self.findout = findout
        self.author = author
    
    def to_json(self):
        return dict(title=self.title,findout=self.findout, author=self.author)

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
    if 'logged_in' in session:
        if session['logged_in']:
            code_snippets = CodeSnippet.query.filter_by(author=session['id'])
            questions = Question.query.filter_by(author=session['id'])
            findouts = Findout.query.filter_by(author=session['id'])            
            return render_template('home.html', code_snippets=code_snippets, questions=questions, findouts=findouts)
    return render_template('home.html')

@app.route('/articles')
def articles():
    return render_template('articles/index.html')
  
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
            session['id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            return json.dumps({'message':"OK", 'iserror': False})
        else:
            return json.dumps({'message': "Wrong password. Please try again!", 'iserror': True})
    else:
        return json.dumps({'message': "This username does not exist!", 'iserror': True})
    
    

@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
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
    
    db.session.add(User(request.form['username'], request.form['password'], request.form['email'], False, False))
    db.session.commit()

    return json.dumps({'message': "OK", 'iserror': False})
  
"""
    Routes for tutorials
"""
@app.route('/articles/add')
def add_article():
    return render_template('articles/add.html')

@app.route('/articles/create_code_snippet', methods=['GET', 'POST'])
def create_code_snippet():
    title = request.json['title']
    code = request.json['code']
    language = request.json['language']
    
    code_snippet = CodeSnippet(language, title, code, session['id'])
    db.session.add(code_snippet)
    db.session.commit()
    
    return json.dumps(dict(message="OK", iserror=False))

@app.route('/articles/create_question', methods=['GET', 'POST'])
def create_question():
    title = request.json['title']
    question = request.json['question']
    
    question = Question(title, question, session['id'])
    db.session.add(question)
    db.session.commit()
    
    return json.dumps(dict(message="OK", iserror=False))

@app.route('/articles/create_findout', methods=['GET', 'POST'])
def create_findout():
    title = request.json['title']
    findout = request.json['findout']
    
    findout = Findout(title, findout, session['id'])
    db.session.add(findout)
    db.session.commit()
    
    return json.dumps(dict(message="OK", iserror=False))

@app.route('/articles/python')
def python():
    return render_template('articles/python.html')

@app.route('/articles/java')
def java():
    return render_template('/articles/java.html')

@app.route('/articles/c')
def c():
    return render_template('/articles/c.html')

@app.route('/articles/code_snippets/<snippet_id>')
def view_code_snippet(snippet_id):
    code_snippet = CodeSnippet.query.filter_by(id=snippet_id).first()
    print code_snippet.language
    return render_template('/articles/code_snippet.html', code_snippet=code_snippet)

if __name__ == '__main__':
    app.secret_key = 'This is my supersecret key that nobody knows about, except my butcher!!!'
    app.run(debug=True)