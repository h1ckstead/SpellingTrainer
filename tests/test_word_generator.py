import unittest
from unittest.mock import patch

from random_words import RandomWords

from app.core.user import User
from app.core.word_generator import WordGenerator
from core.constants import SPELLING, AmE, BrE, DEFINITIONS, TIMES_TO_SPELL


class TestPickSpelling(unittest.TestCase):
    def setUp(self):
        self.word_dict = {'Colour': {AmE: 'Color', DEFINITIONS: {
            'Noun': ['a visual attribute of things that results from the light they emit or transmit or reflect']}}}

    @patch("random.choice", return_value='Colour')
    def test_pick_british_spelling(self, mock_choice):
        expected_result = {'Colour': {AmE: 'Color', DEFINITIONS: {
            'Noun': ['a visual attribute of things that results from the light they emit or transmit or reflect']},
                                      SPELLING: BrE}}
        result = WordGenerator.pick_which_spelling('Colour', self.word_dict)
        self.assertEqual(result, expected_result)

    @patch("random.choice", return_value='Color')
    def test_pick_american_spelling(self, mock_choice):
        expected_result = {'Colour': {AmE: 'Color', DEFINITIONS: {
            'Noun': ['a visual attribute of things that results from the light they emit or transmit or reflect']},
                                      SPELLING: AmE}}
        result = WordGenerator.pick_which_spelling('Colour', self.word_dict)
        self.assertEqual(result, expected_result)


class TestPickDictionary(unittest.TestCase):
    def setUp(self):
        self.user = User(name='TestPickDictionary', strict_spelling=False, avatar='dog.png')
        self.word_generator = WordGenerator(self.user, callback=None)

    def test_pick_dictionary_with_few_vocab(self):
        self.user.dictionaries.vocabulary = {"Dog": {DEFINITIONS: []}, "Cat": {DEFINITIONS: []}}
        choice_source = self.word_generator.pick_dictionary()
        self.assertIn(choice_source, ['commonly_misspelled', 'common_english', 'random_words'])

    def test_choose_dictionary_with_many_vocab(self):
        random_words = RandomWords()
        random_key = random_words.random_words(count=31)
        for k in random_key:
            self.user.dictionaries.vocabulary.update({f"{k}": {DEFINITIONS: []}})
        choice_source = self.word_generator.pick_dictionary()
        self.assertIn(choice_source, ['vocabulary', 'commonly_misspelled', 'common_english', 'random_words'])

    def test_choose_dictionary_probabilities(self):
        with patch('random.choices', side_effect=[['commonly_misspelled'], ['common_english'], ['random_words']]):
            results = [self.word_generator.pick_dictionary() for _ in range(3)]
        self.assertAlmostEqual(results.count('commonly_misspelled') / len(results), 0.44, delta=0.2)
        self.assertAlmostEqual(results.count('common_english') / len(results), 0.33, delta=0.2)
        self.assertAlmostEqual(results.count('random_words') / len(results), 0.22, delta=0.2)

    def test_choose_dictionary_probabilities_with_vocab(self):
        with patch('random.choices', side_effect=[['vocabulary'], ['commonly_misspelled'], ['common_english'],
                                                  ['random_words']]):
            results = [self.word_generator.pick_dictionary() for _ in range(4)]
        self.assertAlmostEqual(results.count('commonly_misspelled') / len(results), 0.44, delta=0.2)
        self.assertAlmostEqual(results.count('common_english') / len(results), 0.33, delta=0.2)
        self.assertAlmostEqual(results.count('random_words') / len(results), 0.22, delta=0.2)
        self.assertAlmostEqual(results.count('random_words') / len(results), 0.11, delta=0.2)


class TestIsDuplicate(unittest.TestCase):
    def setUp(self):
        self.user = User(name="TestIsDuplicate", strict_spelling=False)
        self.word_generator = WordGenerator(self.user, callback=None)

    def test_word_is_duplicate_vocabulary(self):
        self.user.dictionaries.vocabulary.update({"Cat": {DEFINITIONS: []}})
        is_duplicate = self.word_generator.is_duplicate("Cat")
        self.assertTrue(is_duplicate)

    def test_word_is_duplicate_learned(self):
        self.user.dictionaries.learned_words.update({"Dog": {DEFINITIONS: []}})
        is_duplicate = self.word_generator.is_duplicate("Dog")
        self.assertTrue(is_duplicate)

    def test_word_is_not_duplicate(self):
        is_duplicate = self.word_generator.is_duplicate("Orca")
        self.assertFalse(is_duplicate)


