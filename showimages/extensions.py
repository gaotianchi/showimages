"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

from flask import Flask
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class


photos = UploadSet('photos', IMAGES)

def init_flask_uploads(app: Flask):
    configure_uploads(app, photos)
    patch_request_class(app) 