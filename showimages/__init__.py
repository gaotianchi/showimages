"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

import os
import threading

from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask, render_template
from flask_wtf.csrf import CSRFError

from showimages.settings import Config
from showimages.blueprints import interface_bp, api_bp
from showimages.models import RedisHandler
from showimages.extensions import csrf
from showimages.utils import destroy_user_data

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app():

    app = Flask("showimages")
    app.config.from_object(Config)

    register_blueprints(app)
    register_extensions(app)
    register_errorhandlers(app)

    def start_scheduler(scheduler: BlockingScheduler):
        scheduler.start()

    redishandler = RedisHandler()
    scheduler = BlockingScheduler()
    scheduler.add_job(destroy_user_data, 'interval', seconds=10800, args=[app, redishandler])
    scheduler_thread = threading.Thread(target=start_scheduler, args=[scheduler])
    scheduler_thread.start()

    return app


def register_blueprints(app: Flask):
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(interface_bp)


def register_extensions(app: Flask):
    csrf.init_app(app)


def register_errorhandlers(app: Flask):

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 500
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500