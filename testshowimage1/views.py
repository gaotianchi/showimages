import datetime
import os
import math

from flask import render_template, redirect, url_for, send_from_directory, jsonify, request, session

from testshowimage1 import app
from testshowimage1.forms import MultiUploadForm
from testshowimage1.models import ImageProcesser
from testshowimage1.utils import generate_user_id, get_user_data_path, make_session


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)


@app.before_request
def destroy_session():
    with app.app_context():
        now = datetime.datetime.now().astimezone(datetime.timezone.utc)
        expiration_time = session.get('expiration_time')
        if not expiration_time or expiration_time < now:
            session.clear()

    return None
    

@app.route('/')
def index():
    form = MultiUploadForm()
    
    return render_template('t1.html', form=form)


@app.route('/upload', methods=['POST'])
def upload():
    user_id = session.get('USER_ID', '')
    if not user_id:
        user_id = generate_user_id(request)
        now = datetime.datetime.now()
        make_session(user_id, now, session, app)
    
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