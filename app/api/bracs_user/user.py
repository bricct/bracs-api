import json
import secrets

import bcrypt
from app import db
from app.api import api
from app.api.utils import processToken
from app.schema import Token, User
from app.utils import defaultResponse, response, UnableToCompleteAction
from app.utils.api_imports import *
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


@api.route('/post_user', methods=['POST'])
def post_user():
  try:
    data = json.loads(request.data)
    
    username = data['username']
    email = data['email']
    
    password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    user = User(username=username, password=password, email=email)

    db_session.add(user)
    db_session.commit()
  except Exception as e:
    # if username/email already exists return default response
    raise UnableToCompleteAction(e)

  return response({"userID":user.id}, 200)




@api.route('/user/<int:userID>', methods=['GET'])
def get_user(userID):

  authUser = False

  try:
    user = db_session.query(User).filter_by(id=userID).one_or_none()
    return user 
  except Exception as e:
    raise UnableToCompleteAction(e)
  # try:
  #   authUser = processToken(request.headers["Authorization"])
  # except:
  #   return defaultResponse()

  # # bad token
  # if not authUser:
  #   return defaultResponse()

  # # user is not an admin and is not getting themselves
  # if not authUser.isAdmin and authUser.id != userID:
  #   return defaultResponse()

  # user = db_session.query(User).filter_by(id=userID).one_or_none()

  # if user:
  #   return response(user, 200)
  
  # return response({"error":"user not found"}, 200)

# @app.route('/api/modify_user', methods=['PUT'])
# def modify_user():
#   data = json.loads(request.data)
#   userID = data['userID']
#   user = User.query.filter_by(id=userID).first()

@api.route('/login', methods=['POST'])
def login():

  identifier = None
  password = None

  try:
    data = json.loads(request.data)
    identifier = data['identifier']
    password = data['password']
  
  except Exception as e:
    return UnableToCompleteAction(e)

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

        return response({"token":token.token, "userID":user.id}, 200)

  # if username/email not real or password match is bad return default response

  return defaultResponse()
