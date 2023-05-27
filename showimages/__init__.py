"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

import logging
from logging.handlers import RotatingFileHandler
import os
import threading

from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFError

from showimages.settings import Config
from showimages.blueprints import interface_bp, api_bp
from showimages.models import redis_handler
from showimages.extensions import csrf
from showimages.utils import destroy_user_data, destroy_temp_data

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app():

    app = Flask("showimages")
    app.config.from_object(Config)

    register_blueprints(app)
    register_extensions(app)
    register_errorhandlers(app)
    register_scheduler(app)
    register_logging(app)

    return app


def register_scheduler(app: Flask):

    def start_scheduler(scheduler: BlockingScheduler):
        scheduler.start()

    scheduler = BlockingScheduler()
    scheduler.add_job(destroy_user_data, 'interval', seconds=10, args=[app, redis_handler])
    scheduler.add_job(destroy_temp_data, 'interval', seconds=10, args=[app])
    scheduler_thread = threading.Thread(target=start_scheduler, args=[scheduler])
    scheduler_thread.start()


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
    

def register_logging(app: Flask):
    log_file_path = os.path.join(basedir, "log/showimages.log")
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(log_file_path, maxBytes=10 * 1024 * 1024, backupCount=10, encoding='utf-8')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)