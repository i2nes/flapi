import logging
from . import api
from flask import Flask, jsonify, request
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import BadRequest
from ..helpers import meta, isvalidEmail
from ..models import User


"""
curl -X GET http://localhost:8080/user/list
"""
@api.route('user/list', methods=['GET'])
def user_list_api():

    users_ndb = User().query().fetch()
    user_list = [user.list_content() for user in users_ndb]
    
    response = {
        'content': user_list,
        'meta': meta(200, HTTP_STATUS_CODES.get(200)),
    }

    return jsonify(response), 200


"""
curl -X GET http://localhost:8080/user/john.doe@gmail.com/info
"""
@api.route('user/<user_id>/info', methods=['GET'])
def user_info_api(user_id):

    if isvalidEmail(user_id):

        user = User.get_by_id(user_id.lower())

        if user:
            response = {
                'content': user.content(),
                'meta': meta(200, HTTP_STATUS_CODES.get(200)),
            }
            return jsonify(response), 200

        else: # user doesn't exist
            return jsonify(meta(404, HTTP_STATUS_CODES.get(404))), 404
            
    else: # Invalid email
        return jsonify(meta(404, HTTP_STATUS_CODES.get(404))), 404

    return jsonify(meta(500, HTTP_STATUS_CODES.get(500))), 500


"""
curl -X DELETE http://localhost:8080/user/john.doe@gmail.com/delete
"""
@api.route('user/<user_id>/delete', methods=['DELETE'])
def user_delete_api(user_id):

    if isvalidEmail(user_id):

        user = User.get_by_id(user_id.lower())

        if user:
            user.key.delete()
            response = {
                'meta': meta(202, HTTP_STATUS_CODES.get(202)),
            }
            return jsonify(response), 202

        else: # user doesn't exist
            return jsonify(meta(404, HTTP_STATUS_CODES.get(404))), 404
            
    else: # Invalid email
        return jsonify(meta(404, HTTP_STATUS_CODES.get(404))), 404

    return jsonify(meta(500, HTTP_STATUS_CODES.get(500))), 500


"""
curl -X POST http://localhost:8080/user/john.doe@gmail.com/update \
-H 'content-type: application/json' \
-d '{
  "first_name": "Johnny",
  "last_name": "Fingers"
}'
"""
@api.route('user/<user_id>/update', methods=['POST'])
def user_update_api(user_id):

    if isvalidEmail(user_id):

        user = User.get_by_id(user_id.lower())

        if user is None:
            return jsonify(meta(404, HTTP_STATUS_CODES.get(404))), 404

        try:
            request_body = request.get_json()

        except BadRequest as e:
            return jsonify({'meta': meta(e.code, e.description)}), e.code

        except Exception as e:
            logging.info('Untreated exception: {}'.format(type(e)))
            logging.info('Status code: {}, Message: {}'.format(e.code, e.description))
            return jsonify({'meta': meta(e.code, e.description)}), e.code

        else:

            if request_body is None:
                return jsonify({'meta': meta(400, "Bad request. Expecting content-type: application/json")}), 400

            logging.info(request_body)
            if not 'first_name' in request_body.keys() or not 'last_name' in request_body.keys():
                return jsonify({'meta': meta(400, "Missing or unexpected first_name or last_name value")}), 400

            if 'first_name' in request_body.keys():
                user.first_name = str(request_body['first_name']).capitalize()

            if 'last_name' in request_body.keys():
                user.last_name = str(request_body['last_name']).capitalize()

            user.put()
            
            response = {
                'content': user.content(),
                'meta': meta(202, HTTP_STATUS_CODES.get(202)),
            }

            return jsonify(response), 202
            
    else: # Invalid email
        return jsonify(meta(404, HTTP_STATUS_CODES.get(404))), 404

    return jsonify(meta(500, HTTP_STATUS_CODES.get(500))), 500


"""
curl -X POST http://localhost:8080/user/create \
-H 'content-type: application/json' \
-d '{
  "email": "john.doe12@gmail.com",
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
            'meta': meta(202, HTTP_STATUS_CODES.get(202)),
        }

        return jsonify(response), 202
