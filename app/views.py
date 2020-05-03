import os
from json import load

from flask import render_template, request, url_for, jsonify

from app import app
from app.client.control import CtrlWrapper, Settings

with open('./app/client/settings.json', 'r') as json:
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
    if ctrl.running_bot:
        bot_state = 'online'
    else:
        bot_state = 'offline'
    return render_template('control.html', state=bot_state)


@app.route('/settings', methods=['POST', 'GET'])
def settings():
    global ctrl
    if request.method == 'POST':
        action = request.get_json()['action']
        bot_settings = request.get_json()['config']
        if action == 'start':
            if ctrl.running_bot:
                configuration = Settings(
                    bot_settings.get('START_MODE') or default_settings.get('START_MODE'),
                    bot_settings.get('LOG_TO_FILE') or default_settings.get('LOG_TO_FILE'),
                    bot_settings.get('LOG_TO_CONSOLE') or default_settings.get('LOG_TO_CONSOLE'),
                    bot_settings.get('LOG_LEVEL_DEBUG') or default_settings.get('LOG_LEVEL_DEBUG'),
                    bot_settings.get('LOG_REQUESTS_TO_SERVER') or default_settings.get('LOG_REQUESTS_TO_SERVER'),
                    bot_settings.get('MULTIPLE_MODE') or default_settings.get('MULTIPLE_MODE'),
                    bot_settings.get('INFINITY_MODE') or default_settings.get('INFINITY_MODE'),
                    False,
                    bot_settings.get('SIMPLIFIED_ALGORITHMS_MODE') or
                    default_settings.get('SIMPLIFIED_ALGORITHMS_MODE'),
                )
                ctrl = CtrlWrapper(configuration)
                ctrl.start()
        elif action == 'stop':
            ctrl.stop_bot()
    return render_template('settings.html')


@app.route('/state', methods=['POST'])
def state():
    global ctrl
    if ctrl.running_bot:
        bot_state = {'state': 'online'}
    else:
        bot_state = {'state': 'offline'}
    return jsonify(bot_state), 200


@app.errorhandler(404)
def page_not_found(error):
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
