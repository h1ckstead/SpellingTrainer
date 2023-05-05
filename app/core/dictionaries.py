import pickle

from spellchecker import SpellChecker

import config


class Dictionaries:
    def __init__(self):
        self.commonly_misspelled = self.load_dictionary("commonly_misspelled")
        self.common_english_words = self.load_dictionary("common_english_words")
        self.vocabulary = {}
        self.learned_words = {}

    @staticmethod
    def load_dictionary(name):
        with open(f'assets/{name}', mode='rb') as document:
            return pickle.load(document)

    def add_word(self, word):
        status = 'OK'
        dictionaries = [self.commonly_misspelled, self.common_english_words,
                        self.vocabulary, self.learned_words]
        word_exists, dictionary = self.check_word_in_dicts(word, dictionaries)
        if word_exists and dictionary is self.vocabulary:
            status = 'already_exists'
        elif word_exists:
            word_dict = dictionary[word]
            self.vocabulary.update({word: word_dict})  # TODO: set times to spell to 10!
            dictionary.pop(word)
        else:
            word_dict = {word: {"times_to_spell": config.ATTEMPTS_TO_LEARN_WORD}}
            self.vocabulary.update(word_dict)
        return status

    def delete_words(self, words):
        for word in words:
            self.learned_words.update({word: self.vocabulary[word]})
            self.vocabulary.pop(word)

    @staticmethod
    def check_spelling(user_word):
        spell_checker = SpellChecker()
        misspelled = list(spell_checker.unknown([user_word]))
        if len(misspelled) > 0:
            return spell_checker.correction(misspelled[0])

    @staticmethod
    def check_word_in_dicts(user_word, dictionaries):
        for dictionary in dictionaries:
            if user_word in dictionary.keys():
                return True, dictionary
        return None, None
