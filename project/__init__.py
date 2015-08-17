'''
Created on 17. aug. 2015

@author: Criblica
'''

from flask import Flask, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['PROFILE_IMAGES'] = './static/img/profile_images'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///development.db"

db = SQLAlchemy(app)

