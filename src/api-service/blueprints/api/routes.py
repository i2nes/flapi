import logging
from . import api
from flask import Flask, jsonify
from werkzeug.http import HTTP_STATUS_CODES


@api.route('hello', methods=['GET'])
def hello_api():

    hello = {
        'content': {
            'text': 'hello world',
        },
        'meta': {
            'httpCode': 200,
            'httpText': HTTP_STATUS_CODES.get(200),
        }        
    }

    return jsonify(hello), 200
