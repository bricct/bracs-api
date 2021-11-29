from datetime import timedelta
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_caching import Cache
from flask_jwt_extended import JWTManager

from app.utils import load_app_config

db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'simple'})

from app.api import api


def create_app():
  app_config = load_app_config()
  app = Flask(__name__)
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['CSRF_ENABLED'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = app_config['database_uri']
  app.config['DEBUG'] = app_config['flask_debug_mode']
  app.config['SESSION_TYPE'] = 'filesystem'
  app.config['TRAP_HTTP_EXCEPTIONS']=True
  app.secret_key = app_config['flask_login_secret']

  cache.init_app(app)

  db.init_app(app)

  cors = CORS(app, supports_credentials=True)
  app.register_blueprint(api, url_prefix='/api')

  jwt = JWTManager(app)

  @app.before_request
  def extend_session():
    session.permanent = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
    session.modified = True

  return app

