from datetime import timedelta
from flask import Flask, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_caching import Cache
from flask_jwt_extended import JWTManager
import os

from app.utils import load_app_config, UnableToCompleteAction

db = SQLAlchemy()
cache = Cache(config={"CACHE_TYPE": "simple"})

from app.api import api


def create_app(dev=False):
    app_config = load_app_config()
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["CSRF_ENABLED"] = True
    app.config["DEBUG"] = app_config["flask_debug_mode"]
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["TRAP_HTTP_EXCEPTIONS"] = True

    if dev:
        from dotenv import dotenv_values

        vals = dotenv_values()
        #
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "mysql+mysqlconnector://{}:{}@{}/{}".format(
            vals["DB_USER"], vals["DB_PASS"], vals["DB_URI"], vals["DB_NAME"]
        )
        app.secret_key = vals["FLASK_KEY"]

    else:
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "mysql+mysqlconnector://{}:{}@{}/{}".format(
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            os.environ["DB_URI"],
            os.environ["DB_NAME"],
        )
        app.secret_key = os.environ["FLASK_KEY"]

    cache.init_app(app)

    db.init_app(app)

    cors = CORS(app, supports_credentials=True)
    app.register_blueprint(api, url_prefix="/api")

    JWTManager(app)

    @app.before_request
    def extend_session():
        session.permanent = True
        app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=31)
        session.modified = True

    @app.route("/", methods=["GET"])
    def default():
        app_config = load_app_config()
        return jsonify({"version": app_config["server_version"]})

    @app.errorhandler(UnableToCompleteAction)
    def unable_to_complete(err):
        res = jsonify(error=str(err.error), status=err.status)
        return res

    return app
