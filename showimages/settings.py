"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

import datetime
import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "default")

    PERMANENT_SESSION_LIFETIME = datetime.timedelta(hours=24)

    USER_DATA_PATH = os.path.join(basedir, "userdata")
    
    # ALLOWED_IMAGE_EXTENSIONS = ["png"]

    IMAGE_PER_PAGE = 9

    def __init__(self) -> None:
        if not os.path.exists(self.USER_DATA_PATH):
            os.makedirs(self.USER_DATA_PATH)