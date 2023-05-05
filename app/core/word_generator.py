import random

from random_words import RandomWords


class WordGenerator:
    def __init__(self, user):
        self.user = user

    def generate_next_word(self):
        """
        Randomly retrieves one word for practice from one of the dictionaries
        :return: dictionary containing a word and its definition
        """
        choice_source = self.determine_word_choice_source()
        if 'users_vocabulary' in choice_source:
            users_vocabulary_list = list(self.user.dictionaries.vocabulary.keys())
            word = users_vocabulary_list[random.randrange(0, len(users_vocabulary_list) - 1)]
            word_dict = {word: self.user.dictionaries.vocabulary[word]}
            if self.user.strict_spelling and 'AmE' in word_dict[word].keys():
                word_dict = self.choose_which_spelling(word, word_dict)
        elif 'commonly_misspelled' in choice_source:
            commonly_misspelled_list = list(self.user.dictionaries.commonly_misspelled.keys())
            word = commonly_misspelled_list[random.randrange(0, len(commonly_misspelled_list) - 1)]
            word_dict = {word: self.user.dictionaries.commonly_misspelled[word]}
            if self.user.strict_spelling and 'AmE' in word_dict[word].keys():
                word_dict = self.choose_which_spelling(word, word_dict)
        elif 'common_english' in choice_source:
            common_english_words_list = list(self.user.dictionaries.common_english_words.keys())
            word = common_english_words_list[random.randrange(0, len(common_english_words_list) - 1)]
            word_dict = {word: self.user.dictionaries.common_english_words[word]}
            if self.user.trict_spelling and 'AmE' in word_dict[word].keys():
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
        if len(self.user.dictionaries.vocabulary) > 30:
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
