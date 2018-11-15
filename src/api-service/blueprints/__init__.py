import logging
from flask import Flask


def create_app(config):

    logging.info("STARTUP: Getting ready to launch")

    api = Flask(__name__)
    api.config.update(config)

    from .api import api as api_blueprint
    api.register_blueprint(api_blueprint, url_prefix='/')

    logging.info("STARTUP: Ready to rock!!!")

    return api