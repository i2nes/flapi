import logging
from flask import Flask


def create_app(config):

    logging.info("STARTUP: Getting ready to launch")

    app = Flask(__name__)
    app.config.update(config)

    # Register Blueprints
    from .webApp import app as webApp_blueprint
    app.register_blueprint(webApp_blueprint, url_prefix='/')

    logging.info("STARTUP: Ready to rock!!!")

    return app