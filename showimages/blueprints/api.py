"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

import datetime
import os
import shutil

from flask import Blueprint, redirect, request, current_app, session, url_for, \
send_from_directory, jsonify, flash

from showimages.forms import UploadForm
from showimages.models import RedisHandler, ImageProcessor
from showimages.utils import generate_user_id, get_feature_images, get_user_path, init_user, paging


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
            redishandler.add_uploading(session.get("USER_ID"), image_name)
        success = True
    else:
        success = False

    return redirect(url_for("api.process_image"))


@api_bp.route("/get-report/<filename>")
def get_report(filename: str):
    image_id = filename.split(".")[0]
    image_report = redishandler.get_report(image_id)

    return jsonify(image_report)



@api_bp.route("/process")
def process_image():
    user_id = session.get("USER_ID")
    upload_path = get_user_path(user_id, current_app)["user_upload_path"]
    result_path = get_user_path(user_id, current_app)["user_result_path"]
    handler = ImageProcessor(upload_path, result_path, user_id)
    handler.process()
    fail_items = handler.redis_handler.get_fails(user_id)
    if fail_items:
        for fail_item in fail_items:
            flash(f"处理失败：{fail_item}")
    else:
        flash("处理成功！")
    
    return redirect(url_for("interface.result"))


@api_bp.route("/page-urls")
@api_bp.route("/page-urls/<feature>")
def get_page_urls(feature="All"):
    per_page = current_app.config["IMAGE_PER_PAGE"]
    current_page = request.args.get("page", 1, int)
    user_id = session.get("USER_ID", "")
    image_names = get_feature_images(user_id, feature, current_app, redishander=redishandler)

    page_images, num_pages = paging(image_names, current_page, per_page)

    image_items = []
    for image in page_images:
        image_hash = image.split(".")[0]
        image_report = redishandler.get_report(image_hash)
        image_url = url_for("api.send_image_from_dir", filename=image)
        image_item = dict(image_url=image_url, image_report=image_report)
        image_items.append(image_item)

    return jsonify(num_pages=num_pages, image_items=image_items)


@api_bp.route("/image-url/<filename>")
def send_image_from_dir(filename):
    user_id = session.get("USER_ID", "")
    result_path = get_user_path(user_id, current_app)["user_result_path"]

    return send_from_directory(result_path, filename)


@api_bp.route("/processed-images")
def get_processed_images():
    user_id = session.get("USER_ID")
    result_path = get_user_path(user_id, current_app)["user_result_path"]
    images = os.listdir(result_path)
    image_urls = []
    for image in images:
        image_url = url_for("api.send_image_from_dir", filename=image)
        image_urls.append(image_url)

    return jsonify(image_urls)


@api_bp.route("/delete-this-one/<image_name>", methods=['GET', 'POST'])
def delete_this_one(image_name: str):
    user_id = session.get("USER_ID")
    result_path = get_user_path(user_id, current_app)["user_result_path"]
    upload_path = get_user_path(user_id, current_app)["user_upload_path"]
    image_id = image_name.split(".")[0]
    report = redishandler.get_report(image_id)
    upload_image_path = os.path.join(upload_path, report["original_name"])
    result_image_path = os.path.join(result_path, image_name)
    os.remove(upload_image_path)
    os.remove(result_image_path)
    
    redishandler.delete_report(image_id)
    
    return "ok"


@api_bp.route("/delete-all", methods=['GET', 'POST'])
def delete_all():
    user_id = session.get("USER_ID")
    result_path = get_user_path(user_id, current_app)["user_result_path"]
    upload_path = get_user_path(user_id, current_app)["user_upload_path"]
    image_names: list[str] = os.listdir(result_path)
    for image_name in image_names:
        image_id = image_name.split(".")[0]
        redishandler.delete_report(image_id)

    for i in (result_path, upload_path):
        shutil.rmtree(i)
        os.makedirs(i)

    return "ok"