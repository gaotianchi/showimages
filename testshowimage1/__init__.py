import threading
import datetime
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask
from dotenv import load_dotenv

from testshowimage1.utils import destory_user_data

load_dotenv()
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask('testshowimage1')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['FLASK_APP'] = os.getenv('FLASK_APP')
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(seconds=60)


if not os.path.exists(os.path.join(PROJECT_PATH, 'data1')):
    os.makedirs(os.path.join(PROJECT_PATH, 'data1'))

config_path = os.path.join(os.path.join(PROJECT_PATH, 'data1'), 'config.json')
if not os.path.exists(config_path):
    c = open(config_path, 'w')
    c.close()


app.config['USER_DATA_PATH'] = PROJECT_PATH + '\\data1'
app.config["USER_CONFIG"] = os.path.join(os.path.join(PROJECT_PATH, 'data1'), 'config.json')

def start_scheduler(scheduler: BlockingScheduler):
    scheduler.start()

scheduler = BlockingScheduler()
scheduler.add_job(destory_user_data, 'interval', seconds=3, args=[app])
scheduler_thread = threading.Thread(target=start_scheduler, args=[scheduler])
scheduler_thread.start()


from testshowimage1 import views