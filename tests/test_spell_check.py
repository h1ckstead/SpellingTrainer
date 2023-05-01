import unittest
from app.core.user import User


class TestWordLearned(unittest.TestCase):
    def setUp(self):
        self.user = User('TestUserSpellcheck', 'bear.png')
        self.user.vocabulary = {
            'Appetite': {
                'times_to_spell': 0,
                'definition': {
                    'Noun': ['a feeling of craving something']
                     }
            },
            'Advertisement': {
                'times_to_spell': 10,
                'definition': {
                    'Noun': ['a public promotion of some product or service']
                }
            },
        }

    def test_word_learned(self):
        word_dict = {'Appetite': {'times_to_spell': 0, 'definition': {'Noun': ['a feeling of craving something']}}}
        self.user.check_word_learned('Appetite', word_dict)
        self.assertNotIn('Appetite', self.user.vocabulary.keys())
        self.assertIn('Appetite', self.user.learned_words)


class TestSpellcheck(unittest.TestCase):
    def setUp(self):
        self.user = User('TestUserSpellcheck', 'bear.png')
        self.user.vocabulary = {
            'Appetite': {
                'times_to_spell': 9,
                'definition': {
                    'Noun': ['a feeling of craving something']
                }
            },
            'Advertisement': {
                'times_to_spell': 1,
                'definition': {
                    'Noun': ['a public promotion of some product or service']
                }
            },
        }
        self.word_dict = {'Believable': {'definition': {'Adjective': ['capable of being believed']}}}
        self.word_dict2 = {'Appetite': {'times_to_spell': 9,
                                        'definition': {'Noun': ['a feeling of craving something']}}}

    def test_user_word_empty(self):
        self.assertIsNone(self.user.spell_check(self.word_dict, ''))

    def test_spelled_ok_word_not_in_misspelled_dict(self):
        self.user.spell_check(self.word_dict, 'Believable')
        self.assertIn('Believable', self.user.learned_words.keys())
        #  check word is popt from original dict

    def test_spelled_ok_word_in_misspelled_dict(self):
        self.user.spell_check(self.word_dict2, 'Appetite')
        self.assertEqual(self.user.vocabulary['Appetite']['times_to_spell'], 8)

    def test_misspelled_word_not_in_misspelled_dict(self):
        self.user.spell_check(self.word_dict, 'Beliaveble')
        self.assertIn('Believable', self.user.vocabulary.keys())

    def test_misspelled_word_in_misspelled_dict(self):
        word_dict = {'Advertisement': {'times_to_spell': 1,
                                       'definition': {'Noun': ['a public promotion of some product or service']}}}
        self.user.spell_check(word_dict, 'Advertisemend')
        self.assertEqual(self.user.vocabulary['Advertisement']['times_to_spell'], 2)


class TestAttempts(unittest.TestCase):
    def setUp(self):
        self.user = User('TestUserAttempts', 'bear.png')
        self.word_dict = {'Believable': {'definition': {'Adjective': ['capable of being believed']}}}

    def test_user_word_empty(self):
        self.user.spell_check(self.word_dict, '')
        self.assertEqual(self.user.attempts_correct, 0)
        self.assertEqual(self.user.attempts_incorrect, 0)

    def test_ok_word(self):
        self.user.spell_check(self.word_dict, 'Believable')
        self.assertEqual(self.user.attempts_correct, 1)
        self.assertEqual(self.user.attempts_incorrect, 0)

    def test_misspelled_word(self):
        self.user.spell_check(self.word_dict, 'Incorrect')
        self.assertEqual(self.user.attempts_correct, 0)
        self.assertEqual(self.user.attempts_incorrect, 1)
