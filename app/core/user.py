import pickle
import random
import config

from random_words import RandomWords


class User:
    def __init__(self, name, avatar, strict_spelling):
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
        :return: dictionary containing a word and its definition
        """
        choice_source = self.determine_word_choice_source()
        if 'users_vocabulary' in choice_source:
            users_vocabulary_list = list(self.vocabulary.keys())
            word = users_vocabulary_list[random.randrange(0, len(users_vocabulary_list) - 1)]
            word_dict = {word: self.vocabulary[word]}
            if self.strict_spelling and 'AmE' in word_dict[word].keys():
                word_dict = self.choose_which_spelling(word, word_dict)
        elif 'commonly_misspelled' in choice_source:
            commonly_misspelled_list = list(self.commonly_misspelled.keys())
            word = commonly_misspelled_list[random.randrange(0, len(commonly_misspelled_list) - 1)]
            word_dict = {word: self.commonly_misspelled[word]}
            if self.strict_spelling and 'AmE' in word_dict[word].keys():
                word_dict = self.choose_which_spelling(word, word_dict)
        elif 'common_english' in choice_source:
            common_english_words_list = list(self.common_english_words.keys())
            word = common_english_words_list[random.randrange(0, len(common_english_words_list) - 1)]
            word_dict = {word: self.common_english_words[word]}
            if self.strict_spelling and 'AmE' in word_dict[word].keys():
                word_dict = self.choose_which_spelling(word, word_dict)
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
        print(f'Word choice source: {choice_source}')
        return choice_source

    @staticmethod
    def choose_which_spelling(word, word_dict):
        word_choice = random.choice([word, word_dict[word]['AmE']])
        if word_choice in word_dict.keys():
            word_dict[word].update({'spelling': 'BrE'})
            print("Spelling: BrE")
            return word_dict
        else:
            word_dict[word].update({'spelling': 'AmE'})
            print("Spelling: AmE")
            return word_dict

    @staticmethod
    def load_dictionary(name):
        with open(f'assets/{name}', mode='rb') as document:
            return pickle.load(document)

    def spell_check(self, word_dict, user_word):
        word, user_word = self.prepare_data(word_dict, user_word)
        if user_word == '':
            status = None
        elif self.strict_spelling and "spelling" in word_dict[word].keys():
            status = self.strict_spellcheck(word, word_dict, user_word)
        else:
            status = self.soft_spellcheck(word, user_word, word_dict)
        return status

    @staticmethod
    def prepare_data(word_dict, user_word):
        word = list(word_dict.keys())[0]
        user_word.title()
        return word, user_word

    def strict_spellcheck(self, word, word_dict, user_word):
        if word_dict[word]["spelling"] == "BrE" and user_word == word:
            status = 'correct'
            self.check_if_word_in_vocabulary(word, word_dict, status)
        elif word_dict[word]["spelling"] == "AmE" and user_word == word_dict[word]["AmE"]:
            status = 'correct'
            self.check_if_word_in_vocabulary(word, word_dict, status)
        else:
            status = 'incorrect'
            self.check_if_word_in_vocabulary(word, word_dict, status)
        return status

    def soft_spellcheck(self, word, user_word, word_dict):
        if 'AmE' in word_dict[word].keys():
            status = self.soft_spellcheck_alt_spelling(word, user_word, word_dict)
        else:
            if user_word == word:
                status = 'correct'
                self.check_if_word_in_vocabulary(word, word_dict, status)
            else:
                status = 'incorrect'
                self.check_if_word_in_vocabulary(word, word_dict, status)
        return status

    def soft_spellcheck_alt_spelling(self, word, user_word, word_dict):
        words = [word, word_dict[word]['AmE']]
        if user_word in words:
            status = 'correct'
            self.check_if_word_in_vocabulary(word, word_dict, status)
        else:
            status = 'incorrect'
            self.check_if_word_in_vocabulary(word, word_dict, status)
        return status

    def check_if_word_in_vocabulary(self, word, word_dict, status):
        if status == 'correct':
            if word in self.vocabulary.keys():
                self.vocabulary[word]["times_to_spell"] -= 1
                self.attempts_correct += 1
                self.check_word_learned(word, word_dict)
            else:
                self.learned_words.update(word_dict)
                self.pop_word_from_dictionary(word)
                self.attempts_correct += 1
        elif status == 'incorrect':
            if word in self.vocabulary.keys():
                self.vocabulary[word]["times_to_spell"] += 1
                self.attempts_incorrect += 1
            else:
                word_dict.update({"times_to_spell": config.ATTEMPTS_TO_LEARN_WORD})
                self.vocabulary.update(word_dict)
                self.pop_word_from_dictionary(word)
                self.attempts_incorrect += 1
        else:
            raise Exception("Unknown status")

    def pop_word_from_dictionary(self, word):
        if word in self.commonly_misspelled.keys():
            self.commonly_misspelled.pop(word)
        elif word in self.common_english_words.keys():
            self.common_english_words.pop(word)

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
