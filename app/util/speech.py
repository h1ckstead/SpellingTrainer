import logging
import os
import platform
import random
import subprocess
import threading

import pyttsx3

from core.config import MAC_OS_VOICES


# def read_aloud(word_dict):
#     word = list(word_dict.keys())[0]
#     voice = MAC_OS_VOICES[random.randint(0, len(MAC_OS_VOICES) - 1)]
#     os.system(f'/usr/bin/say -v {voice} ' + word)
#     print(f'{voice} is speaking')


def say(word, volume):
    if platform.system() == 'Darwin':  # macOS
        voice = get_random_macos_voice()
        os.system(f'/usr/bin/say [[volm {volume}]] -v {voice} ' + word)
        logging.info(f'{voice} is speaking')
    elif platform.system() == 'Windows':  # Windows
        engine = pyttsx3.init()
        voice = get_random_win_voice(engine)
        say_in_thread(word, volume, voice, engine)
        logging.info(f'{voice} is speaking')
    else:
        logging.error('Sorry, your operating system is not supported.')


def get_random_win_voice(engine):
    voices = engine.getProperty('voices')
    # random_voice = random.choice(voices).id
    return random.choice(voices).id


def win_say(word, volume, voice, engine):
    engine.setProperty('voice', voice)
    engine.setProperty('volume', volume)
    engine.say(word)
    engine.runAndWait()


def say_in_thread(word, volume, voice, engine):
    thread = threading.Thread(target=win_say, args=(word, volume, voice, engine))
    thread.start()


def get_random_macos_voice():
    # cmd = "say -v '?' | grep 'en[_-]' | awk -F '[ .]' '{print $1}'"
    # cmd_out = subprocess.run(cmd, capture_output=True, shell=True, text=True)
    # str_out = cmd_out.stdout.strip().splitlines()
    # return random.choice(str_out)
    return random.choice(MAC_OS_VOICES)
