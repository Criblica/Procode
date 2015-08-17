'''
Created on 17. aug. 2015

@author: Criblica
'''

from project import *
import time

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False, unique=False)
    email = db.Column(db.String(60), nullable=False, unique=True)   
    image_src = db.Column(db.String, unique=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    admin = db.Column(db.Boolean, nullable=False, default=False) 
    banned = db.Column(db.Boolean, nullable=False, default=False) 
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.image_src = url_for('static', filename='img/profile_images/no-profile.gif')
        
        
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
    answered = db.Column(db.Boolean, default=False)
    
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
    image_src = db.Column(db.String, unique=False)
    date = db.Column(db.String(20), default=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), unique=False)
    
    def __init__(self, article_id, article_type, message, author, image_src):
        self.article_id = article_id
        self.article_type = article_type
        self.message = message
        self.author = author
        self.image_src = image_src
        

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