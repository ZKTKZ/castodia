from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#TO-DO: move database_uri values to ENV vars
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pw@ec2-18-191-192-189.us-east-2.compute.amazonaws.com/postgres'
db = SQLAlchemy(app)

class User(db.Model):
    name = db.Column(db.String(128), primary_key=True)
    email = db.Column(db.String(254), unique=True)
    age = db.Column(db.Integer)
    #TO-DO: automatic current timestamp
    timestamp = db.Column(db.TIMESTAMP, server_default=)

    def __repr__(self):
        return self.name

#CREATE TABLE test1(id int GENERATED ALWAYS AS IDENTITy, test text, time_stamp TIMESTAMPtz);
class Test1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test = db.Column(db.Text)
    timestamp = db.Column(db.TIMESTAMP)

    def __repr__(self):
        return  self.test

#TO-DO: confirm primary_key is internally checked for uniqueness

#ORM -> DB with the following
#db.create_all()
