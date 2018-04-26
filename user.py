from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(55), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    country = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(30), nullable=False)
    meal = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, fullname, email, password, dob, country, gender, meal, created_at, updated_at):
        self.fullname = fullname
        self.password = password
        self.email = email
        self.dob = dob
        self.country = country
        self.gender = gender
        self.meal = meal
        self.created_at = created_at
        self.updated_at = updated_at


@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    email = Users.query.filter_by(email=data['email']).first()
    if email:
        return jsonify({'message': 'User with email address already exist'}), 400
    created_at = datetime.now()
    updated_at = datetime.now()
    user = Users(data['fullname'], data['email'], data['password'], data['dob'], data['country'], data['gender'],
                 data['meal'], created_at, updated_at)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'New user has been created successfully'})


@app.route('/user/<user_id>', methods=['GET'])
def get_user_with_id(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'user not found', 'success': False}), 400
    output = {'id': user.id, 'fullname': user.fullname, 'email': user.email, 'password': user.password, 'dob': user.dob,
              'country': user.country, 'gender': user.gender,'meal': user.meal, 'created_at': user.created_at,
              'updated_at': user.updated_at}
    return jsonify({'user': output})


@app.route('/user', methods=['GET'])
def get_all_users():
    users = Users.query.all()
    output = []
    for user in users:
        data = {'id': user.id, 'fullname': user.fullname, 'email': user.email, 'password': user.password,
                  'dob': user.dob, 'country': user.country, 'gender': user.gender, 'meal': user.meal, 'created_at': user.created_at,
                  'updated_at': user.updated_at}
        output.append(data)
    return jsonify({'users': output, 'total': len(output),'success': True})


@app.route('/user/<user_id>', methods=['PUT'])
def update_user_with_id(user_id):
    data = request.get_json()
    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'user not found', 'success': False}), 400
    user.fullname = data['fullname']
    user.password = data['password']
    user.dob = data['dob']
    user.country = data['country']
    user.gender = data['gender']
    user.meal = data['meal']
    user.updated_at = datetime.now()
    db.session.commit()
    return jsonify({'message': 'user has been updated successfully'})


@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user_with_user_id(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'user not found', 'success': False}), 400
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'user deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)