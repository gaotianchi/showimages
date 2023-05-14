import datetime
import json
import math
import os
import time

from flask import Flask, Request
from hashlib import sha256


def generate_user_id(request: Request):
    user_agent = request.headers.get('User-Agent', '')
    screen_width = request.args.get('width', '')
    screen_height = request.args.get('height', '')
    t = str(time.time())
    user_id = sha256((user_agent+screen_height+screen_width+t).encode('utf-8')).hexdigest()
    
    return user_id


def get_user_data_path(user_id: str, app: Flask):
    user_data_path = os.path.join(app.config['USER_DATA_PATH'], user_id)
    upload_path = os.path.join(user_data_path, 'uploads')
    result_image_path = os.path.join(user_data_path, 'result-images')
    result_report_path = os.path.join(user_data_path, 'result-reports')
    ok_image_path = os.path.join(result_image_path, 'ok')
    error_image_path = os.path.join(result_image_path, 'error')
    ok_report_path = os.path.join(result_report_path, 'ok')
    error_report_path = os.path.join(result_report_path, 'error')


    if not os.path.exists(user_data_path):
        for i in (user_data_path, upload_path, result_image_path, result_report_path):
            os.makedirs(i)
        
        for j in (ok_image_path, error_image_path, ok_report_path, error_report_path):
            os.makedirs(j)

    return (user_data_path, upload_path, result_image_path, result_report_path)


def make_session(user_id, now_time, session, app: Flask):
    session['EXPIRATION_TIME'] = now_time + app.config['PERMANENT_SESSION_LIFETIME']
    session['USER_ID'] = user_id

    try:
        with open(app.config["USER_CONFIG"], "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data = data.copy()
    data[user_id] = session['EXPIRATION_TIME']

    with open(app.config["USER_CONFIG"], "w") as f:
        json.dump(data, f, indent=4, cls=DatetimeEncoder)


def destory_user_data(session, app: Flask):
    if session.get('USER_ID', ''):
        user_id = session['USER_ID']
        user_data_path = get_user_data_path(user_id, app)[0]
        os.rmdir(user_data_path)


def file_paths_in_dir(dir_path):
    file_names = os.listdir(dir_path)
    result = []
    for i in file_names:
        file_path = os.path.join(dir_path, i)
        result.append(file_path)
    return result


def paging(image_names, page=1, per_page=3):
    num_pages = math.ceil(len(image_names) / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    page_images = image_names[start:end]
    hashs = []
    for image in page_images:
        hash = image.split('.')[0]
        hashs.append(hash)
    
    return hashs, num_pages


def read_config(app: Flask):
    try:
        with open(app.config["USER_CONFIG"], "r") as f:
            data = json.load(f)
    except:
        return {}
    else:
        return data


def update_config(session, app: Flask):
    user_id = session["USER_ID"]
    expiration_time = session["EXPIRATION_TIME"]

    try:
        with open(app.config["USER_CONFIG"], "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data = data.copy()
    data[user_id] = expiration_time

    with open(app.config["USER_CONFIG"], "w") as f:
        json.dump(data, f, indent=4, cls=DatetimeEncoder)


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)