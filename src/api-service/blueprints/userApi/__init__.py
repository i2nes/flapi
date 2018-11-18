from flask import Blueprint

api = Blueprint('userApi', __name__)

from . import routes