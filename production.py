'''
Created on 17. aug. 2015

@author: Criblica
'''

from project import db, app
from project.models import *
from project.routes import *
import project.configs as configs



if __name__ == '__main__':
    
    #app.secret_key = 'This is my supersecret key that nobody knows about, except my butcher!!!'
    #app.run()
    app.config.from_object(configs.ProductionConfig)
    app.run(host="192.168.10.168", port=80, debug=True)
    #192.168.10.168