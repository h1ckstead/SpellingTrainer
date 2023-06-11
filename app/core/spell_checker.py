import logging

from core.constants import CORRECT, INCORRECT, BrE, AmE, SPELLING
from core.vocab_builder import VocabBuilder


class SpellChecker:
    def __init__(self, user):
        self.user = user
        self.vocab_builder = VocabBuilder(user)

    def spell_check(self, word_dict, user_word, session):
        """
        Main function for spell checking.

        :param session: Session object
        :param word_dict: dict containing a word and its definition
        :param user_word: str a word user has typed
        :return: str status "Correct" or "Incorrect"
        """
        word, user_word = self.prepare_data(word_dict, user_word)
        logging.debug(f'Reference word: {word}, User word: {user_word}')
        if self.user.strict_spelling and SPELLING in word_dict[word]:
            status = self.strict_spellcheck(word, word_dict, user_word, session)
        else:
            status = self.soft_spellcheck(word, word_dict, user_word, session)
        return status

    @staticmethod
    def prepare_data(word_dict, user_word):
        """
        Prepares words for comparing by formatting user input and retrieving
        the reference word from word_dict.

        :param word_dict: dict containing a word and its definition
        :param user_word: str a word user has typed
        :return: str reference word, str capitalized user word
        """
        word = list(word_dict)[0]
        user_word = user_word.title()
        return word, user_word

    def strict_spellcheck(self, word, word_dict, user_word, session):
        """
        Based on the spelling prompt "BrE/AmE" compares if user word
        matches the appropriate spelling.

        :param session: Session object
        :param word: str reference word
        :param word_dict: dict containing reference word, definition,
        AmE version of the word and Spelling which was asked from the user
        :param user_word: str a word user has typed
        :return: str status "Correct" or "Incorrect"
        """
        word_entry = word_dict[word]
        spelling = word_entry[SPELLING]

        if spelling == BrE and user_word == word:
            status = CORRECT
        elif spelling == AmE and user_word == word_entry[AmE]:
            status = CORRECT
        else:
            status = INCORRECT
        self.vocab_builder.manage_vocabulary_based_on_word_status(word, word_dict, status, session)
        return status

    def soft_spellcheck(self, word, word_dict, user_word, session):
        """
        Soft spellcheck performed for users who have their "strict_spelling"
        attribute set to False. For words with alternative spelling such as
        colour/color both spellings will be considered correct.

        :param session: Session object
        :param word: str reference word
        :param word_dict: dict containing a word and its definition,
        may also contain alternative spelling for some words
        :param user_word: str a word user has typed
        :return: str status "Correct" or "Incorrect"
        """
        if AmE in word_dict[word]:
            status = self.soft_spellcheck_alt_spelling(word=word, user_word=user_word, word_dict=word_dict,
                                                       session=session)
        else:
            if user_word == word:
                status = CORRECT
                self.vocab_builder.manage_vocabulary_based_on_word_status(word=word, word_dict=word_dict,
                                                                          status=status, session=session)
            else:
                status = INCORRECT
                self.vocab_builder.manage_vocabulary_based_on_word_status(word=word, word_dict=word_dict,
                                                                          status=status, session=session)
        return status

    def soft_spellcheck_alt_spelling(self, word, user_word, word_dict, session):
        """
        Checks if user word matches any of the acceptable spellings.

        :param session: Session object
        :param word: str reference word
        :param word_dict: dict containing a word, its definition
        and alternative spelling
        :param user_word: str a word user has typed
        :return:
        """
        words = [word, word_dict[word][AmE]]
        if user_word in words:
            status = CORRECT
            self.vocab_builder.manage_vocabulary_based_on_word_status(word=word, word_dict=word_dict, status=status,
                                                                      session=session)
        else:
            status = INCORRECT
            self.vocab_builder.manage_vocabulary_based_on_word_status(word=word, word_dict=word_dict, status=status,
                                                                      session=session)
        return status
