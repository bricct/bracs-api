from app.schema import Token, User
from app.utils.api_imports import db_session


def processToken(token):
    token = token[7:]

    uToken = db_session.query(Token).filter_by(token=token).one_or_none()

    if uToken:
        user = db_session.query(User).filter_by(id=uToken.userID).one_or_none()
        return user

    return None
