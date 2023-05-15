class VocabBuilder:
    def __init__(self, user):
        self.user = user

    def manage_vocabulary_based_on_word_status(self, word, word_dict, status, session):
        if status == "Correct":
            if word in self.user.dictionaries.vocabulary.keys():
                if self.user.dictionaries.vocabulary[word]["Times_to_spell"] == 1:
                    self.user.dictionaries.mark_word_as_learned(session)
                else:
                    self.user.dictionaries.decrement_times_to_spell(word)
            else:
                self.user.dictionaries.add_word_to_vocab(word, word_dict, status, session)
            self.user.increment_attempts_correct()
        elif status == "Incorrect":
            if word in self.user.dictionaries.vocabulary.keys():
                self.user.dictionaries.increment_times_to_spell(word)
            else:
                self.user.dictionaries.add_word_to_vocab(word, word_dict, status, session)
            self.user.increment_attempts_incorrect()
        else:
            raise ValueError("Invalid status value. Must be either 'Correct' or 'Incorrect'")
