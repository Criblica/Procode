from flask import Flask, render_template, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug import secure_filename
import datetime
import time
#from datetime import timedelta, datetime
import json
import os

   
app = Flask(__name__)

app.config['PROFILE_IMAGES'] = './static/img/profile_images'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])


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
    image_src = db.Column(db.String, unique=False, default=app.config['PROFILE_IMAGES']+"/no-profile.gif")
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    admin = db.Column(db.Boolean, nullable=False, default=False) 
    banned = db.Column(db.Boolean, nullable=False, default=False) 
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        
        
class CodeSnippet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), default="code snippet", nullable=False, unique=False)
    author =  db.Column(db.String(16), nullable=False, unique=False)
    image_src = db.Column(db.String, unique=False)
    date = db.Column(db.String(20), default=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), unique=False)
    language = db.Column(db.String(255), nullable=False, unique=False)
    title = db.Column(db.String(255), nullable=False, unique=False)
    code = db.Column(db.Text, nullable=False, unique=False)
    prewords = db.Column(db.Text, unique=False)
    afterwords = db.Column(db.Text, unique=False)
    
    def __init__(self, author, image_src, language, title, code, prewords, afterwords):
        self.author = author
        self.image_src = image_src
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
    image_src = db.Column(db.String, unique=False)
    date = db.Column(db.String(20), default=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), unique=False)
    answered = db.Column(db.Boolean, default=False)
    
    def __init__(self, author, image_src, title, question):
        self.author = author
        self.image_src = image_src
        self.title = title
        self.question = question

class Findout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=False)
    findout = db.Column(db.Text, nullable=False, unique=False)
    type = db.Column(db.String(20), default="findout", nullable=False, unique=False)
    author =  db.Column(db.String(16), nullable=False, unique=False)
    image_src = db.Column(db.String, unique=False)
    date = db.Column(db.String(20), default=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), unique=False)
    
    def __init__(self, author, image_src, title, findout):
        self.author = author
        self.image_src = image_src
        self.title = title
        self.findout = findout
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, nullable=False, unique=False)
    article_type = db.Column(db.String(20), nullable=False, unique=False)
    message = db.Column(db.Text, nullable=False, unique=False)
    author =  db.Column(db.String(16), nullable=False, unique=False) 
    image_src = db.Column(db.String, unique=False)
    date = db.Column(db.String(20), default=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), unique=False)
    
    def __init__(self, article_id, article_type, message, author, image_src):
        self.article_id = article_id
        self.article_type = article_type
        self.message = message
        self.author = author
        self.image_src = image_src
        
"""  
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=False)
    message = db.Column(db.Text, nullable=False, unique=False)
    date = db.Column(db.String(20), default=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), unique=False)
    
    def __init__(self, title, message, date):
        self.title = title
        self.message = message
        self.date = date
        
"""
db.create_all()


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(hours=12) 

def login_required(f):
    @wraps(f)
    def login_redirect(*args, **kwargs):
        if 'logged_in' in session:
            if session['logged_in']:
                return f(*args, **kwargs)
        return redirect(url_for('home'))
       
    return login_redirect
    
"""
def admin_required(f):
    @wraps(f)
    def admin_redirect(*args, **kwargs):
        if 'role' in session:
            if session['role'] == 'admin':
                return f(*args, **kwargs)
        return redirect(url_for('home'))
    return admin_redirect
"""    

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
    #code_snippets = CodeSnippet.query.all()
    #questions = Question.query.all()
    #findouts = Findout.query.all()
    #return render_template('articles/code_snippets.html', code_snippets=code_snippets, questions=questions, findouts=findouts)
    return redirect(url_for('all_code_snippets'))
  
@app.route('/articles/code_snippets')
def all_code_snippets():
    code_snippets = CodeSnippet.query.all()
    return render_template('articles/code_snippets.html', code_snippets=code_snippets)

@app.route('/articles/questions')
def all_questions():
    questions = Question.query.all()
    return render_template('articles/questions.html', questions=questions)

@app.route('/articles/findouts')
def all_findouts():
    findouts = Findout.query.all()
    return render_template('articles/findouts.html', findouts=findouts)
  
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
            session['image_src'] = user.image_src
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
    session.pop('image_src', None)
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
    
    new_user = User(request.form['username'], request.form['password'], request.form['email'])
    db.session.add(new_user)
    db.session.commit()

    return json.dumps({'message': "OK", 'iserror': False})
  
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_profile_image():
    code_snippets = CodeSnippet.query.filter_by(author=session['username'])
    questions = Question.query.filter_by(author=session['username'])
    findouts = Findout.query.filter_by(author=session['username'])  
    return render_template('upload.html', code_snippets=code_snippets, questions=questions, findouts=findouts)
  
