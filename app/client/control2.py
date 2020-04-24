
from datetime import datetime

from colorama import Fore, init

from app.client.brawlbot import Bot


def get_time():
    return datetime.strftime(datetime.now(), "%H:%M:%S")

class Settings:

    def __init__(self, start_mode: str,
                 log_to_file: bool,
                 log_to_console: bool,
                 log_level_debug: bool,
                 log_requests_to_server: bool,
                 multiple_mode: bool,
                 infinity_mode: bool,
                 simplified_algorithms_mode: bool):

        self.start_mode = start_mode

        self.log_to_file = log_to_file
        self.log_to_console = log_to_console
        self.log_level_debug = log_level_debug
        self.log_requests_to_server = log_requests_to_server

        self.multiple_mode = multiple_mode
        self.infinity_mode = infinity_mode
        self.simplified_algorithms_mode = simplified_algorithms_mode


class CtrlWrapper:
    def __init__(self, settings: Settings):

        self.settings = settings

    def __start_bot(self, bot):
        bot.start()
        bot.log_to_console(f'Бот {bot} запущен', level='succ')
        self.running_bots_count += 1
        self.running_bots.append(bot)

    def __start_bot(self, bot):
        bot.kill()
        bot.log_to_console(f'Бот {bot} остановлен', level='succ')
        self.running_bots_count -= 1
        self.running_bots.remove(bot)

    def stop_all_bots(self):
        for bot in self.running_bots:
            bot.kill()
            self.running_bots_count -= 1
            self.running_bots.remove(bot)

    def initialize_bot(self):
        if self.running_bots_count >= 1:
            print(f'[{get_time()}] {Fore.YELLOW}!{Fore.RESET} Отслежена попытка запустить бота в параллельном выполнении... Запуск бота отклонен.')
        else:
            brawlbot = Bot(self.settings)
            print(f'[{get_time()}] {Fore.GREEN}✓{Fore.RESET} Инициализация бота завершена. Запуск...')
            self.__start_bot(brawlbot)


    def start(self):
        if self.settings.start_mode == 'console':
            self.initialize_bot()
