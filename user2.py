from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
from datetime import datetime


app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)

class Sudha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)

    def __init__(self, email, created_at, updated_at):
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at


@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    email = Sudha.query.filter_by(email=data['email']).first()
    if email:
        return jsonify({'Message' : 'User with email address is already exists'}),400
    created_at = datetime.now()
    updated_at = datetime.now()
    user = Sudha(data['email'], created_at, updated_at)
    db.session.add(user)
    db.session.commit()
    return jsonify({'Message' : 'New User has been created'})


if __name__ == '__main__':
    app.run(debug=True, port=7000)




