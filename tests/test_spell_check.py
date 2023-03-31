import unittest
from app.core.user import User
from app.util.spell_check import spell_check, check_word_learned


class TestWordLearned(unittest.TestCase):
    def setUp(self):
        self.user = User('TestUserSpellcheck', 'bear.png')
        self.user.misspelled_dict = {'word1': 0}

    def test_word_learned(self):
        check_word_learned(self.user, 'word1')
        self.assertNotIn('word1', self.user.misspelled_dict)
        self.assertIn('word1', self.user.spelled_ok_lst)


class TestSpellcheck(unittest.TestCase):
    def setUp(self):
        self.user = User('TestUserSpellcheck', 'bear.png')
        self.user.misspelled_dict = {'word1': 10, 'word2': 0, 'another': 1}

    def test_user_word_empty(self):
        self.assertIsNone(spell_check(self.user, 'test_word', ''))

    def test_spelled_ok_word_not_in_misspelled_dict(self):
        spell_check(self.user, 'ok', 'ok')
        self.assertIn('ok', self.user.spelled_ok_lst)

    def test_spelled_ok_word_in_misspelled_dict(self):
        spell_check(self.user, 'word1', 'word1')
        self.assertEqual(9, self.user.misspelled_dict['word1'])

    def test_misspelled_word_not_in_misspelled_dict(self):
        spell_check(self.user, 'word3', 'word')
        self.assertIn('word3', self.user.misspelled_dict)

    def test_misspelled_word_in_misspelled_dict(self):
        spell_check(self.user, 'another', 'word')
        self.assertEqual(2, self.user.misspelled_dict['another'])


class TestAttempts(unittest.TestCase):
    def setUp(self):
        self.user = User('TestUserAttempts', 'bear.png')

    def test_user_word_empty(self):
        spell_check(self.user, 'word', '')
        self.assertEqual(self.user.attempts_correct, 0)
        self.assertEqual(self.user.attempts_incorrect, 0)

    def test_ok_word(self):
        spell_check(self.user, 'word', 'word')
        self.assertEqual(self.user.attempts_correct, 1)
        self.assertEqual(self.user.attempts_incorrect, 0)

    def test_misspelled_word(self):
        spell_check(self.user, 'word', 'world')
        self.assertEqual(self.user.attempts_correct, 0)
        self.assertEqual(self.user.attempts_incorrect, 1)
