"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

import datetime
import hashlib
import math
import os
import pathlib
import shutil
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


def creat_dir_zip(image_dir: str, name_map: dict, result_zip_path: str, report: str):
    directory = pathlib.Path(image_dir)
    with zipfile.ZipFile(result_zip_path, mode="w") as archive:
        for file_path in directory.iterdir():
            arcname = "images/" + name_map[file_path.name.split(".")[0]]
            archive.write(file_path, arcname=arcname)

        archive.writestr(zinfo_or_arcname="reports.json", data=report)
        

def destroy_user_data(app: Flask, redishandler):
    user_ids = os.listdir(app.config["USER_DATA_PATH"])
    for user in user_ids:
        expiration_time: str = redishandler.get_user_expiration_time(user).decode()
        expiration_time_datatime = datetime.datetime.fromisoformat(expiration_time)
        now = datetime.datetime.now().astimezone(datetime.timezone.utc)

        if expiration_time_datatime < now:
            user_data_path = os.path.join(app.config["USER_DATA_PATH"], user)
            shutil.rmtree(user_data_path)
            app.logger.info(f"成功删除用户 {user} 的个人数据！")
        else:
            app.logger.info(f"用户 {user} session 有效。")
        

def destroy_temp_data(app: Flask):
    temp_path = app.config["TEMP_DIR"]
    temp_items = os.listdir(temp_path)
    for temp_item in temp_items:
        item_path = os.path.join(temp_path, temp_item)
        os.remove(item_path)
        app.logger.info(f"成功移除 {temp_item}")