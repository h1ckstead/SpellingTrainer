import unittest

from app.core.user import User
from unittest import mock


class TestWordGeneration(unittest.TestCase):
    def setUp(self):
        self.user = User('TestUserWordsGeneration', 'bunny.png', strict_spelling=False)
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

    @mock.patch("app.core.user.User.determine_word_choice_source")
    def test_commonly_misspelled(self, determine_word_choice_source):
        determine_word_choice_source.return_value = 'commonly_misspelled'
        word_dict = self.user.generate_next_word()
        self.assertIn(list(word_dict.keys())[0], self.user.commonly_misspelled.keys())

    @mock.patch("app.core.user.User.determine_word_choice_source")
    def test_common_english(self, determine_word_choice_source):
        determine_word_choice_source.return_value = 'common_english'
        word_dict = self.user.generate_next_word()
        self.assertIn(list(word_dict.keys())[0], self.user.common_english_words)

    @mock.patch("app.core.user.User.determine_word_choice_source")
    def test_users_vocabulary(self, determine_word_choice_source):
        determine_word_choice_source.return_value = 'users_vocabulary'
        word_dict = self.user.generate_next_word()
        self.assertIn(list(word_dict.keys())[0], self.user.vocabulary)


class TestWordGenerationStrictSpelling(unittest.TestCase):
    def setUp(self):
        self.user = User('TestUserWordsGeneration', 'bunny.png', strict_spelling=True)
        self.user.common_english_words = {
            'Colour': {
                'AmE': 'Color',
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

    @mock.patch("app.core.user.User.choose_which_spelling")
    @mock.patch("random.randrange")
    @mock.patch("app.core.user.User.determine_word_choice_source")
    def test_strict_spelling_word(self, determine_word_choice_source, randrange, choose_which_spelling):
        determine_word_choice_source.return_value = 'common_english'
        randrange.return_value = 1
        self.user.generate_next_word()
        choose_which_spelling.assert_not_called()

    @mock.patch("app.core.user.User.choose_which_spelling")
    @mock.patch("random.randrange")
    @mock.patch("app.core.user.User.determine_word_choice_source")
    def test_strict_spelling_alt_word(self, determine_word_choice_source, randrange, choose_which_spelling):
        determine_word_choice_source.return_value = 'common_english'
        randrange.return_value = 0
        self.user.generate_next_word()
        choose_which_spelling.assert_called_once()

    @mock.patch("random.choice")
    def test_strict_spelling_alt_word_american(self, choice):
        choice.return_value = "Colour"
        result = self.user.choose_which_spelling("Colour", {"Colour": self.user.common_english_words["Colour"]})
        self.assertIn("spelling", result["Colour"].keys())
        self.assertEqual("BrE", result["Colour"]["spelling"])

    @mock.patch("random.choice")
    def test_strict_spelling_alt_word_british(self, choice):
        choice.return_value = "Color"
        result = self.user.choose_which_spelling("Colour", {"Colour": self.user.common_english_words["Colour"]})
        self.assertIn("spelling", result["Colour"].keys())
        self.assertEqual("AmE", result["Colour"]["spelling"])
