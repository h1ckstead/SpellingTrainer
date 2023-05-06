import logging
import random

from random_words import RandomWords


class WordGenerator:
    def __init__(self, user):
        self.user = user

    def generate_word(self):
        """
        Retrieves one random word for practice from one of the existing dictionaries or
        generates a random word.

        :return: dictionary containing a word and its definition
        """
        choice_source = self.pick_dictionary()
        if choice_source == 'users_vocabulary':
            users_vocabulary_list = list(self.user.dictionaries.vocabulary.keys())
            word = users_vocabulary_list[random.randrange(0, len(users_vocabulary_list) - 1)]
            word_dict = {word: self.user.dictionaries.vocabulary[word]}
            if self.user.strict_spelling and 'AmE' in word_dict[word].keys():
                word_dict = self.pick_which_spelling(word, word_dict)
        elif choice_source == 'commonly_misspelled':
            commonly_misspelled_list = list(self.user.dictionaries.commonly_misspelled.keys())
            word = commonly_misspelled_list[random.randrange(0, len(commonly_misspelled_list) - 1)]
            word_dict = {word: self.user.dictionaries.commonly_misspelled[word]}
            if self.user.strict_spelling and 'AmE' in word_dict[word].keys():
                word_dict = self.pick_which_spelling(word, word_dict)
        elif choice_source == 'common_english':
            common_english_words_list = list(self.user.dictionaries.common_english_words.keys())
            word = common_english_words_list[random.randrange(0, len(common_english_words_list) - 1)]
            word_dict = {word: self.user.dictionaries.common_english_words[word]}
            if self.user.strict_spelling and 'AmE' in word_dict[word].keys():
                word_dict = self.pick_which_spelling(word, word_dict)
        else:
            word_dict = self.generate_random_word()
        logging.info(word_dict)
        return word_dict

    def generate_random_word(self):
        """
        Uses RandomWords to generate a word with min length of 4.

        :return: dict containing word and definition
        """
        random_words = RandomWords()
        while True:
            word = random_words.random_word(min_letter_count=4)
            if not self.is_duplicate(word.title()):
                word_dict = {word: {"Definition": None}}  # Think about loading definition in the background
                return word_dict

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
        if len(self.user.dictionaries.vocabulary) > 30:
            choice_source = random.choices(['vocabulary', 'commonly_misspelled',
                                            'common_english', 'random_words'],
                                           weights=[4, 3, 2, 1], k=1)
        else:
            choice_source = random.choices(['commonly_misspelled', 'common_english', 'random_words'],
                                           weights=[4, 3, 1], k=1)
        logging.info(f'Word choice source: {choice_source}')
        return choice_source[0]

    @staticmethod
    def pick_which_spelling(word, word_dict):
        """
        Randomly choose British or American spelling for words that have
        different spellings.

        :param word: str British spelling
        :param word_dict: dict containing definitions and American spelling
        :return: original dict with added key Spelling
        """
        word_choice = random.choice([word, word_dict[word]['AmE']])
        if word_choice in word_dict.keys():
            word_dict[word].update({'Spelling': 'BrE'})
        else:
            word_dict[word].update({'Spelling': 'AmE'})
            logging.debug(word_dict)
        logging.debug(word_dict)
        return word_dict
