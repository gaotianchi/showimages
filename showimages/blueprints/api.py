"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

import os

from flask import Blueprint


api_bp = Blueprint("api", __name__)


@api_bp.before_request
def update_session():
    now = datetime.datetime.now()
    user_id = session.get("USER_ID", "")
    session['EXPIRATION_TIME'] = now + current_app.config["PERMANENT_SESSION_LIFETIME"]
    
    if not user_id:
        user_id = generate_user_id(request)
        session['USER_ID'] = user_id
        init_user(user_id, current_app)

    RedisHandler.set_expiration_time(user_id, session['EXPIRATION_TIME'])


@api_bp.route('/upload', methods=['GET', 'POST'])
def upload_image():
    """上传图片"""
    form = UploadForm()
    if form.validate_on_submit():
        upload_path = get_user_path(session["USER_ID"])["user_upload_path"]

        for file in request.files.getlist("photo"):
            image_name = secure_filename(file.filename)
            photos.save(file, os.path.join(upload_path, image_name))
        success = True
    else:
        success = False

    return "OK" if success else "FAIL"