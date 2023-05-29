import logging
import os
import platform
import random
import threading

import pyttsx3

from core.config import MONTEREY_VOICES, VENTURA_VOICES


def say(word, volume):
    if platform.system() == 'Darwin':  # macOS
        mac_version = platform.mac_ver()[0]
        voice = get_random_macos_voice(mac_version)
        os.system(f'/usr/bin/say [[volm {volume}]] -v {voice} ' + word)
        logging.info(f'{voice} is speaking')
    elif platform.system() == 'Windows':  # Windows
        engine = pyttsx3.init()
        voice = get_random_win_voice(engine)
        say_in_thread(word, volume, voice, engine)
        # win_say(word, volume, voice, engine)
        logging.info(f'{voice} is speaking')
    else:
        logging.error('Sorry, your operating system is not supported.')


def get_random_win_voice(engine):
    voices = engine.getProperty('voices')
    return random.choice(voices).id


def win_say(word, volume, voice, engine, rate=0.8):
    initial_rate = engine.getProperty('rate')
    engine.setProperty('voice', voice)
    engine.setProperty('volume', volume)
    engine.setProperty('rate', initial_rate * rate)
    engine.say(word)
    engine.runAndWait()


def say_in_thread(word, volume, voice, engine):
    threading.Thread(target=win_say, args=(word, volume, voice, engine)).start()


def get_random_macos_voice(mac_version):
    # cmd = "say -v '?' | grep 'en[_-]' | awk -F '[ .]' '{print $1}'"
    # cmd_out = subprocess.run(cmd, capture_output=True, shell=True, text=True)
    # str_out = cmd_out.stdout.strip().splitlines()
    # return random.choice(str_out)
    version_components = mac_version.split('.')
    major_version = int(version_components[0])

    if major_version <= 12:
        return random.choice(MONTEREY_VOICES)
    else:
        return random.choice(VENTURA_VOICES)
