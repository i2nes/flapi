import logging
from . import api
from flask import Flask, jsonify, request
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError, Conflict
from ..helpers import meta, isvalidEmail, handle_http_error
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
            return handle_http_error(NotFound)
            
    else: # Invalid email
        return handle_http_error(NotFound)

    return handle_http_error(InternalServerError)


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
            return handle_http_error(NotFound)
            
    else: # Invalid email
        return handle_http_error(NotFound)

    return handle_http_error(InternalServerError)


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
            return handle_http_error(NotFound)

        try:
            request_body = request.get_json()

        except BadRequest as e:
            return handle_http_error(e)

        except Exception as e:
            logging.info('Untreated exception: {}'.format(type(e)))
            logging.info('Status code: {}, Message: {}'.format(e.code, e.description))
            return handle_http_error(e)

        else:

            if request_body is None:
                return handle_http_error(BadRequest)

            logging.info(request_body)
            if not 'first_name' in request_body.keys() or not 'last_name' in request_body.keys():
                return handle_http_error(BadRequest)

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
        return handle_http_error(NotFound)

    return handle_http_error(InternalServerError)


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
        return handle_http_error(e)

    except Exception as e:
        logging.info('Untreated exception: {}'.format(type(e)))
        logging.info('Status code: {}, Message: {}'.format(e.code, e.description))
        return handle_http_error(e)

    else:
        if not 'email' in request_body.keys() or not isvalidEmail(request_body["email"]):
            return handle_http_error(BadRequest)

        if not 'first_name' in request_body.keys() or not 'last_name' in request_body.keys():
            return handle_http_error(BadRequest)

        new_user = User.get_by_id(str(request_body['email'].lower()))

        if new_user is not None:
            return handle_http_error(Conflict)

        new_user = User(id=str(request_body["email"]).lower())
        new_user.first_name = str(request_body["first_name"]).capitalize()
        new_user.last_name = str(request_body["last_name"]).capitalize()

        email = new_user.put()
        
        response = {
            'content': new_user.content(),
            'meta': meta(202, HTTP_STATUS_CODES.get(202)),
        }

        return jsonify(response), 202
