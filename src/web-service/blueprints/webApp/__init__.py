from flask import Blueprint

app = Blueprint('webApp', __name__)

from . import routes