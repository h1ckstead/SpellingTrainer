import random
import os
from app.config import MAC_OS_VOICES


def read_aloud(word_dict):
    word = list(word_dict.keys())[0]
    voice = MAC_OS_VOICES[random.randint(0, len(MAC_OS_VOICES)-1)]
    os.system(f'/usr/bin/say -v {voice} ' + word)
    print(f'{voice} is speaking')


# maybe later
# def get_voices_list():
#     cmd = "say -v '?' |grep "en[_-]"
#     cmd_out = run(cmd, capture_output=True, shell=True)
#     str_out = cmd_out.stdout.splitlines()
#     print(str_out)

