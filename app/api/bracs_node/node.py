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




@api.route('/post_node', methods=['POST'])
def post_game():
  data = json.loads(request.data)
  name = data['username']
  image = None
  if 'image' in data.keys():
    image = data['image']
  team = Team(name=name, image=image)

  try:
    db_session.add(team)
    db_session.commit()
  except:
    # if team with that name already exists return default response
    return defaultResponse()

  return response({"teamID":team.id}, 200)




@api.route('/node/<int:nodeID>', methods=['GET'])
def get_game(nodeID):

  authUser = processToken(request.headers["Authorization"])

  # bad token
  if not authUser:
    return defaultResponse()

  # user is not an admin and is not getting themselves
  if not authUser.isAdmin:
    return defaultResponse()

  node = db_session.query(Node).filter_by(id=nodeID).one_or_none()

  if node:
    return response(node, 200)
  
  return response({"error":"user not found"}, 200)


