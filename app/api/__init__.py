from flask import Blueprint, jsonify
import requests, json
from app.utils import load_app_config

api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
def default():
  app_config = load_app_config()
  return jsonify({
    'version': app_config['server_version']
  })

from app.api.bracs_user.user import *
from app.api.bracs_bracket.bracket import *
