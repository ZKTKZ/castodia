from flask import Flask, request, url_for
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy

#TO-DO: move database_uri values to ENV vars
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pw@ec2-18-191-192-189.us-east-2.compute.amazonaws.com/postgres'
db = SQLAlchemy(app)

class User(db.Model):
    #TO-DO: confirm primary_key is internally checked for uniqueness
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

@app.route('/get_info/<name>')
def get_info(__name):
    user = User.query.filter_by(name=__name).first()
    return escape('email: %s' % user.email + ', age: %s ' % user.age)

#Test url string format; 
with app.test_request_context():
    print(url_for('get_info', name='abc'))

#Test return value
print(get_info('abc'))
