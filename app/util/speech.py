import logging
import os
import platform
import random
import threading

import pyttsx3

from core.config import MACOS_VOICES


def say(word, volume):
    if platform.system() == 'Darwin':  # macOS
        voice = random.choice(MACOS_VOICES)
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
