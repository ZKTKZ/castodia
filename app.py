import json
from flask import Flask, request, url_for, jsonify
from markupsafe import escape
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
    timestamp = db.Column(db.TIMESTAMP)#, server_default=)

    def __repr__(self):
        return self.name

#CREATE TABLE test1(id int GENERATED ALWAYS AS IDENTITy, test text, time_stamp TIMESTAMPtz);
class Test1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test = db.Column(db.Text)
    timestamp = db.Column(db.TIMESTAMP)

    def __repr__(self):
        return  self.test

#ORM -> DB with the following
#db.create_all()

@app.route('/')
def index():
    return 'hello'

@app.route('/get_info/<_name>')
def get_info(_name):
    try:
        user = User.query.filter_by(name=_name).first()
        #TO-DO: return name as "outer key" of JSON
        return jsonify(email=user.email, age=user.age) 
    except AttributeError:
        return 'user with this name not found'

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        res = request.json
        print('response type: ' + str(type(res)))
        user = User(name=res.get('name'), email=res.get('email'), age=res.get('age'))
        db.session.add(user)
        db.session.commit()
        return res.get('name') 
    else:
        #TO-DO: hrow proper rror handler
        pass

#since data is arbitrary, storing JSON obj as dictionary
#root nodes aka top-level keys are SQL columns
@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        res = request.json
        keys = list(res)
        #table = db.Table('Table1', db.Column(
        return str((list(res)))

with app.test_request_context():
    #Test url string format; 
    print(url_for('get_info', _name='abc'))

    #Test return value
    #print(get_info('abc'))