@app.route('/save_image', methods=['GET', 'POST'])
@login_required
def save_image():
    image = request.files['file']
    if image and allowed_file(image.filename):
        _, file_extension = os.path.splitext(image.filename)
        #filename = secure_filename(image.filename)
        #path = os.path.join(app.config['PROFILE_IMAGES'], filename)
        path = os.path.join(app.config['PROFILE_IMAGES'], session['username']+file_extension)
        image.save(path)
        
        user = User.query.filter_by(id=session['id']).first()
        user.image_src = path
        db.session.commit()
        session['image_src'] = path
        
        change_profile_image()
    return redirect(url_for('home'))

@app.route('/use_image', methods=['GET', 'POST'])
@login_required
def use_image():
    user = User.query.filter_by(id=session['id']).first()
    user.image_src = request.json['image_src']
    db.session.commit()
    session['image_src'] = user.image_src
    
    change_profile_image()
    
    return json.dumps({'message': "OK", 'iserror': False})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def change_profile_image():
    code_snippets = CodeSnippet.query.filter_by(author=session['username'])
    questions = Question.query.filter_by(author=session['username'])
    findouts = Findout.query.filter_by(author=session['username'])
    comments = Comment.query.filter_by(author=session['username'])
    
    for code_snippet in code_snippets:
        code_snippet.image_src = session['image_src']
    for question in questions:
        question.image_src = session['image_src']
    for findout in findouts:
        findout.image_src = session['image_src']
    for comment in comments:
        comment.image_src = session['image_src']
    db.session.commit()

"""
    Routes for articles
"""
@app.route('/articles/add')
@login_required
def add_article():
    return render_template('articles/add.html')


@app.route('/articles/create_code_snippet', methods=['GET', 'POST'])
@login_required
def create_code_snippet():
    title = request.json['title']
    code = request.json['code']
    prewords = request.json['prewords']
    afterwords = request.json['afterwords']
    language = request.json['language']
    
    code_snippet = CodeSnippet(session['username'], session['image_src'], language, title, code, prewords, afterwords)
    db.session.add(code_snippet)
    db.session.commit()
    return json.dumps(dict(message="OK", iserror=False))

@app.route('/articles/create_question', methods=['GET', 'POST'])  
@login_required
def create_question():
    title = request.json['title']
    question_message = request.json['question']
    
    question = Question(session['username'], session['image_src'], title, question_message)
    db.session.add(question)
    db.session.commit()
    return json.dumps(dict(message="OK", iserror=False))

@app.route('/articles/create_findout', methods=['GET', 'POST'])
@login_required
def create_findout():
    title = request.json['title']
    findout_message = request.json['findout']
    
    findout = Findout(session['username'], session['image_src'], title, findout_message)
    db.session.add(findout)
    db.session.commit()
    return json.dumps(dict(message="OK", iserror=False))

@app.route('/articles/code_snippet/<code_snippet_id>')
def view_code_snippet(code_snippet_id):
    code_snippet = CodeSnippet.query.filter_by(id=code_snippet_id).first()
    comments = Comment.query.filter_by(article_id=code_snippet_id, article_type=code_snippet.type)
    return render_template('/articles/article.html', article=code_snippet, comments=comments)

@app.route('/articles/question/<question_id>')
def view_question(question_id):
    question = Question.query.filter_by(id=question_id).first()
    comments = Comment.query.filter_by(article_id=question_id, article_type=question.type)    
    return render_template('/articles/article.html', article=question, comments=comments)

@app.route('/articles/findout/<findout_id>')
def view_findout(findout_id):
    findout = Findout.query.filter_by(id=findout_id).first()
    comments = Comment.query.filter_by(article_id=findout_id, article_type=findout.type)
    return render_template('/articles/article.html', article=findout, comments=comments)


@app.route('/articles/post_comment', methods=['GET', 'POST'])
@login_required
def post_comment():
    message = request.json['message']
    article_id = request.json['article_id']
    article_type = request.json['article_type']
    
    comment = Comment(article_id, article_type, message, session['username'], session['image_src'])
    db.session.add(comment)
    db.session.commit()
    return json.dumps(dict(message="OK", iserror=False))

@app.route('/articles/<question_id>=answered', methods=['GET', 'POST'])
@login_required
def answered(question_id):
    question = Question.query.filter_by(id=question_id).first()
    question.answered = True
    db.session.commit()
    return redirect(url_for('view_question', question_id=question_id))

@app.route('/articles/<question_id>=not_answered', methods=['GET', 'POST'])
@login_required
def not_answered(question_id):
    question = Question.query.filter_by(id=question_id).first()
    question.answered = False
    db.session.commit()
    return redirect(url_for('view_question', question_id=question_id))
   

if __name__ == '__main__':
    app.secret_key = 'This is my supersecret key that nobody knows about, except my butcher!!!'
    #app.run(debug=True)
    app.run(host="192.168.10.168", port=5000, debug=True)
    