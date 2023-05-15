import unittest
from app.core.user import User
from unittest import mock


class TestWordLearned(unittest.TestCase):
    def setUp(self):
        self.user = User('TestUserSpellcheck', 'bear.png', strict_spelling=True)
        self.user.vocabulary = {
            'Colour': {
                'AmE': 'Color',
                'spelling': 'AmE',
                'times_to_spell': 0,
                'definition': {
                    'Noun': ['a visual attribute of things that results from the light they emit'
                             ' or transmit or reflect']
                }
            }
        }

    def test_word_learned(self):
        self.user.check_word_learned('Colour', dict({'Colour': self.user.vocabulary['Colour']}))
        self.assertNotIn('Colour', self.user.vocabulary.keys())
        self.assertIn('Colour', self.user.learned_words)


class TestStrictSpellCheck(unittest.TestCase):
    def setUp(self):
        self.user = User('TestUserSpellcheck', 'bear.png', strict_spelling=True)
        self.user.common_english_words = {
            'Colour': {
                'AmE': 'Color',
                'spelling': 'AmE',
                'definition': {
                    'Noun': ['a visual attribute of things that results from the light they emit'
                             ' or transmit or reflect']
                }
            },
            'Appetite': {
                'times_to_spell': 0,
                'definition': {
                    'Noun': ['a feeling of craving something']
                }
            }
        }
        self.word_dict = {'Believable': {'definition': {'Adjective': ['capable of being believed']}}}

    def test_user_word_empty(self):
        self.assertIsNone(self.user.spell_check(self.word_dict, ''))

    @mock.patch("app.core.user.User.strict_spellcheck")
    def test_strict_spellcheck_called(self, strict_spellcheck):
        word_dict = {'Colour': self.user.common_english_words['Colour']}
        self.user.spell_check(word_dict, 'Colour')
        strict_spellcheck.assert_called_once()

    @mock.patch("app.core.user.User.strict_spellcheck")
    def test_strict_spellcheck_not_called(self, strict_spellcheck):
        self.user.spell_check(self.word_dict, 'Believable')
        strict_spellcheck.assert_not_called()

    def test_spelled_ok_british(self):
        self.user.common_english_words['Colour'].update({'spelling': 'BrE'})
        word_dict = {'Colour': self.user.common_english_words['Colour']}
        status = self.user.strict_spellcheck('Colour', word_dict, 'Colour')
        self.assertEqual('correct', status)

    def test_spelled_ok_american(self):
        word_dict = {'Colour': self.user.common_english_words['Colour']}
        status = self.user.strict_spellcheck('Colour', word_dict, 'Color')
        self.assertEqual('correct', status)

    def test_spelled_incorrect_british(self):
        self.user.common_english_words['Colour'].update({'spelling': 'BrE'})
        word_dict = {'Colour': self.user.common_english_words['Colour']}
        status = self.user.strict_spellcheck('Colour', word_dict, 'Color')
        self.assertEqual('incorrect', status)

    def test_spelled_incorrect_american(self):
        word_dict = {'Colour': self.user.common_english_words['Colour']}
        status = self.user.strict_spellcheck('Colour', word_dict, 'Colour')
        self.assertEqual('incorrect', status)

    def test_spelled_ok_word_not_in_vocabulary(self):
        word_dict = {'Colour': self.user.common_english_words['Colour']}
        self.user.spell_check(word_dict, 'Color')
        self.assertIn('Colour', self.user.learned_words.keys())
