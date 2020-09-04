import uuid
import json
from flask import Flask, request, url_for, jsonify
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy

#TO-DO: move database_uri values to ENV vars; security risk right now
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pw@ec2-18-191-192-189.us-east-2.compute.amazonaws.com/postgres'
db = SQLAlchemy(app)
e = db.create_engine('postgresql://postgres:pw@ec2-18-191-192-189.us-east-2.compute.amazonaws.com/postgres', {})

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    email = db.Column(db.String(254), unique=True)
    age = db.Column(db.Integer)
    #TO-DO: automatic current timestamp
    timestamp = db.Column(db.TIMESTAMP)#, server_default=)

    def __repr__(self):
        return self.name

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
        return jsonify(email=user.email, age=user.age) 
    except AttributeError:
        return 'user with this name not found'

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        res = request.json
        try:
            user = User(name=res.get('name'), email=res.get('email'), age=res.get('age'))
            db.session.add(user)
            db.session.commit()
            return jsonify(success=True) 
        except BaseException as error:
            return ('An exception occured: {}'.format(error))
    else:
        pass

@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        res = request.json
        class Object(object):
            pass
        columns = list(res)
        metadata = db.MetaData(bind=e)
        t1 = db.Table(str(uuid.uuid4()), metadata, db.Column('id', db.Integer, primary_key=True), *(db.Column(col, db.String(255)) for col in columns))
        print(type(t1))
        metadata.create_all()
        db.mapper(Object, t1)
        Session = db.sessionmaker()
        Session.configure(bind=e)
        session = Session()
        w = Object()
        for col in res:
            w.col = res[col]
            print(w.col)
        session.add(w)
        session.commit()
        return 'Table updated' 

with app.test_request_context():
    #Test url string format; 
    '''
    print(url_for('get_info', _name='abc'))
    '''


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
