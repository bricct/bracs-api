from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json
import secrets
import bcrypt
from app import db
from app.utils import defaultResponse, response
from app.schema import *

from app.api.utils import processToken

from app.utils.api_imports import *
from app.api import api


@api.route('/get_user_brackets', methods=["GET"])
def get_user_brackets():
  data = json.loads(request.data)
  userID = data["userID"]
  
  authUser = processToken(request.headers["Authorization"])

  # bad token
  if not authUser:
    return defaultResponse()

  # user is not an admin and is not getting themselves
  if (not authUser.isAdmin) and authUser.id != userID:
    return defaultResponse()

  bracketIDs = db_session.query(Bracket.id).filter_by(ownerID=userID).all()
  
  return response({"bracketIDs":bracketIDs}, 200)


@api.route('/post_bracket', methods=['POST'])
def post_bracket():
  data = json.loads(request.data)

  authUser = processToken(request.headers["Authorization"])

  # bad token
  if not authUser:
    return defaultResponse()
  
  bracket = Bracket(ownerID=authUser.id, bracketData = data["bracketData"])

  try:
    db_session.add(bracket)
    db_session.commit()
  except:
    # if team with that name already exists return default response
    return defaultResponse()

  return response({"bracketID":bracket.id}, 200)

# @api.route('/modify_bracket', methods=["PUT"])
# def modify_bracket():
#   data = json.loads(request.data)
#   name = data['username']
#   image = None
#   if 'image' in data.keys():
#     image = data['image']
#   team = Team(name=name, image=image)

#   try:
#     db_session.add(team)
#     db_session.commit()
#   except:
#     # if team with that name already exists return default response
#     return defaultResponse()

#   return response({"teamID":team.id}, 200)


@api.route('/bracket/<int:bracketID>', methods=['GET'])
def get_bracket(bracketID):

  authUser = processToken(request.headers["Authorization"])

  # bad token
  if not authUser:
    return defaultResponse()

  bracket = db_session.query(Bracket).filter_by(id=bracketID).one_or_none()

  if not authUser.isAdmin and authUser.id != bracket.ownerID:
    return defaultResponse()

  if bracket:
    return response(bracket, 200)
  
  return response({"error":"bracket not found"}, 200)


