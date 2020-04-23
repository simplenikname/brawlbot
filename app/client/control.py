
from datetime import datetime
from json import load
from time import sleep

from colorama import Fore, init
# from prompt_toolkit import prompt
# from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.shortcuts import ProgressBar, button_dialog

from app.client.brawlbot import Bot

def get_time():
    return datetime.strftime(datetime.now(), "%H:%M:%S")

class CtrlWrapper:
    def __init__(self, config_dictionary):
        self.running_bots_count = 0
        self.running_bots = []
        self.config_dictionary = config_dictionary
        self.START_MODE = config_dictionary.get('START_MODE') or 'console'

        if config_dictionary:
            # Испрользование переданного словаря для настройки

            # Настройки вывода и отладки
            self.LOG_TO_FILE = config_dictionary.get('LOG_TO_FILE') or False
            self.LOG_TO_CONSOLE = config_dictionary.get(
                'LOG_TO_CONSOLE') or True
            self.SIMPLIFIED_DEBUG = config_dictionary.get(
                'SIMPLIFIED_DEBUG') or False
            self.LOGGING_LEVEL_DEBUG = config_dictionary.get(
                'LOGGING_LEVEL_DEBUG') or False

            # Настройки бота
            self.AUTO_START = config_dictionary.get('AUTO_START') or False
            self.MULTIPLE_MODE = config_dictionary.get(
                'MULTIPLE_MODE') or False
            self.SIMPLIFIED_ALGORITHMS_MODE = config_dictionary.get(
                'SIMPLIFIED_ALGORITHMS_MODE') or True

        else:
            # Применение настроек по умолчанию

            # Настройки вывода и отладки
            self.LOG_TO_FILE = False
            self.LOG_TO_CONSOLE = True
            self.SIMPLIFIED_DEBUG = False
            self.LOGGING_LEVEL_DEBUG = False

            # Настройки бота
            self.AUTO_START = False
            self.MULTIPLE_MODE = False
            self.SIMPLIFIED_ALGORITHMS_MODE = True

    @staticmethod 
    def load_from_json(json_file):
        with open(json_file, 'r') as fp:
            settings_dict = load(fp)
            return settings_dict

    def __start_bot(self):
        brawlbot = Bot(self.MULTIPLE_MODE, self.LOGGING_LEVEL_DEBUG, self, infinify=self.infinity)
        brawlbot.start()
        self.running_bots_count += 1
        self.running_bots.append(brawlbot)


    def stop_all_bots(self):
        for bot in self.running_bots:
            print(f'[{get_time()}] {Fore.GREEN}✓{Fore.RESET} Бот {bot} остановлен')
            bot.kill()
            self.running_bots_count -= 1
            self.running_bots.remove(bot)

    def init_brawlbot_start(self):
        if self.running_bots_count >= 1:
            print(f'[{get_time()}] {Fore.YELLOW}!{Fore.RESET} Отслежена попытка запустить бота в параллельном выполнении... Запуск бота отклонен.')
        else:
            print(f'[{get_time()}] {Fore.GREEN}✓{Fore.RESET} Инициализация бота завершена. Запуск...')
            self.__start_bot()


    def start(self):
        if self.START_MODE == 'console':
            # start_state = button_dialog(title='BrawlBot Ctrl',
            #                             text='Запустить бота?',
            #                             buttons=[('Запуск', True),
            #                                      ('Отладка', None),
            #                                      ('Отмена', False)]).run()
            start_state = True
            if start_state is True:
                self.infinity = False 
                self.init_brawlbot_start()
            elif start_state is None:
                self.infinity = True
                self.init_brawlbot_start()
            elif start_state is False:
                exit(code=0)




