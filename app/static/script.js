let settings = {
    "START_MODE": "console",

    "LOG_TO_FILE": false,
    "LOG_TO_CONSOLE": true,
    "SIMPLIFIED_DEBUG": false,
    "LOGGING_LEVEL_DEBUG": false,

    "AUTO_START": false,
    "MULTIPLE_MODE": false,
    "SIMPLIFIED_ALGORITHMS_MODE": true
}

const DEBUG = true

function set_listener(identifier, proprty) {
    try {
        document.getElementById(identifier).onchange = function() {
            proprty == true ? proprty = false : proprty = true;
            console.log(`${identifier} ${proprty}`);
        }
    } catch (e) {
        if (DEBUG) {
            console.log("Ошибка: " + e);
        }
    }
}

function postData(url = '', data = {}) {
    // let t = JSON.stringify(data)
    try {
        let send = JSON.stringify(data)
        console.log(send)
        fetch(url, {
            method: 'POST',
            body: send,
            headers: {
                'Content-Type': 'application/json'
            }
        });
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

//=================================//
// описание лисенеров для настроек //
//=================================//

if (document.title == 'Контроль бота') {
    // control.html
    set_listener('log_to_file', settings.LOG_TO_FILE)
    set_listener('easy_debug', settings.SIMPLIFIED_DEBUG)
    set_listener('log_to_console', settings.LOG_TO_CONSOLE)
    set_listener('log_level_debug', settings.LOGGING_LEVEL_DEBUG)
} else if (document.title == 'Настройки') {
    // settings.html
    set_listener('multiple_mode', settings.MULTIPLE_MODE)
    set_listener('autoreload_mode', settings.AUTO_START)
    set_listener('easy_mode', settings.SIMPLIFIED_ALGORITHMS_MODE)
}

//==================================//
// описание post запросов к серверу //
//==================================//

document.getElementById('panel__start').onclick = function() {
    postData(document.baseURI + 'settings', {
        'action': 'start',
        'config': settings
    })
}
document.getElementById('panel__stop').onclick = function() {
    postData(document.baseURI + 'settings', {
        'action': 'stop',
        'config': settings
    })
}