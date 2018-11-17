import logging
from . import api
from flask import Flask, jsonify, request
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import BadRequest, BadGateway
from ..helpers import meta, isvalidEmail
from ..models import User


"""
curl -X POST http://localhost:8080/user/create \
-H 'content-type: application/json' \
-d '{
  "email": "john.doe@gmail.com",
  "first_name": "John",
  "last_name": "Doe"
}'
"""
@api.route('user/create', methods=['POST'])
def user_create_api():

    try:
        request_body = request.get_json()

    except BadRequest as e:
        return jsonify({'meta': meta(e.code, e.description)}), e.code

    except Exception as e:
        logging.info('Untreated exception: {}'.format(type(e)))
        logging.info('Status code: {}, Message: {}'.format(e.code, e.description))
        return jsonify({'meta': meta(e.code, e.description)}), e.code

    else:
        if not 'email' in request_body.keys() or not isvalidEmail(request_body["email"]):
            return jsonify({'meta': meta(400, "Missing or unexpected email value")}), 400

        if not 'first_name' in request_body.keys() or not 'last_name' in request_body.keys():
            return jsonify({'meta': meta(400, "Missing or unexpected first_name or last_name value")}), 400

        new_user = User.get_by_id(str(request_body['email'].lower()))

        if new_user is not None:
            return jsonify({'meta': meta(409, "User already exists")}), 409

        new_user = User(id=str(request_body["email"]).lower())
        new_user.first_name = str(request_body["first_name"]).capitalize()
        new_user.last_name = str(request_body["last_name"]).capitalize()

        email = new_user.put()
        
        response = {
            'content': new_user.content(),
            'meta': meta(200, HTTP_STATUS_CODES.get(200)),
        }

        return jsonify(response), 200
