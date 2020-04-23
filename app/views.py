import os

from flask import render_template, request, url_for

from app import app
from app.client.control import CtrlWrapper

ctrl = CtrlWrapper(CtrlWrapper.load_from_json('./app/client/settings.json'))


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=12'
    return response


@app.route('/')
@app.route('/control')
def control():
    return render_template('control.html')


@app.route('/settings', methods=['POST', 'GET'])
def settings():
    global ctrl
    if request.method == 'POST':
        content = request.get_json()
        # print(content)
        if content['action'] == 'start':
            # print(ctrl.running_bots_count)
            if ctrl.running_bots_count == 0:
                ctrl = CtrlWrapper(content['config'])
                ctrl.start()
            
        elif content['action'] == 'stop':
            ctrl.stop_all_bots()
    return render_template('settings.html')


@app.errorhandler(404)
def page_not_found(e):
    return '404'


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
