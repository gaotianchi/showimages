"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

import datetime
import math
import os

from flask import Blueprint, redirect, request, current_app, session, url_for, send_from_directory, jsonify

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


@api_bp.route("/page-urls")
def get_page_urls():
    per_page = current_app.config["IMAGE_PER_PAGE"]
    current_page = request.args.get("page", 1, int)
    user_id = session.get("USER_ID", "")
    result_path = get_user_path(user_id, current_app)["user_result_path"]
    image_names = os.listdir(result_path)
    start = (current_page - 1) * per_page
    end = start + per_page
    page_images = image_names[start:end]
    num_pages = math.ceil(len(image_names) / per_page)

    page_urls = []
    for image in page_images:
        image_url = url_for("api.send_image_from_dir", filename=image)
        page_urls.append(image_url)

    return jsonify(num_pages=num_pages, page_urls=page_urls)


@api_bp.route("/image-url/<filename>")
def send_image_from_dir(filename):
    user_id = session.get("USER_ID", "")
    result_path = get_user_path(user_id, current_app)["user_result_path"]

    return send_from_directory(result_path, filename)


@api_bp.route("/image-report/<imagename>")
def get_image_report(imagename: str):
    image_hash = imagename.split(".")[0]
    report = redishandler.get_report(image_hash)
    report = {key.decode(): value.decode() for key, value in report.items()}
    result = {f"{image_hash}": report}


    return jsonify(result)
    