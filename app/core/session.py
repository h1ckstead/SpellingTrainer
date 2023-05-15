import logging


class Session:
    def __init__(self):
        self.attempts_correct = 0
        self.attempts_incorrect = 0
        self.learned_words = 0
        self.new_words = 0
        logging.info("New session created")

    @property
    def total_attempts(self):
        return self.attempts_correct + self.attempts_incorrect

    def increment_attempts_correct(self):
        self.attempts_correct += 1
        logging.debug("Session correct attempts +1")

    def increment_attempts_incorrect(self):
        self.attempts_incorrect += 1
        logging.debug("Session incorrect attempts +1")

    def increment_learned_words(self):
        self.learned_words += 1
        logging.debug("Session learned words +1")

    def increment_new_words(self):
        self.new_words += 1
        logging.debug("Session new words +1")
