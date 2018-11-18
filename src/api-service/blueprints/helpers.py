# Helper Functions
import re
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def meta(status_code, message):
    return { 'http_code': status_code, 'message': message }


def isvalidEmail(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


# HTTP Error Handler
def handle_http_error(e):

    response = {
        'meta': meta(e.code, HTTP_STATUS_CODES.get(e.code)),
    }
    
    return jsonify(response), e.code
