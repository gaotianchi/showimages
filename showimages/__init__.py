"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

import os

from flask import Flask

from showimages.settings import Config
from showimages.blueprints import interface_bp, api_bp

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app():

    app = Flask("showimages")
    app.config.from_object(Config)

    register_blueprints(app)

    return app


def register_blueprints(app: Flask):
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(interface_bp)