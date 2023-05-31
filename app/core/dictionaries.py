from spellchecker import SpellChecker

from core import config, constants
from util import helpers


class Dictionaries:
    def __init__(self):
        self.high_priority_words = helpers.load_dictionary(constants.HIGH_PRIORITY_WORDS)
        self.low_priority_words = helpers.load_dictionary(constants.LOW_PRIORITY_WORDS)
        self.vocabulary = {}
        self.learned_words = {}

    def add_word_to_vocab_manually(self, word, alternative_spelling=None):
        """
        Function for handling manual word adding to vocabulary. It checks if the word or
        its alternative spelling already exists in one of the dictionaries and moves it
        to vocabulary.

        :param word: str
        :param alternative_spelling: str
        :return: str status
        """
        status = constants.OK
        word_exists, word_dictionary = self.check_word_in_dicts(word)
        if word_exists and word_dictionary is self.vocabulary and not alternative_spelling:
            return constants.ALREADY_EXISTS
        if alternative_spelling:
            alt_word_exists, alt_dictionary = self.check_word_in_dicts(alternative_spelling)
            if alt_word_exists and alt_dictionary is self.vocabulary:
                self.vocabulary.update({word: {constants.AmE: alternative_spelling,
                                               constants.TIMES_TO_SPELL: config.TIMES_TO_SPELL_IF_INCORRECT}})
                self.vocabulary.pop(alternative_spelling)
            elif alt_word_exists:
                self.vocabulary.update({word: {constants.AmE: alternative_spelling,
                                               constants.TIMES_TO_SPELL: config.TIMES_TO_SPELL_IF_INCORRECT}})
                alt_dictionary.pop(alternative_spelling)
            elif word_exists:
                word_dictionary.pop(word)
                self.vocabulary.update({word: {constants.AmE: alternative_spelling,
                                               constants.TIMES_TO_SPELL: config.TIMES_TO_SPELL_IF_INCORRECT}})
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
        """
        Adds word to vocabulary with value "times_to_spell" based on status.

        :param word: str
        :param word_dict: dict
        :param status: str
        :param session: Session object
        :return:
        """
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
        """
        Deletes words from vocabulary and adds them to learned words.

        :param words: list of str
        :return:
        """
        for word in words:
            self.learned_words.update({word: self.vocabulary[word]})
            self.vocabulary.pop(word)

    @staticmethod
    def check_spelling(user_word):
        """
        Spellchecks users word and returns possible correction.

        :param user_word: string
        :return: str or None
        """
        spell_checker = SpellChecker()
        misspelled = list(spell_checker.unknown([user_word]))
        if len(misspelled) > 0:
            return spell_checker.correction(misspelled[0])

    def check_word_in_dicts(self, user_word):
        """
        Checks if word already exists in one of the dicts.

        :param user_word: str
        :return: bool, dict or None, None
        """
        dictionaries = [self.high_priority_words["data"], self.low_priority_words["data"], self.vocabulary,
                        self.learned_words]
        for dictionary in dictionaries:
            if user_word in dictionary:
                return True, dictionary
        return None, None

    def increment_times_to_spell(self, word):
        """
        Increments "times_to_spell" parameter of the word.

        :param word: str
        :return:
        """
        self.vocabulary[word][constants.TIMES_TO_SPELL] += 1

    def decrement_times_to_spell(self, word):
        """
        Decrements "times_to_spell" parameter of the word.

        :param word: str
        :return:
        """
        self.vocabulary[word][constants.TIMES_TO_SPELL] -= 1

    def mark_word_as_learned(self, word, word_dict, session):
        """
        Removes word dict from vocabulary and adds it to learned_words dict.
        Increments Session learned words attribute for statistics.

        :param word: str
        :param word_dict: dict containing the word and its params
        :param session: Session object
        :return:
        """
        self.vocabulary.pop(word)
        self.learned_words.update(word_dict)
        session.increment_learned_words()
