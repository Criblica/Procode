import os

class Config():
    JSON_AS_ASCII = False
    SECRET_KEY = 'This is my supersecret key that nobody knows about, except my butcher!!!'
    PROFILE_IMAGES = './project/static/img/profile_images'
    ALLOWED_EXTENSIONS =  set(['png', 'jpg', 'jpeg', 'gif'])
    
    
    
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"
    DEBUG = True
    TESTING = False
    PREFERRED_URL_SCHEME = "http"
    SECRET_KEY = 'This is my supersecret key that nobody knows about, except my butcher!!!'
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///production.db"
    DEBUG = False
    TESTING = False
    #SERVER_NAME = "procode.no"
    PREFERRED_URL_SCHEME = "http"
    SECRET_KEY = os.urandom(24)