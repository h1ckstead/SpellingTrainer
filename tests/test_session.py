import unittest
from app.core.session import Session


class TestSession(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = Session()

    def test_total_attempts_property(self):
        session = Session()
        session.attempts_correct = 5
        session.attempts_incorrect = 2
        self.assertEqual(session.total_attempts, 7)

    def test_increment_attempts_correct(self):
        self.session.increment_attempts_correct()
        self.assertEqual(self.session.attempts_correct, 1)

    def test_increment_attempts_incorrect(self):
        self.session.increment_attempts_incorrect()
        self.assertEqual(self.session.attempts_incorrect, 1)

    def test_increment_learned_words(self):
        self.session.increment_learned_words()
        self.assertEqual(self.session.learned_words, 1)

    def test_increment_new_words(self):
        self.session.increment_new_words()
        self.assertEqual(self.session.new_words, 1)
