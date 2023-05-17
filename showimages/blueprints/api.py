"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

import datetime
import os

from flask import Blueprint, redirect, request, current_app, session, url_for

from showimages.forms import UploadForm
from showimages.models import RedisHandler, ImageProcessor, ModelErrorHandler
from showimages.utils import generate_user_id, get_user_path, init_user


api_bp = Blueprint("api", __name__)
redishandler = RedisHandler()


@api_bp.before_request
def update_session():
        
    now = datetime.datetime.now().astimezone(datetime.timezone.utc)
    user_id = session.get("USER_ID", "")
    session['EXPIRATION_TIME'] = now + current_app.config["PERMANENT_SESSION_LIFETIME"]
    
    if not user_id:
        user_id = generate_user_id(request)
        session['USER_ID'] = user_id
        init_user(user_id, current_app)
    
    expiration_time = str(session.get("EXPIRATION_TIME"))

    redishandler.set_expiration_time(user_id, expiration_time)


@api_bp.route('/upload', methods=['GET', 'POST'])
def upload_image():
    """上传图片"""
    form = UploadForm()
    if form.validate_on_submit():
        upload_path = get_user_path(session["USER_ID"], current_app)["user_upload_path"]

        for file in request.files.getlist("photo"):
            image_name = file.filename
            file.save(os.path.join(upload_path, image_name))
        success = True
    else:
        success = False

    return redirect(url_for("api.process_image"))


@api_bp.route("/process")
def process_image():
    user_id = session.get("USER_ID")
    upload_path = get_user_path(user_id, current_app)["user_upload_path"]
    result_path = get_user_path(user_id, current_app)["user_result_path"]
    handler = ImageProcessor(upload_path, result_path)
    handler.process()
    result = dict(num=handler.error_handler.error_num, items=handler.error_handler.error_items)
    
    return "OK" if result["num"] == 0 else result