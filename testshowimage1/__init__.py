from datetime import timedelta
import os

from flask import Flask
from dotenv import load_dotenv

load_dotenv()
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask('testshowimage1')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['FLASK_APP'] = os.getenv('FLASK_APP')

if not os.path.exists(os.path.join(PROJECT_PATH, 'data1')):
    os.makedirs(os.path.join(PROJECT_PATH, 'data1'))

app.config['USER_DATA_PATH'] = PROJECT_PATH + '\\data1'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

from testshowimage1 import views