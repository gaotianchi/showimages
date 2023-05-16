"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

import os

from flask import Blueprint, render_template, current_app

from showimages.forms import UploadForm


interface_bp = Blueprint("interface", __name__, template_folder="templates")


@interface_bp.route("/")
def index():

    form = UploadForm()
    return render_template("index.html", form=form)