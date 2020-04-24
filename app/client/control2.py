
from datetime import datetime
from json import load
from time import sleep

from colorama import Fore, init
from prompt_toolkit.shortcuts import ProgressBar, button_dialog

from app.client.brawlbot import Bot


def get_time():
    return datetime.strftime(datetime.now(), "%H:%M:%S")



