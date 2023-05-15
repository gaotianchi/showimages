"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

import os

from flask import Flask

from showimages.settings import Config

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app():

    app = Flask("showimage")
    app.config.from_object(Config)

    return app
