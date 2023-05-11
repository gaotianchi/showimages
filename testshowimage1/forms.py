from wtforms import MultipleFileField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class MultiUploadForm(FlaskForm):
    photo = MultipleFileField('Upload Image', validators=[DataRequired()])
    submit = SubmitField()