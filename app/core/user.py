import pickle

from app.core.dictionaries import Dictionaries


class User:
    def __init__(self, name, avatar, strict_spelling):
        self.name = name
        self.avatar = avatar
        self.dictionaries = Dictionaries()
        self.strict_spelling = strict_spelling
        self.attempts_correct = 0
        self.attempts_incorrect = 0

    def edit_username(self, new_name):
        self.name = new_name
        self.save_progress()

    def edit_avatar(self, new_avatar):
        self.avatar = new_avatar
        self.save_progress()

    def toggle_strict_spelling(self, state):
        self.strict_spelling = state
        self.save_progress()

    def save_progress(self):
        try:
            with open('savefile', 'rb+') as file:
                loaded_data = pickle.load(file)
                loaded_data.update({self.name: self, 'last_user': self.name})
                file.seek(0)
                pickle.dump(loaded_data, file)
        except FileNotFoundError:
            with open('savefile', 'wb') as file:
                data = {self.name: self, 'last_user': self.name}
                pickle.dump(data, file)

    @staticmethod
    def load_save():
        try:
            with open('savefile', 'rb') as file:
                data = pickle.load(file)
            return data
        except FileNotFoundError:
            return None