class TestWordGenerator(unittest.TestCase):
    def setUp(self):
        self.user = User(name='TestWordGeneration', strict_spelling=False)
        self.user.dictionaries.vocabulary = {
            'Appetite': {
                TIMES_TO_SPELL: 0,
                DEFINITIONS: {
                    'Noun': ['a feeling of craving something']
                     }
            },
            'Advertisement': {
                TIMES_TO_SPELL: 10,
                DEFINITIONS: {
                    'Noun': ['a public promotion of some product or service']
                }
            },
        }
        self.word_generator = WordGenerator(self.user, callback=None)

    @patch("app.core.word_generator.WordGenerator.pick_dictionary", return_value='commonly_misspelled')
    def test_commonly_misspelled(self, mock_pick_dictionary):
        word_dict = self.word_generator.generate_word()
        self.assertIn(list(word_dict.keys())[0], self.user.dictionaries.commonly_misspelled.keys())

    @patch("app.core.word_generator.WordGenerator.pick_dictionary", return_value='common_english')
    def test_common_english(self, mock_pick_dictionary):
        word_dict = self.word_generator.generate_word()
        self.assertIn(list(word_dict.keys())[0], self.user.dictionaries.common_english_words)

    @patch("app.core.word_generator.WordGenerator.pick_dictionary", return_value='vocabulary')
    def test_users_vocabulary(self, mock_pick_dictionary):
        word_dict = self.word_generator.generate_word()
        self.assertIn(list(word_dict.keys())[0], self.user.dictionaries.vocabulary)

    @patch("app.core.word_generator.WordGenerator.pick_dictionary", return_value='random')
    def test_random_word(self, pick_dictionary):
        word_dict = self.word_generator.generate_word()
        word = list(word_dict.keys())[0]
        self.assertTrue(len(word) >= 4)
        self.assertTrue(word.istitle())


class TestWordGeneratorStrictSpelling(unittest.TestCase):
    def setUp(self):
        self.user = User('TestWordGeneratorStrictSpelling', strict_spelling=True)
        self.user.dictionaries.common_english_words = {
            'Colour': {
                AmE: 'Color',
                DEFINITIONS: {
                    'Noun': ['a visual attribute of things that results from the light they emit'
                             ' or transmit or reflect']
                }
            },
            'Appetite': {
                TIMES_TO_SPELL: 0,
                DEFINITIONS: {
                    'Noun': ['a feeling of craving something']
                     }
            }
        }
        self.word_generator = WordGenerator(self.user, callback=None)

    @patch("app.core.word_generator.WordGenerator.pick_which_spelling")
    @patch("random.choice", return_value="Appetite")
    @patch("app.core.word_generator.WordGenerator.pick_dictionary", return_value='common_english')
    def test_strict_spelling_word(self, mock_pick_dictionary, mock_randrange, pick_which_spelling):
        self.word_generator.generate_word()
        pick_which_spelling.assert_not_called()

    @patch("app.core.word_generator.WordGenerator.pick_which_spelling")
    @patch("random.choice", return_value="Colour")
    @patch("app.core.word_generator.WordGenerator.pick_dictionary", return_value='common_english')
    def test_strict_spelling_alt_word(self, mock_pick_dictionary, mock_randrange, pick_which_spelling):
        self.word_generator.generate_word()
        pick_which_spelling.assert_called_once()

    @patch("random.choice", return_value='Colour')
    def test_strict_spelling_alt_word_american(self, mock_choice):
        result = self.word_generator.pick_which_spelling(
            "Colour", {"Colour": self.user.dictionaries.common_english_words["Colour"]})
        self.assertIn(SPELLING, result["Colour"].keys())
        self.assertEqual(BrE, result["Colour"][SPELLING])

    @patch("random.choice", return_value='Color')
    def test_strict_spelling_alt_word_british(self, mock_choice):
        result = self.word_generator.pick_which_spelling(
            "Colour", {"Colour": self.user.dictionaries.common_english_words["Colour"]})
        self.assertIn(SPELLING, result["Colour"].keys())
        self.assertEqual(AmE, result["Colour"][SPELLING])


class OnlyVocabularyTest(unittest.TestCase):
    def setUp(self):
        self.user = User('TestWordGeneratorStrictSpelling', strict_spelling=False)
        self.user.only_from_vocabulary = True
        self.word_generator = WordGenerator(self.user, callback=None)

    def test_word_only_from_vocab(self):
        self.user.dictionaries.vocabulary.update({"Dog": {DEFINITIONS: []}})
        result = self.word_generator.generate_word()
        self.assertEqual(result, self.user.dictionaries.vocabulary)

    def test_word_empty_vocab(self):
        instance = self.word_generator
        with patch.object(instance, "callback") as mock_callback:
            instance.generate_word()
        mock_callback.assert_called_once()
