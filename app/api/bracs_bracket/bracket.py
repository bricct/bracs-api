import json

from flask import request

from app.api import api
from app.api.utils import processToken
from app.schema import *
from app.utils import UnableToCompleteAction, defaultResponse, response
from app.utils.api_imports import *


@api.route("/get_user_brackets/<int:userID>", methods=["GET"])
def get_user_brackets(userID):
  try:
    authUser = processToken(request.headers["Authorization"])

  # # bad token or user is not an admin and is not getting themselves
    if not authUser or ((not authUser.isAdmin) and authUser.id != userID):
        return defaultResponse()

    bracketIDs = db_session.query(Bracket.id).filter_by(ownerID=userID).all()

    ids = []
    for i in bracketIDs:
        ids.extend(i)

    return response({"bracketIDs": ids}, 200)
  except Exception as e:
    raise UnableToCompleteAction(e)


@api.route("/post_bracket", methods=["POST"])
def post_bracket():
  data = json.loads(request.data)

  authUser = processToken(request.headers["Authorization"])

  # bad token
  if not authUser:
    return defaultResponse()

  bracket = Bracket(ownerID=authUser.id, bracketData=data["bracketData"])

  try:
    db_session.add(bracket)
    db_session.commit()
  except Exception as e:
    # if team with that name already exists
    return UnableToCompleteAction(e)

  return response({"bracketID": bracket.id}, 200)

@api.route('/bracket/<int:bracketID>', methods=['GET'])
def get_bracket(bracketID):
  
    try:
        authUser = processToken(request.headers["Authorization"])
        # bad token
        if not authUser:
            return defaultResponse()

        bracket = db_session.query(Bracket).filter_by(id=bracketID).one_or_none()

        if not authUser.isAdmin and authUser.id != bracket.ownerID:
            return defaultResponse()

        if bracket:
            return response(bracket, 200)
    except Exception as e:
        raise UnableToCompleteAction(e)
