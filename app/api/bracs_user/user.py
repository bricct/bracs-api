from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json
import secrets
import bcrypt
from app import db
from app.utils import defaultResponse, response
from app.schema import User, Token

from app.api.utils import processToken

from app.utils.api_imports import *
from app.api import api




@api.route('/post_user', methods=['POST'])
def post_user():
  data = json.loads(request.data)
  username = data['username']
  email = data['email']
  password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
  user = User(username=username, password=password, email=email)

  try:
    db_session.add(user)
    db_session.commit()
  except:
    # if username/email already exists return default response
    return defaultResponse()

  return response({"userID":user.id}, 200)




@api.route('/user/<int:userID>', methods=['GET'])
def get_user(userID):

  authUser = processToken(request.headers["Authorization"])

  # bad token
  if not authUser:
    return defaultResponse()

  # user is not an admin and is not getting themselves
  if not authUser.isAdmin and authUser.id != userID:
    return defaultResponse()

  user = db_session.query(User).filter_by(id=userID).one_or_none()

  if user:
    return response(user, 200)
  
  return response({"error":"user not found"}, 200)

# @app.route('/api/modify_user', methods=['PUT'])
# def modify_user():
#   data = json.loads(request.data)
#   userID = data['userID']
#   user = User.query.filter_by(id=userID).first()

@api.route('/login', methods=['POST'])
def login():
  data = json.loads(request.data)

  identifier = data['identifier']
  password = data['password']

  userFound = False

  # first try logging in with username 
  user = db_session.query(User).filter_by(username=identifier).one_or_none()

  if user:
    userFound = True

  else:
    # now try logging in with email
    user = db_session.query(User).filter_by(email=identifier).one_or_none()
    if user:
      userFound = True

  if userFound:

    # if user found check password match & give token
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        token = Token(userID=user.id, token=secrets.token_hex(256))
        db.session.add(token)
        db.session.commit()

        return response({"token":token.token}, 200)

  # if username/email not real or password match is bad return default response

  return defaultResponse()