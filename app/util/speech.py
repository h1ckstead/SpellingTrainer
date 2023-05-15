import os
import platform
import random

from core.config import MAC_OS_VOICES


def read_aloud(word_dict):
    word = list(word_dict.keys())[0]
    voice = MAC_OS_VOICES[random.randint(0, len(MAC_OS_VOICES) - 1)]
    os.system(f'/usr/bin/say -v {voice} ' + word)
    print(f'{voice} is speaking')


# import win32com.client as wincl

def say(word, volume):
    if platform.system() == 'Darwin':  # macOS
        voice = MAC_OS_VOICES[random.randint(0, len(MAC_OS_VOICES) - 1)]
        os.system(f'/usr/bin/say [[volm {volume}]] -v {voice} ' + word)
        print(f'{voice} is speaking')
    # elif platform.system() == 'Windows':  # Windows
    #     engine = wincl.Dispatch("SAPI.SpVoice")
    #     voices = engine.GetVoices()
    #     voice = voices.Item(random.randint(0, voices.Count - 1)).GetDescription()
    #     engine.Speak(word)
    #     print(f'{voice} is speaking')
    # else:
    #     print('Sorry, your operating system is not supported.')

# word_dict = {'hello': 'world'}
# read_aloud(word_dict)

# maybe later
# def get_voices_list():
#     cmd = "say -v '?' |grep "en[_-]"
#     cmd_out = run(cmd, capture_output=True, shell=True)
#     str_out = cmd_out.stdout.splitlines()
#     print(str_out)
