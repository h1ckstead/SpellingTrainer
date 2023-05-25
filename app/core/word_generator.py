import logging
import random

from random_words import RandomWords

from core.constants import BrE, AmE, DEFINITIONS, SPELLING


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
        if choice_source == 'vocabulary':
            try:
                word = random.choice(list(self.user.dictionaries.vocabulary.keys()))
                word_dict = {word: self.user.dictionaries.vocabulary[word]}
            except IndexError:
                self.callback()
                return
        elif choice_source == 'commonly_misspelled':
            word = random.choice(list(self.user.dictionaries.commonly_misspelled.keys()))
            word_dict = {word: self.user.dictionaries.commonly_misspelled[word]}
        elif choice_source == 'common_english':
            word = random.choice(list(self.user.dictionaries.common_english_words.keys()))
            word_dict = {word: self.user.dictionaries.common_english_words[word]}
        else:
            word, word_dict = self.generate_random_word()
        if self.user.strict_spelling and word_dict.get(word, {}).get(AmE):
            word_dict = self.pick_which_spelling(word, word_dict)
        logging.info(word_dict)
        return word_dict

    def generate_random_word(self):
        """
        Uses RandomWords to generate a word with min length of 4.

        :return: dict containing word and definition
        """
        random_words = RandomWords()
        while True:
            word = random_words.random_word(min_letter_count=4).title()
            if not self.is_duplicate(word.title()):
                word_dict = {word: {DEFINITIONS: None}}  # TODO: Think about loading definition in the background
                return word, word_dict

    def is_duplicate(self, word):
        """
        Checks if the word has already been learned or is in the users' vocabulary.

        :param word: str containing a random word
        :return: bool
        """
        if word in self.user.dictionaries.vocabulary.keys() or word in self.user.dictionaries.learned_words.keys():
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
            return 'vocabulary'
        choice_sources = self.get_non_empty_dicts()
        if len(self.user.dictionaries.vocabulary) > 30:
            choice_source = random.choices(['vocabulary', 'random_words'] + choice_sources,
                                           weights=[4, 3, 2, 1], k=1)
        else:
            choice_source = random.choices(['random_words'] + choice_sources,
                                           weights=[4, 3, 1], k=1)
        logging.info(f'Word choice source: {choice_source}')
        return choice_source[0]

    def get_non_empty_dicts(self):
        """
        Checks if commonly_misspelled or common_english still have
        words. If so, they are added to choice_sources.

        :return: list of strings
        """
        choice_sources = []
        if len(self.user.dictionaries.commonly_misspelled) > 0:
            choice_sources.append('commonly_misspelled')
        if len(self.user.dictionaries.common_english_words) > 0:
            choice_sources.append('common_english')
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
