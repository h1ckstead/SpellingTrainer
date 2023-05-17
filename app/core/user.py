import logging
import pickle
import random

from core.dictionaries import Dictionaries
from util import helpers


class User:
    def __init__(self, name, strict_spelling, avatar=None):
        self.name = name
        if avatar is None:
            self.avatar = self.pick_random_avatar()
        else:
            self.avatar = avatar
        self.dictionaries = Dictionaries()
        self.strict_spelling = strict_spelling
        self.attempts_correct = 0
        self.attempts_incorrect = 0
        self.volume = 0.5
        self.only_from_vocabulary = False
        self.save_progress()

    @property
    def total_attempts(self):
        return self.attempts_correct + self.attempts_incorrect

    def edit_username(self, new_name):
        with open('savefile', 'rb+') as file:
            loaded_data = pickle.load(file)
            if self.name in loaded_data:
                loaded_data[new_name] = loaded_data.pop(self.name)
                loaded_data['last_user'] = new_name
                self.name = new_name
                file.seek(0)
                pickle.dump(loaded_data, file)
                logging.info("Updated savefile")
            else:
                logging.error(f"User '{self.name}' does not exist in the savefile.")

    def edit_avatar(self, new_avatar):
        self.avatar = new_avatar
        self.save_progress()

    def toggle_strict_spelling(self, state):
        self.strict_spelling = state
        self.save_progress()

    def increment_attempts_correct(self):
        self.attempts_correct += 1
        self.save_progress()

    def increment_attempts_incorrect(self):
        self.attempts_incorrect += 1
        self.save_progress()

    def set_volume(self, value):
        self.volume = value
        self.save_progress()

    def toggle_only_from_vocabulary(self, state):
        self.only_from_vocabulary = state
        self.save_progress()

    @staticmethod
    def pick_random_avatar():
        avatars = helpers.get_avatars_list()
        return random.choice(avatars)

    def save_progress(self):
        try:
            with open('savefile', 'rb+') as file:
                loaded_data = pickle.load(file)
                loaded_data.update({self.name: self, 'last_user': self.name})
                file.seek(0)
                pickle.dump(loaded_data, file)
                logging.info("Updated savefile")
        except FileNotFoundError:
            with open('savefile', 'wb') as file:
                data = {self.name: self, 'last_user': self.name}
                pickle.dump(data, file)
                logging.info(f"Created savefile: {data}")
