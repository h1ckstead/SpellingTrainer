import pickle
from app.util import common_words


class User:
    def __init__(self, name, avatar):
        self.name = name
        self.avatar = avatar
        self.commonly_misspelled_lst = common_words.commonly_misspelled_lst()
        self.common_english_words_lst = common_words.common_english_words_lst()
        self.spelled_ok_lst = []
        self.misspelled_dict = {}
        self.attempts_correct = 0
        self.attempts_incorrect = 0

#  TODO: save to specific location in the system and not in project directory
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
