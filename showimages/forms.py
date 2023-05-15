"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField



class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(), FileRequired()])
    submit = SubmitField("上传")