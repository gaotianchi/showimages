"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

import os


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "default")

    USER_DATA_PATH = os.path.join(basedir, "userdata")
    
    ALLOWED_IMAGE_EXTENSIONS = ["png"]

    IMAGE_PER_PAGE = 12