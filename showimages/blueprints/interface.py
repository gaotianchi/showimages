"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""
import os
from urllib.parse import urljoin

import requests
from flask import Blueprint, render_template, url_for, request, session, flash, current_app, redirect

from showimages.forms import UploadForm
from showimages.utils import get_user_path


interface_bp = Blueprint("interface", __name__, template_folder="templates")


@interface_bp.route("/")
def index():

    form = UploadForm()
    user_id = session.get("USER_ID", "")
    if user_id:
        flash(f"欢迎！{user_id}")
    return render_template("index.html", form=form)


@interface_bp.route("/result")
def result():
    user_id = session.get("USER_ID")
    result_path = get_user_path(user_id, current_app)["user_result_path"]
    result_num = len(os.listdir(result_path))
    if result_num > 0:
        init_page_items_url = url_for("api.get_page_urls")
        cookies = request.cookies
        base_url = f"http://{request.server[0]}:{request.server[1]}"
        url = urljoin(base_url, init_page_items_url)
        items = requests.get(url, cookies=cookies).json()

        return render_template("result.html", items=items)
    
    else:

        return redirect(url_for("interface.index"))