from os import environ
import uuid
import json
from flask import Flask, request, url_for, jsonify
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
database_uri = 'postgresql://' + environ['pg_username'] + ':' + environ['pg_password'] + '@' + environ['pg_host'] + environ['pg_database']
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db = SQLAlchemy(app)
e = db.create_engine(database_uri, {})

#User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    email = db.Column(db.String(254), unique=True)
    age = db.Column(db.Integer)
    #TO-DO: automatic current timestamp
    timestamp = db.Column(db.TIMESTAMP)#, server_default=)

    def __repr__(self):
        return self.name
#Test1 table
class Test1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test = db.Column(db.Text)
    timestamp = db.Column(db.TIMESTAMP)

    def __repr__(self):
        return  self.test

#Run in python shell to create on EC2
#db.create_all()

#Placeholder main page
@app.route('/')
def index():
    return 'hello'

#GET info given name
@app.route('/get_info/<_name>')
def get_info(_name):
    try:
        #bug: should be all(), since name is non-unique
        user = User.query.filter_by(name=_name.strip()).first()
        return jsonify(email=user.email, age=user.age) 
    except AttributeError:
        return 'user with this name not found'

#Add user with given info
@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        res = request.json
        try:
            user = User(name=res.get('name').strip(), email=res.get('email').strip(), age=res.get('age'))
            db.session.add(user)
            db.session.commit()
            return jsonify(success=True) 
        except BaseException as error:
            return ('An exception occured: {}'.format(error))
    else:
        pass

#Add new table
@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        res = request.json
        class Object(object):
            pass
        columns = list(res)
        metadata = db.MetaData(bind=e)
        t1 = db.Table(str(uuid.uuid4()), metadata, db.Column('id', db.Integer, primary_key=True), *(db.Column(col, db.String(255)) for col in columns))
        metadata.create_all()
        db.mapper(Object, t1)
        Session = db.sessionmaker()
        Session.configure(bind=e)
        session = Session()
        w = Object()
        for col in res:
            w.col = res[col]
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
