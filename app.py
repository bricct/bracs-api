from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json
import secrets
import bcrypt

from sqlalchemy import Column, DECIMAL, Date, DateTime, Float, ForeignKey, Index, JSON, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, TINYINT


from sqlalchemy.ext.declarative import DeclarativeMeta



def get_db_credentials():
	file = open("db-credentials.txt", "r")
	db_vars = {}
	for line in file:
		line = line.rstrip()
		lVars = line.split(" ")
		db_vars[lVars[0]] = lVars[1]
	return db_vars

db_vars = get_db_credentials()

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(db_vars['BRACS_DB_USER'], db_vars['BRACS_DB_PASS'], db_vars['BRACS_DB_HOST'], db_vars['BRACS_DB_PORT'], db_vars['BRACS_DB_NAME'])

db = SQLAlchemy(app)

class User(db.Model):
  id = Column(INTEGER, primary_key=True)
  username = Column(VARCHAR(64), unique=True, nullable=False)
  password = Column(VARCHAR(1024), nullable=False)
  isAdmin = Column(TINYINT, nullable=False, server_default=text('0'))
  createdAt = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
  updatedAt = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

class Token(db.Model):
  id = Column(INTEGER, primary_key=True)
  userID = Column(INTEGER, ForeignKey("user.id"), nullable=False)
  token = Column(VARCHAR(256), nullable=False)
  createdAt = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
  updatedAt = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


def response(data, code):
  return json.dumps(data, cls=AlchemyEncoder), code

def defaultResponse(success=False):

  if success:
    return response({}, 200)
  else:
    return response({"error":"Request Rejected"}, 200)


def processToken(token):
  token = token[7:]

  uToken = Token.query.filter_by(token=token).one_or_none()

  if uToken:
    user = User.query.filter_by(id=uToken.userID).one_or_none()
    return user

  return None



class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            restrictedFields = ['metadata', 'query', 'query_class', 'password', 'createdAt', 'updatedAt', 'isAdmin']
            for field in [x for x in dir(obj) if not x.startswith('_') and x not in restrictedFields]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)




@app.route('/api/post_user', methods=['POST'])
def post_user():
  data = json.loads(request.data)
  username = data['username']
  password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
  user = User(username=username, password=password)

  try:
    db.session.add(user)
    db.session.commit()
  except:
    return defaultResponse()


  return response({"userID":user.id}, 200)




@app.route('/api/user/<int:userID>', methods=['GET'])
def get_user(userID):

  authUser = processToken(request.headers["Authorization"])

  # bad token
  if not authUser:
    return defaultResponse()

  # user is not an admin and is not getting themselves
  if not authUser.isAdmin and authUser.id != userID:
    return defaultResponse()

  user = User.query.filter_by(id=userID).first()

  return response(user, 200)

# @app.route('/api/modify_user', methods=['PUT'])
# def modify_user():
#   data = json.loads(request.data)
#   userID = data['userID']
#   user = User.query.filter_by(id=userID).first()

@app.route('/api/login', methods=['POST'])
def login():
  data = json.loads(request.data)

  username = data['username']
  password = data['password']

  user = User.query.filter_by(username=username).one_or_none()

  if user:
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        token = Token(userID=user.id, token=secrets.token_hex(256))
        db.session.add(token)
        db.session.commit()

        return response({"token":token.token}, 200)

  return defaultResponse()


#@app.route('/api/reset_password', methods=['POST'])

  




