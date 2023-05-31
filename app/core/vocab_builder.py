from core.constants import CORRECT, INCORRECT, TIMES_TO_SPELL


class VocabBuilder:
    def __init__(self, user):
        self.user = user

    def manage_vocabulary_based_on_word_status(self, word, word_dict, status, session):
        if status == CORRECT:
            word_entry = self.user.dictionaries.vocabulary.get(word)
            if word_entry:
                if word_entry[TIMES_TO_SPELL] == 1:
                    self.user.dictionaries.mark_word_as_learned(word, word_dict, session)
                else:
                    self.user.dictionaries.decrement_times_to_spell(word)
            else:
                self.user.dictionaries.add_word_to_vocab(word, word_dict, status, session)
            self.user.increment_attempts_correct()
        elif status == INCORRECT:
            word_entry = self.user.dictionaries.vocabulary.get(word)
            if word_entry:
                self.user.dictionaries.increment_times_to_spell(word)
            else:
                self.user.dictionaries.add_word_to_vocab(word, word_dict, status, session)
            self.user.increment_attempts_incorrect()
        else:
            raise ValueError(f"Invalid status value. Must be either {CORRECT} or {INCORRECT}")
