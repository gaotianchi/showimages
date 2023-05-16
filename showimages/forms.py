"""
    :author: 高天驰
    :copyright: © 2023 高天驰 <6159984@gmail.com>
"""

from flask_wtf import FlaskForm
from wtforms import MultipleFileField, SubmitField
from wtforms.validators import DataRequired



class UploadForm(FlaskForm):
    photo = MultipleFileField('Upload Image', validators=[DataRequired()])
    submit = SubmitField()