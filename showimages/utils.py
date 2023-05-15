"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

import datetime
import hashlib
import json
import os
import time

from flask import Request, Flask
from flask.sessions import SessionMixin


def generate_user_id(request: Request):
    """根据用户浏览器生成用户id"""
    user_agent = request.headers.get('User-Agent', '')
    screen_width = request.args.get('width', '')
    screen_height = request.args.get('height', '')
    t = str(time.time())
    user_id = hashlib.sha256((user_agent+screen_height+screen_width+t).encode('utf-8')).hexdigest()
    
    return user_id


def update_user_session(app: Flask, session: SessionMixin, request: Request):
    """用户的每次请求都会更新session有效期"""

    class DatetimeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.isoformat()
            return json.JSONEncoder.default(self, obj)
        
    now = datetime.datetime.now()
    user_id = session.get("USER_ID", "")
    session['EXPIRATION_TIME'] = now + app.config["PERMANENT_SESSION_LIFETIME"]
    
    if not user_id:
        user_id = generate_user_id(request)
        session['USER_ID'] = user_id

    try:
        with open(app.config["USER_EXPIRATION_TIME_LOG"], "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data = data.copy()
    data[user_id] = session['EXPIRATION_TIME']

    with open(app.config["USER_EXPIRATION_TIME_LOG"], "w") as f:
        json.dump(data, f, indent=4, cls=DatetimeEncoder)
