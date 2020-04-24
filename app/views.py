import os
from json import load

from flask import render_template, request, url_for

from app import app
from app.client.control import CtrlWrapper, Settings


with open('/app/client/settings.json', 'r') as json:
    default_settings = load(json)
ctrl = CtrlWrapper(default_settings)


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
        action = request.get_json()['action']
        settings = request.get_json()['config']
        if action == 'start':
            if ctrl.running_bots_count == 0:
                ctrl = CtrlWrapper(Settings(settings))
                ctrl.start()
        elif action == 'stop':
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
