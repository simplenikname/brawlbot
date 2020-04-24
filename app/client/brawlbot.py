from datetime import datetime
from threading import Thread
from time import sleep

from colorama import Fore, init
from pyautogui import click, press, keyDown, keyUp, size, center, Point

from app.client.utils import (continue_if_not_locate_on_screen, find, on_screen,
                   wait_until_locate_on_screen)
from app.client.control import Settings

init()

class Worker(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, daemon=True, **kwargs)
        self.running = False 
        self.killed = False

    def kill(self):
        self.killed = True


class Walker(Worker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move_key = 'w' 

    def __key_down(self):
        keyUp(self.move_key)
        keyDown(self.move_key)

    def __switch(self):
        press(self.move_key)
        self.__key_down()
        sleep(10)

    def run(self):
        sleep(2)
        while not self.killed:
            self.__switch()

    def kill(self):
        self.killed = True
        keyUp('w')


class Attacker(Worker):
    def run(self):
        while not self.killed:
            press('space')
            sleep(.3)


class Bot(Worker):
    def __init__(self, settings: Settings, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.settings = settings

           
    def log_to_console(self,
                       message,
                       level: str = 'info',
                       **kwargs):
        '''
        level - succ, erro, warn, info, debg
        '''
        if level == 'succ':
            display_mode = f'{Fore.GREEN}[✓]{Fore.RESET}'
        elif level == 'erro':
            display_mode = f'{Fore.RED}[x]{Fore.RESET}'
        elif level == 'warn':
            display_mode = f'{Fore.YELLOW}[!]{Fore.RESET}'
        elif level == 'debg' and self.settings.log_level_debug is True:
            display_mode = f'{Fore.LIGHTWHITE_EX}--→{Fore.RESET}'
        elif level == 'info':
            display_mode = f'{Fore.CYAN}[~]{Fore.RESET}'
        # else:
        #     display_mode = f'{Fore.BLUE}[*]{Fore.RESET}' # •
        date = datetime.strftime(datetime.now(), '%H:%M:%S')
        message = f'{self} [{date}] {display_mode} {message}'
        print(message)

    def check_play_button(self):
        if play_button := find('./app/client/images/battle/start.png'):
            self.play_button = play_button
            self.log_to_console(
                'Кнопка ИГРАТЬ обнаружена на экране. Бот начал работу...')
        else:
            self.log_to_console(
                'Кнопка ИГРАТЬ не обнаружена на экране. Завершение работы.',
                level='warn')
            self.host.stop_all_bots()
            return 1
 
    def start_battle(self):
        click(self.play_button)

    def wait_loading(self):
        continue_if_not_locate_on_screen('./app/client/images/battle/loading.png')

    def append_demons(self, demons):
        for d in demons:
            message = f'Демон {d.__class__} добавлен в очередь'
            self.log_to_console(message)
            self.demons.append(d)

    def run_demons(self):
        self.log_to_console(self.demons, 'debg')
        for d in self.demons:
            message = f'Демон {d.__class__} начал работу'
            self.log_to_console(message)
            d.start()

    def kill_all_demons(self):
        for d in self.demons:
            message = f'Демон {d.__class__} завершил работу'
            self.log_to_console(message, 'succ')
            d.kill()
        self.demons = []

    def process_battle_results(self, t=.5):
        self.log_to_console('Определение результатов боя...')
        found_data = {}
        # определение результатов боя - победа или поражение
        if battle_result := find('./app/client/images/battle/win.png'):
            found_data['battle_result'] = 'Победа'
        else:
            found_data['battle_result'] = 'Поражение'
        # нажатие на кнопку ДАЛЕЕ
        click(wait_until_locate_on_screen('./app/client/images/battle/next.png'))
        # нажатие на кнопку ВЫЙТИ
        click(wait_until_locate_on_screen('./app/client/images/battle/exit2.png'))
        sleep(t if t > 0 else .1)
        self.log_to_console(found_data['battle_result'])

    def check_chest(self, t=.5):
        chest = Point(x=414, y=968) # FHD
        self.log_to_console('Обнаружение сундука...')
        click(chest)
        sleep(t if t > 0 else .5)
        while not on_screen('./app/client/images/battle/start.png'):
            click(chest)

    def run(self):
        while not self.killed:
            if not self.settings.start_from_battle_stage:
                # проверка присудствия на экране кнопки ИГРАТЬ
                if self.check_play_button() == 1: return
                # начатие боя
                self.start_battle()
                # ожидание окончания загрузки
                self.wait_loading()
            # создание и запуск новых потоков-демонов осуществяющих передвижение
            # бойца по карте, использование супера, и атаку врагов во время боя
            # NOTE: для корректной работы необходимо настроить управление в используемом эмуляторе Android-а
            self.append_demons([Walker(), Attacker()])
            self.run_demons()
            # вход в mainloop
            while not on_screen('./app/client/images/battle/next.png'):
                if self.killed is True:
                    self.kill_all_demons()
                    return
                sleep(1)
            # завершение работы демонов
            self.kill_all_demons()
            # выход из боя и анализ результатов
            self.process_battle_results()
            # проверка возможности открыть сундук
            self.check_chest()
            if self.settings.infinity_mode is False:
                self.host.stop_all_bots()
                return
            

