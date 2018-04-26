from flask import Flask
from flask import request, jsonify
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_httpauth import HTTPBasicAuth   #Flask-HTTPAuth an endpoint is protected by adding the login_required decorator
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)
auth = HTTPBasicAuth()


class Sree(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(40), index = True)
    password = db.Column(db.String(128))

   #def __init__(self, username, created_at, updated_at):
        #self.username = username
        #self.password = password
        #self.created_at = created_at
        #self.updated_at = updated_at"""

    def hash_password(self, password):    #This method is called when a new user is registering with the server, or when the user changes the password.
        self.password_hash = pwd_context.encrypt(password)
    def verify_password(self, password):  #This method is called whenever the user provides credentials and they need to be validated.
        return pwd_context.verify(password, self.password.hash)

@app.route('/api/users', methods = ['POST'])
def new_user():
    #data = request.get_json()
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:         #abort(400)  & Missing arguments
        return  jsonify({'message' : 'Username or Password is None'})
    if users.query.filter_by(username = username).first() is not None:     #abort(400), For Existing User
        return jsonify({'message' : 'Username is already existed'})
    #created_at = datetime.now()
    #updated_at = datetime.now()
    #user = Sree(data['username'], created_at, updated_at)  #New user creating
    user = users(username = username)
    user.hash_password(password)     #Password Creating
    db.session.add(user)
    db.session.commit()
    return jsonify({'username' : user.username}), 201, {'Location' : url_for('get_user', id = user.id, _external = True)}
                    #201 status code for "Created"  && Location header pointing to the URI of newly created User

@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data' : 'Hello, %s!' % g.user.username})

@auth.verify_password
def verify_password(username, password):
    user = users.query.filter_by(username = username).first()  #Finds the user by user name
    if not user or not user.verify_password(password):    #Verifies the password using verify_password method
        return False
    g.user = user   #the user is stored in Flask's g object so that the view function can use it.
    return True

#Token Based Authentication


if __name__ == '__main__':
    app.run(debug=True, port = 6000)






