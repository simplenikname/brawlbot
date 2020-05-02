let settings = {
    START_MODE: "console",

    LOG_TO_FILE: false,
    LOG_TO_CONSOLE: true,
    LOG_LEVEL_DEBUG: false,
    LOG_REQUESTS_TO_SERVER: true,

    MULTIPLE_MODE: false,
    INFINITY_MODE: false,
    SIMPLIFIED_ALGORITHMS_MODE: true
};

let keys = ['LOG_TO_FILE', 'LOG_TO_CONSOLE', 'LOG_LEVEL_DEBUG', 'LOG_REQUESTS_TO_SERVER', 'MULTIPLE_MODE', 'INFINITY_MODE', 'SIMPLIFIED_ALGORITHMS_MODE']


function postData(url = "", data = {}) {
    try {
        let send = JSON.stringify(data);
        console.log(send);
        fetch(url, {
            method: "POST",
            body: send,
            headers: {
                "Content-Type": "application/json",
            },
        });
    } catch (error) {
        console.error("Ошибка:", error);
    }
}

//=================================//
// описание лисенеров для настроек //
//=================================//

if (document.title === "Контроль бота") {

    // control.html

    let infinity = document.getElementById('infinity_mode').onchange = function() {
        settings.INFINITY_MODE == false ? (settings.INFINITY_MODE = true) : (settings.INFINITY_MODE = false)
        console.log(settings)
    }

    let log_to_file = document.getElementById('log_to_file').onchange = function() {
        settings.LOG_TO_FILE == false ? (settings.LOG_TO_FILE = true) : (settings.LOG_TO_FILE = false)
        console.log(settings)
    }

    let log_to_console = document.getElementById('log_to_console').onchange = function() {
        settings.LOG_TO_CONSOLE == true ? (settings.LOG_TO_CONSOLE = false) : (settings.LOG_TO_CONSOLE = true)
        console.log(settings)
    }

    let log_level_debug = document.getElementById('log_level_debug').onchange = function() {
        settings.LOG_LEVEL_DEBUG == false ? (settings.LOG_LEVEL_DEBUG = true) : (settings.LOG_LEVEL_DEBUG = false)
        console.log(settings)
    }

    let logrequests_to_server = document.getElementById('log_requests_to_server').onchange = function() {
        settings.LOG_REQUESTS_TO_SERVER == true ? (settings.LOG_REQUESTS_TO_SERVER = false) : (settings.LOG_REQUESTS_TO_SERVER = true)
        console.log(settings)
    }

} else if (document.title == "Настройки") {

    // settings.html

    let multiple_mode = document.getElementById('multiple_mode').onchange = function() {
        settings.MULTIPLE_MODE == false ? (settings.MULTIPLE_MODE = true) : (settings.MULTIPLE_MODE = false)
        console.log(settings)
    }

    let simplefield_mode = document.getElementById('simplified_mode').onchange = function() {
        settings.SIMPLIFIED_ALGORITHMS_MODE == true ? (settings.SIMPLIFIED_ALGORITHMS_MODE = false) : (settings.SIMPLIFIED_ALGORITHMS_MODE = true)
        console.log(settings)
    }

}

//==================================//
// описание post запросов к серверу //
//==================================//

document.getElementById("bot_start").onclick = function() {
    postData(document.baseURI + "settings", {
        action: "start",
        config: settings,
    });
};
document.getElementById("bot_stop").onclick = function() {
    postData(document.baseURI + "settings", {
        action: "stop",
        config: settings,
    });
};

const current_state = document.getElementById('bot__state').innerText

setInterval(async() => {
    const response = await fetch(document.baseURI + "state", {
        method: "POST",
    });

    const response_json = await response.json();

    console.log(current_state.toLowerCase(), response_json['state'])

    if (current_state.toLowerCase() !== response_json['state']) {
        location.href = location.href
    }

}, 1000)