import logging
from flask import Flask
from .helpers import handle_http_error


def create_app(config):

    logging.info("STARTUP: Getting ready to launch")

    api = Flask(__name__)
    api.config.update(config)

    # Register Error handlers
    api.register_error_handler(404, handle_http_error)

    # Register Blueprints
    from .api import api as api_blueprint
    api.register_blueprint(api_blueprint, url_prefix='/')

    logging.info("STARTUP: Ready to rock!!!")

    return api