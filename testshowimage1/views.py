from datetime import datetime, timedelta
import os
import math

from flask import render_template, redirect, url_for, send_from_directory, jsonify, request, session

from testshowimage1 import app
from testshowimage1.forms import MultiUploadForm
from testshowimage1.models import ImageProcesser
from testshowimage1.utils import generate_user_id, get_user_data_path


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


@app.before_request
def destroy_session():
    with app.app_context():
        now = datetime.now()
        for key in list(session.keys()):
            val = session.get(key)
            if isinstance(val, dict) and val.get('expiration_time', datetime.max) < now:
                session.pop(key)
    

@app.route('/')
def index():
    form = MultiUploadForm()
    
    return render_template('t1.html', form=form)


@app.route('/upload', methods=['POST'])
def upload():
    user_id = session.get('USER_ID', '')
    if not user_id:
        user_id = generate_user_id(request)
        session['USER_ID'] = user_id
    
    upload_path = get_user_data_path(user_id, app)[1]

    for f in request.files.getlist('photo'):
        image_name = f.filename
        f.save(os.path.join(upload_path, image_name))
    
    return redirect(url_for('process'))
    

@app.route('/process')
def process():
    user_id = session.get('USER_ID', '')
    if user_id:
        upload_path, result_image_path, result_report_path = get_user_data_path(user_id, app)[1:4]
        handler = ImageProcesser(upload_path, result_image_path, result_report_path)
        handler.process()

    return redirect(url_for('index'))


@app.route('/clear-session')
def clear_session():
    session.clear()
    return 'ok'