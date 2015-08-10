from flask import Flask, render_template, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
import time
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
    type = db.Column(db.String(20), default="code snippet", nullable=False, unique=False)
    author =  db.Column(db.String(16), nullable=False, unique=False)
    date = db.Column(db.String(20), default=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), unique=False)
    language = db.Column(db.String(255), nullable=False, unique=False)
    title = db.Column(db.String(255), nullable=False, unique=False)
    code = db.Column(db.Text, nullable=False, unique=False)
    prewords = db.Column(db.Text, unique=False)
    afterwords = db.Column(db.Text, unique=False)
    
    def __init__(self, author, language, title, code, prewords, afterwords):
        self.author = author
        self.language = language
        self.title = title
        self.code = code
        self.prewords = prewords
        self.afterwords = afterwords

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=False)
    question = db.Column(db.Text, nullable=False, unique=False)
    type = db.Column(db.String(20), default="question", nullable=False, unique=False)
    author =  db.Column(db.String(16), nullable=False, unique=False)
    date = db.Column(db.String(20), default=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), unique=False)
    
    def __init__(self, author, title, question):
        self.author = author
        self.title = title
        self.question = question

class Findout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=False)
    findout = db.Column(db.Text, nullable=False, unique=False)
    type = db.Column(db.String(20), default="findout", nullable=False, unique=False)
    author =  db.Column(db.String(16), nullable=False, unique=False)
    date = db.Column(db.String(20), default=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), unique=False)
    
    def __init__(self, author, title, findout):
        self.author = author
        self.title = title
        self.findout = findout
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, nullable=False, unique=False)
    article_type = db.Column(db.String(20), nullable=False, unique=False)
    message = db.Column(db.Text, nullable=False, unique=False)
    author =  db.Column(db.String(16), nullable=False, unique=False) 
    date = db.Column(db.String(20), default=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), unique=False)
    
    def __init__(self, article_id, article_type, message, author):
        self.article_id = article_id
        self.article_type = article_type
        self.message = message
        self.author = author
        
   
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=False)
    message = db.Column(db.Text, nullable=False, unique=False)
    date = db.Column(db.String(20), default=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), unique=False)
    
    def __init__(self, title, message, date):
        self.title = title
        self.message = message
        self.date = date
        

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
            code_snippets = CodeSnippet.query.filter_by(author=session['username'])
            questions = Question.query.filter_by(author=session['username'])
            findouts = Findout.query.filter_by(author=session['username'])   
            return render_template('home.html', code_snippets=code_snippets, questions=questions, findouts=findouts)
    return render_template('home.html')

@app.route('/articles')
def articles():
    code_snippets = CodeSnippet.query.all()
    questions = Question.query.all()
    findouts = Findout.query.all()
    return render_template('articles/index.html', code_snippets=code_snippets, questions=questions, findouts=findouts)
  
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
    prewords = request.json['prewords']
    afterwords = request.json['afterwords']
    language = request.json['language']
    
    code_snippet = CodeSnippet(session['username'], language, title, code, prewords, afterwords)
    db.session.add(code_snippet)
    db.session.commit()
    return json.dumps(dict(message="OK", iserror=False))

@app.route('/articles/create_question', methods=['GET', 'POST'])  
def create_question():
    title = request.json['title']
    question_message = request.json['question']
    
    question = Question(session['username'], title, question_message)
    db.session.add(question)
    db.session.commit()
    return json.dumps(dict(message="OK", iserror=False))

@app.route('/articles/create_findout', methods=['GET', 'POST'])
def create_findout():
    title = request.json['title']
    findout_message = request.json['findout']
    
    findout = Findout(session['username'], title, findout_message)
    db.session.add(findout)
    db.session.commit()
    return json.dumps(dict(message="OK", iserror=False))

@app.route('/articles/code_snippet/<code_snippet_id>')
def view_code_snippet(code_snippet_id):
    code_snippet = CodeSnippet.query.filter_by(id=code_snippet_id).first()
    comments = Comment.query.filter_by(id=code_snippet_id, article_type="code_snippet")
    return render_template('/articles/article.html', article=code_snippet, comments=comments)

@app.route('/articles/question/<question_id>')
def view_question(question_id):
    question = Question.query.filter_by(id=question_id).first()
    comments = Comment.query.filter_by(id=question_id, article_type="question")    
    return render_template('/articles/article.html', article=question, comments=comments)

@app.route('/articles/code_snippet/<findout_id>')
def view_findout(findout_id):
    findout = Findout.query.filter_by(id=findout_id).first()
    comments = Comment.query.filter_by(id=findout_id, article_type="findout")
    return render_template('/articles/article.html', article=findout, comments=comments)


@app.route('/articles/post_comment', methods=['GET', 'POST'])
def post_comment():
    message = request.json['message']
    article_id = request.json['article_id']
    article_type = request.json['article_type']
    
    comment = Comment(article_id, article_type, message, session['username'])
    
    print comment.id
    print comment.message
    print comment.article_id
    print comment.article_type
    print comment.author
    print comment.date
    
    db.session.add(comment)
    db.session.commit()
    return json.dumps(dict(message="OK", iserror=False))

if __name__ == '__main__':
    app.secret_key = 'This is my supersecret key that nobody knows about, except my butcher!!!'
    app.run(debug=True)