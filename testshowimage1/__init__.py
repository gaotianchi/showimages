from datetime import timedelta
import datetime
import os

from flask import Flask
from dotenv import load_dotenv

load_dotenv()
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask('testshowimage1')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['FLASK_APP'] = os.getenv('FLASK_APP')
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=3)


if not os.path.exists(os.path.join(PROJECT_PATH, 'data1')):
    os.makedirs(os.path.join(PROJECT_PATH, 'data1'))

    config_path = os.path.join(os.path.join(PROJECT_PATH, 'data1'), 'config.json')
    if not os.path.exists(config_path):
        config_file = open(config_path, 'w')
        config_file.close()


app.config['USER_DATA_PATH'] = PROJECT_PATH + '\\data1'


from testshowimage1 import views