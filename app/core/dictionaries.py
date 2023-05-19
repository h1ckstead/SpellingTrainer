import pickle

from spellchecker import SpellChecker

from core import config, constants
from util import helpers


class Dictionaries:
    def __init__(self):
        self.commonly_misspelled = self.load_dictionary(constants.COMMONLY_MISSPELLED)
        self.common_english_words = self.load_dictionary(constants.COMMON_ENGLISH_WORDS)
        self.vocabulary = {}
        self.learned_words = {}

    @staticmethod
    def load_dictionary(name):
        with open(helpers.get_path(f'assets/{name}'), mode='rb') as document:
            return pickle.load(document)

    def add_word_to_vocab_manually(self, word, alternative_spelling=None):
        status = constants.OK
        dictionaries = [self.commonly_misspelled, self.common_english_words,
                        self.vocabulary, self.learned_words]
        word_exists, word_dictionary = self.check_word_in_dicts(word, dictionaries)
        if word_exists and word_dictionary is self.vocabulary:
            return constants.ALREADY_EXISTS
        if alternative_spelling:
            alt_word_exists, alt_dictionary = self.check_word_in_dicts(alternative_spelling, dictionaries)
            if alt_word_exists and alt_dictionary is self.vocabulary:
                self.vocabulary.update({word: {constants.AmE: alternative_spelling,
                                               constants.TIMES_TO_SPELL: config.TIMES_TO_SPELL_IF_INCORRECT}})
                self.vocabulary.pop(alternative_spelling)
            elif alt_word_exists:
                self.vocabulary.update({word: {constants.AmE: alternative_spelling,
                                               constants.TIMES_TO_SPELL: config.TIMES_TO_SPELL_IF_INCORRECT}})
                alt_dictionary.pop(alternative_spelling)
            elif word_exists:
                self.vocabulary.update({word: {constants.AmE: alternative_spelling,
                                               constants.TIMES_TO_SPELL: config.TIMES_TO_SPELL_IF_INCORRECT}})
                word_dictionary.pop(word)
            else:
                self.vocabulary.update({word: {constants.AmE: alternative_spelling,
                                               constants.TIMES_TO_SPELL: config.TIMES_TO_SPELL_IF_INCORRECT}})
        else:
            if word_exists:
                word_dict = word_dictionary[word]
                word_dict.update({constants.TIMES_TO_SPELL: config.TIMES_TO_SPELL_IF_INCORRECT})
                self.vocabulary.update({word: word_dict})
                word_dictionary.pop(word)
            else:
                word_dict = {word: {constants.TIMES_TO_SPELL: config.TIMES_TO_SPELL_IF_INCORRECT}}
                self.vocabulary.update(word_dict)
        return status

    def add_word_to_vocab(self, word, word_dict, status, session):
        session.increment_new_words()
        if status == constants.CORRECT:
            word_dict[word].update({constants.TIMES_TO_SPELL: config.TIMES_TO_SPELL_IF_CORRECT})
            self.vocabulary.update(word_dict)
        elif status == constants.INCORRECT:
            word_dict[word].update({constants.TIMES_TO_SPELL: config.TIMES_TO_SPELL_IF_INCORRECT})
            self.vocabulary.update(word_dict)
        else:
            raise ValueError(f"Invalid status value. Must be either \"{constants.CORRECT}\" or "
                             f"\"{constants.INCORRECT}\"")

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

    def increment_times_to_spell(self, word):
        self.vocabulary[word][constants.TIMES_TO_SPELL] += 1

    def decrement_times_to_spell(self, word):
        self.vocabulary[word][constants.TIMES_TO_SPELL] -= 1

    def mark_word_as_learned(self, word, word_dict, session):
        self.vocabulary.pop(word)
        self.learned_words.update(word_dict)
        session.increment_learned_words()
