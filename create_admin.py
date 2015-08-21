from project import db
from project.models import User

def create_admin():
    username = "Einar"
    password = "123456"
    email = "einkri1991@gmail.com"
    
    user = User(username, password, email)
    user.admin = True
    
    db.session.add(user)
    db.session.commit()
    
if __name__ == "__main__":
    create_admin()