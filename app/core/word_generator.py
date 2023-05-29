import logging
import random

from random_words import RandomWords

from core.constants import BrE, AmE, DEFINITIONS, SPELLING, VOCABULARY, RANDOM_WORDS, HIGH_PRIORITY_WORDS, \
    LOW_PRIORITY_WORDS


class WordGenerator:
    def __init__(self, user, callback):
        self.user = user
        self.callback = callback

    def generate_word(self):
        """
        Retrieves one random word for practice from one of the existing dictionaries or
        generates a random word.

        :return: dictionary containing a word and its definition
        """
        choice_source = self.pick_dictionary()
        logging.info(f"Randomly picking a word from {choice_source}")
        if choice_source == VOCABULARY:
            try:
                word = random.choice(list(self.user.dictionaries.vocabulary.keys()))
                word_dict = {word: self.user.dictionaries.vocabulary[word]}
            except IndexError:
                self.callback()
                return
        elif choice_source == HIGH_PRIORITY_WORDS:
            word = random.choice(list(self.user.dictionaries.high_priority_words["data"].keys()))
            word_dict = {word: self.user.dictionaries.high_priority_words["data"][word]}
        elif choice_source == LOW_PRIORITY_WORDS:
            word = random.choice(list(self.user.dictionaries.low_priority_words["data"].keys()))
            word_dict = {word: self.user.dictionaries.low_priority_words["data"][word]}
        else:
            word, word_dict = self.generate_random_word()
        if self.user.strict_spelling and word_dict.get(word, {}).get(AmE):
            word_dict = self.pick_which_spelling(word, word_dict)
        logging.info(word_dict)
        return word_dict

    def generate_random_word(self):
        """
        Uses RandomWords to generate a word with min length of 5.

        :return: dict containing word and definition
        """
        random_words = RandomWords()
        while True:
            word = random_words.random_word(min_letter_count=5).title()
            if not self.is_duplicate(word.title()):
                word_dict = {word: {DEFINITIONS: None}}  # TODO: Think about loading definition in the background
                return word, word_dict

    def is_duplicate(self, word):
        """
        Checks if the word has already been learned or is in the users' vocabulary.

        :param word: str containing a random word
        :return: bool
        """
        if word in self.user.dictionaries.vocabulary or word in self.user.dictionaries.learned_words:
            return True
        else:
            return False

    def pick_dictionary(self):
        """
        Randomly chooses a dictionary from which to pick the next word. Each dictionary
        has its own weight so some are more likely to get chosen than others.

        :return: str containing dictionary name
        """
        if self.user.only_from_vocabulary:
            return VOCABULARY

        choice_sources = self.get_non_empty_dicts()
        weights = {
            VOCABULARY: 5,
            HIGH_PRIORITY_WORDS: 4,
            LOW_PRIORITY_WORDS: 3,
            RANDOM_WORDS: 1
        }

        if len(self.user.dictionaries.vocabulary) > 30:
            choice_sources.append(VOCABULARY)

        choice_source = random.choices(choice_sources + [RANDOM_WORDS],
                                       weights=[weights[dict_name] for dict_name in choice_sources] + [1],
                                       k=1)
        return choice_source[0]

    def get_non_empty_dicts(self):
        """
        Checks if high_priority or low_priority dictionaries still
        have words. If so, they are added to choice_sources.

        :return: list of strings
        """
        choice_sources = []
        if len(self.user.dictionaries.high_priority_words["data"]) > 0:
            choice_sources.append(HIGH_PRIORITY_WORDS)
        if len(self.user.dictionaries.low_priority_words["data"]) > 0:
            choice_sources.append(LOW_PRIORITY_WORDS)
        return choice_sources

    @staticmethod
    def pick_which_spelling(word, word_dict):
        """
        Randomly choose British or American spelling for words that have
        different spellings.

        :param word: str British spelling
        :param word_dict: dict containing definitions and American spelling
        :return: original dict with added key Spelling
        """
        word_choice = random.choice([word, word_dict[word][AmE]])
        if word_choice in word_dict.keys():
            word_dict[word].update({SPELLING: BrE})
        else:
            word_dict[word].update({SPELLING: AmE})
            logging.debug(word_dict)
        logging.debug(word_dict)
        return word_dict
