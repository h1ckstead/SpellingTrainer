import config


class SpellChecker:
    def __init__(self, user):
        self.user = user

    def spell_check(self, word_dict, user_word):
        word, user_word = self.prepare_data(word_dict, user_word)
        if user_word == '':
            status = None
        elif self.user.strict_spelling and "spelling" in word_dict[word].keys():
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
            if word in self.user.dictionaries.vocabulary.keys():
                self.user.dictionaries.vocabulary[word]["times_to_spell"] -= 1
                self.user.attempts_correct += 1
                self.check_word_learned(word, word_dict)
            else:
                self.user.dictionaries.learned_words.update(word_dict)
                self.pop_word_from_dictionary(word)
                self.user.attempts_correct += 1
        elif status == 'incorrect':
            if word in self.user.dictionaries.vocabulary.keys():
                self.user.dictionaries.vocabulary[word]["times_to_spell"] += 1
                self.user.attempts_incorrect += 1
            else:
                word_dict[word].update({"times_to_spell": config.ATTEMPTS_TO_LEARN_WORD})
                self.user.dictionaries.vocabulary.update(word_dict)
                self.pop_word_from_dictionary(word)
                self.user.attempts_incorrect += 1
        else:
            raise Exception("Unknown status")

    def pop_word_from_dictionary(self, word):
        if word in self.user.dictionaries.commonly_misspelled.keys():
            self.user.dictionaries.commonly_misspelled.pop(word)
        elif word in self.user.dictionaries.common_english_words.keys():
            self.user.dictionaries.common_english_words.pop(word)

    def check_word_learned(self, word, word_dict):
        """
        Checks if number of attempts is 0 which means the word is considered
        to be learned. Removes learned word from misspelled_dict and puts it
        into vocabulary_lst
        :param word: str
        :param word_dict: dict
        :return:
        """
        if self.user.dictionaries.vocabulary[word]["times_to_spell"] == 0:
            self.user.dictionaries.vocabulary.pop(word)
            self.user.dictionaries.learned_words.update(word_dict)
