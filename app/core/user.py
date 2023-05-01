import pickle
import random
import config

from random_words import RandomWords


class User:
    def __init__(self, name, avatar, strict_spelling=False):
        self.name = name
        self.avatar = avatar
        self.commonly_misspelled = self.load_dictionary("commonly_misspelled")
        self.common_english_words = self.load_dictionary("common_english_words")
        self.vocabulary = {}
        self.learned_words = {}
        self.strict_spelling = strict_spelling
        self.attempts_correct = 0
        self.attempts_incorrect = 0

    def generate_next_word(self):
        """
        Randomly retrieves one word for practice from one of the dictionaries
        :type dict
        :return: dictionary containing a word and its definition
        """
        choice_source = self.determine_word_choice_source()
        if 'users_vocabulary' in choice_source:
            users_vocabulary_list = list(self.vocabulary.keys())
            word = users_vocabulary_list[random.randrange(0, len(users_vocabulary_list) - 1)]
            word_dict = {word: self.vocabulary[word]}
        elif 'commonly_misspelled' in choice_source:
            commonly_misspelled_list = list(self.commonly_misspelled.keys())
            word = commonly_misspelled_list[random.randrange(0, len(commonly_misspelled_list) - 1)]
            test = self.commonly_misspelled[word]
            word_dict = {word: self.commonly_misspelled[word]}
            # self.commonly_misspelled.remove(word)
        elif 'common_english' in choice_source:
            common_english_words_list = list(self.common_english_words.keys())
            word = common_english_words_list[random.randrange(0, len(common_english_words_list) - 1)]
            word_dict = {word: self.common_english_words[word]}
            # self.common_english_words.remove(word)
        else:
            random_words = RandomWords()
            word = random_words.random_word(min_letter_count=4)
            word_dict = {word: {"definition": None}}
        return word_dict

    def determine_word_choice_source(self):
        #  TODO: Remove debug prints
        """
        Randomly picks a dictionary from which to pull the next word
        :return: lst
        """
        if len(self.vocabulary) > 30:
            choice_source = random.choices(['users_vocabulary', 'commonly_misspelled',
                                            'common_english_words', 'random_words'],
                                           weights=[4, 3, 2, 1], k=1)
        else:
            choice_source = random.choices(['commonly_misspelled', 'common_english_words', 'random_words'],
                                           weights=[4, 3, 1], k=1)
        print(f'DEBUG: Word choice source: {choice_source}')
        return choice_source

    @staticmethod
    def load_dictionary(name):
        with open(f'assets/{name}', mode='rb') as document:
            return pickle.load(document)

    def spell_check(self, word_dict, user_word):
        word = list(word_dict.keys())[0]
        user_word.title()
        if user_word == '':
            status = None
        elif user_word == word:
            status = 'correct'
            if word in self.vocabulary.keys():
                self.vocabulary[word]["times_to_spell"] -= 1
                self.attempts_correct += 1
                self.check_word_learned(word, word_dict)
            else:
                self.learned_words.update(word_dict)
                self.attempts_correct += 1
        else:
            status = 'incorrect'
            if word in self.vocabulary.keys():
                self.vocabulary[word]["times_to_spell"] += 1
                self.attempts_incorrect += 1
            else:
                word_dict.update({"times_to_spell": config.ATTEMPTS_TO_LEARN_WORD})
                self.vocabulary.update(word_dict)
                self.attempts_incorrect += 1
        return status

    def check_word_learned(self, word, word_dict):
        """
        Checks if number of attempts is 0 which means the word is considered
        to be learned. Removes learned word from misspelled_dict and puts it
        into vocabulary_lst
        :param word: str
        :param word_dict: dict
        :return:
        """
        if self.vocabulary[word]["times_to_spell"] == 0:
            self.vocabulary.pop(word)
            self.learned_words.update(word_dict)

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
