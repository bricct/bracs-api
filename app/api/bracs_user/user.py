import json
import secrets

import bcrypt
from flask import request

from app import db
from app.api import api
from app.api.utils import processToken
from app.schema import Token, User
from app.utils import UnableToCompleteAction, defaultResponse, response
from app.utils.api_imports import db_session


@api.route("/post_user", methods=["POST"])
def post_user():
    try:
        data = json.loads(request.data)

        username = data["username"]
        email = data["email"]

        password = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())
        user = User(username=username, password=password, email=email)

        db_session.add(user)
        db_session.commit()
        return response({"userID": user.id}, 200)
    except Exception as e:
        # if username/email already exists return default response
        raise UnableToCompleteAction(e)

@api.route('/user/<int:userID>', methods=['GET'])
def get_user(userID):
  try:
    authUser = processToken(request.headers["Authorization"])

    # # bad token or user is not an admin and is not getting themselves
    if not authUser or ((not authUser.isAdmin) and authUser.id != userID):
        return defaultResponse()


    user = db_session.query(User).filter_by(id=userID).one_or_none()
    return response(user, 200)
  except Exception as e:
    raise UnableToCompleteAction(e)


@api.route("/login", methods=["POST"])
def login():
    identifier = None
    password = None
    try:
        data = json.loads(request.data)
        identifier = data["identifier"]
        password = data["password"]  # mad secure bruh
        user = db_session.query(User).filter_by(username=identifier).one_or_none()
        if user is None:
            user = db_session.query(User).filter_by(email=identifier).one_or_none()
        if user and bcrypt.checkpw(
            password.encode("utf-8"), user.password.encode("utf-8")
        ):
            token = Token(userID=user.id, token=secrets.token_hex(256))
            db.session.add(token)
            db.session.commit()

            return response({"token": token.token, "userID": user.id}, 200)
        else:
            raise Exception("Error: Could not verify user")
    except Exception as e:
        raise UnableToCompleteAction(e)
