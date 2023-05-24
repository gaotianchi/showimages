"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

import hashlib
import math
import os
import time
import zipfile

from flask import Request, Flask


def generate_user_id(request: Request):
    """根据用户浏览器生成用户id"""
    user_agent = request.headers.get('User-Agent', '')
    screen_width = request.args.get('width', '')
    screen_height = request.args.get('height', '')
    t = str(time.time())
    user_id = hashlib.sha256((user_agent+screen_height+screen_width+t).encode('utf-8')).hexdigest()
    
    return user_id


def init_user(user_id: str, app: Flask):
    """初始化用户的文件夹结构"""
    user_data_path = os.path.join(app.config["USER_DATA_PATH"], user_id)
    user_upload_path = os.path.join(user_data_path, "uploads")
    user_result_path = os.path.join(user_data_path, "results")

    for i in (user_data_path, user_upload_path, user_result_path):
        os.makedirs(i)


def get_user_path(user_id: str, app: Flask) -> dict:
    """获取用户得文件路径"""

    user_data_path = os.path.join(app.config["USER_DATA_PATH"], user_id)
    user_upload_path = os.path.join(user_data_path, "uploads")
    user_result_path = os.path.join(user_data_path, "results")

    return dict(user_data_path=user_data_path, user_upload_path=user_upload_path, user_result_path=user_result_path)


def paging(image_names, page=1, per_page=9):
    num_pages = math.ceil(len(image_names) / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    page_images = image_names[start:end]
    
    return page_images, num_pages


def get_feature_images(user_id, feature, app, redishander):
    user_result_path = get_user_path(user_id, app)["user_result_path"]
    total_images = os.listdir(user_result_path)
    if feature == "All":
        return total_images
    feature_images = []
    for image_name in total_images:
        report = redishander.get_report(image_name.split(".")[0])
        if int(report[feature]) == 1:
            feature_images.append(image_name)

    return feature_images


def create_this_zip(file_data_dict: dict, result_zip_path: str):
    with zipfile.ZipFile(result_zip_path, mode="w") as archive:
        for file_name in file_data_dict.keys():
            archive.writestr(zinfo_or_arcname=file_name, data=file_data_dict[file_name])