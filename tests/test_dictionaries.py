import unittest
from unittest.mock import patch

from app.core.dictionaries import Dictionaries
from app.core.session import Session
from app.core.config import TIMES_TO_SPELL_IF_CORRECT, TIMES_TO_SPELL_IF_INCORRECT
from app.core.constants import TIMES_TO_SPELL, CORRECT, INCORRECT, ALREADY_EXISTS, AmE


class LoadDictionaryTest(unittest.TestCase):
    def test_load_dictionary(self):
        commonly_misspelled = Dictionaries.load_dictionary("commonly_misspelled")
        self.assertIn("Embarrassment", commonly_misspelled)

    def test_initialization(self):
        dictionaries = Dictionaries()
        self.assertIsNotNone(dictionaries.commonly_misspelled)
        self.assertIsNotNone(dictionaries.common_english_words)
        self.assertDictEqual(dictionaries.vocabulary, {})
        self.assertDictEqual(dictionaries.learned_words, {})

    def test_dictionary_length(self):
        dictionaries = Dictionaries()
        self.assertEqual(len(dictionaries.commonly_misspelled), 474)
        self.assertEqual(len(dictionaries.common_english_words), 6207)


class VocabularyTest(unittest.TestCase):
    def setUp(self):
        self.vocabulary = {'Advertisement': {
            'times_to_spell': 10,
            'definitions': {
                'Noun': ['a public promotion of some product or service']
            }
        },
            'Appetite': {
                'times_to_spell': 9,
                'definition': {
                    'Noun': ['a feeling of craving something']
                }
            },
        }
        self.word = 'Advertisement'
        self.words = ['Advertisement', 'Appetite']
        self.dictionaries = Dictionaries()
        self.dictionaries.vocabulary.update(self.vocabulary)

    def test_increment_times_to_spell(self):
        self.dictionaries.increment_times_to_spell(self.word)
        self.assertEqual(self.dictionaries.vocabulary[self.word][TIMES_TO_SPELL], 11)

    def test_decrement_times_to_spell(self):
        self.dictionaries.decrement_times_to_spell(self.word)
        self.assertEqual(self.dictionaries.vocabulary[self.word][TIMES_TO_SPELL], 9)

    def test_mark_word_as_learned(self):
        session = Session()
        word_dict = {self.word: self.vocabulary[self.word]}
        self.dictionaries.mark_word_as_learned(self.word, word_dict, session)
        self.assertNotIn(self.word, self.dictionaries.vocabulary)
        self.assertIn(self.word, self.dictionaries.learned_words)
        self.assertEqual(session.learned_words, 1)

    def test_delete_words(self):
        self.dictionaries.delete_words(self.words)
        self.assertNotIn(self.words[0], self.dictionaries.vocabulary)
        self.assertNotIn(self.words[1], self.dictionaries.vocabulary)
        self.assertEqual(len(self.dictionaries.vocabulary), 0)
        self.assertIn(self.words[0], self.dictionaries.learned_words)
        self.assertIn(self.words[1], self.dictionaries.learned_words)
        self.assertEqual(len(self.dictionaries.learned_words), 2)


class WordInDictsTest(unittest.TestCase):
    def setUp(self):
        self.dictionaries = Dictionaries()

    def test_word_in_commonly_misspelled(self):
        exists, dictionary = self.dictionaries.check_word_in_dicts("Questionnaire")
        self.assertTrue(exists)
        self.assertEqual(dictionary, self.dictionaries.commonly_misspelled)

    def test_word_in_common_english_words(self):
        exists, dictionary = self.dictionaries.check_word_in_dicts("Entertainment")
        self.assertTrue(exists)
        self.assertEqual(dictionary, self.dictionaries.common_english_words)

    def test_word_in_vocabulary(self):
        self.dictionaries.vocabulary.update({'VocabAppetite': {
            'times_to_spell': 9,
            'definition': {
                'Noun': ['a feeling of craving something']
            }
        }})
        exists, dictionary = self.dictionaries.check_word_in_dicts("VocabAppetite")
        self.assertTrue(exists)
        self.assertEqual(dictionary, self.dictionaries.vocabulary)

    def test_word_in_learned_words(self):
        self.dictionaries.learned_words.update({'LearnedAdvertisement': {
            'times_to_spell': 10,
            'definitions': {
                'Noun': ['a public promotion of some product or service']
            }
        }})
        exists, dictionary = self.dictionaries.check_word_in_dicts("LearnedAdvertisement")
        self.assertTrue(exists)
        self.assertEqual(dictionary, self.dictionaries.learned_words)

    def test_word_not_in_dicts(self):
        exists, dictionary = self.dictionaries.check_word_in_dicts("Cat")
        self.assertIsNone(exists)
        self.assertIsNone(dictionary)


class SpellcheckTest(unittest.TestCase):
    def setUp(self):
        self.dictionaries = Dictionaries()

    def test_spelled_correctly(self):
        result = self.dictionaries.check_spelling("Correctly")
        self.assertIsNone(result)

    def test_spelled_incorrectly(self):
        result = self.dictionaries.check_spelling("Incorrectky")
        self.assertEqual(result.title(), "Incorrectly")


class AddWordToVocabTest(unittest.TestCase):
    def setUp(self):
        self.dictionaries = Dictionaries()
        self.session = Session()
        self.word_dict = {'Believable': {'definition': {'Adjective': ['capable of being believed']}}}
        self.word = 'Believable'

    def test_word_spelled_correctly(self):
        expected_result = {'Believable': {'definition': {'Adjective': ['capable of being believed']},
                                          TIMES_TO_SPELL: TIMES_TO_SPELL_IF_CORRECT}}
        self.dictionaries.add_word_to_vocab(self.word, self.word_dict, CORRECT, self.session)
        self.assertEqual(self.session.new_words, 1)
        self.assertEqual(expected_result, self.dictionaries.vocabulary)

    def test_word_spelled_incorrectly(self):
        expected_result = {'Believable': {'definition': {'Adjective': ['capable of being believed']},
                                          TIMES_TO_SPELL: TIMES_TO_SPELL_IF_INCORRECT}}
        self.dictionaries.add_word_to_vocab(self.word, self.word_dict, INCORRECT, self.session)
        self.assertEqual(self.session.new_words, 1)
        self.assertEqual(expected_result, self.dictionaries.vocabulary)

    def test_invalid_status(self):
        with self.assertRaises(ValueError) as context:
            self.dictionaries.add_word_to_vocab(self.word, self.word_dict, "Invalid status", self.session)
        self.assertIsInstance(context.exception, ValueError)
        self.assertEqual(str(context.exception),
                         f"Invalid status value. Must be either \"{CORRECT}\" or \"{INCORRECT}\"")


class AddWordToVocabManually(unittest.TestCase):
    def setUp(self):
        self.dictionaries = Dictionaries()

    @patch("app.core.dictionaries.Dictionaries.check_word_in_dicts")
    def test_word_already_in_vocab(self, mock_check_word_in_dicts):
        mock_check_word_in_dicts.return_value = (True, self.dictionaries.vocabulary)
        result = self.dictionaries.add_word_to_vocab_manually("Test")
        self.assertEqual(result, ALREADY_EXISTS)

    def test_alt_word_already_in_vocab(self):
        self.dictionaries.vocabulary.update({"Color": {TIMES_TO_SPELL: 1}})
        expected_vocab = {"Colour": {AmE: "Color", TIMES_TO_SPELL: TIMES_TO_SPELL_IF_INCORRECT}}
        self.dictionaries.add_word_to_vocab_manually("Colour", alternative_spelling="Color")
        self.assertEqual(self.dictionaries.vocabulary, expected_vocab)
        self.assertNotIn("Color", self.dictionaries.vocabulary)

    def test_alt_word_exists_in_common_english(self):
        expected = {"Test": {AmE: "Essential", TIMES_TO_SPELL: TIMES_TO_SPELL_IF_INCORRECT}}
        self.dictionaries.add_word_to_vocab_manually("Test", alternative_spelling="Essential")
        self.assertEqual(self.dictionaries.vocabulary, expected)
        self.assertNotIn("Essential", self.dictionaries.common_english_words)

    def test_alt_word_exists_in_commonly_misspelled(self):
        expected = {"Test": {AmE: "Successful", TIMES_TO_SPELL: TIMES_TO_SPELL_IF_INCORRECT}}
        self.dictionaries.add_word_to_vocab_manually("Test", alternative_spelling="Successful")
        self.assertEqual(self.dictionaries.vocabulary, expected)
        self.assertNotIn("Successful", self.dictionaries.common_english_words)

    def test_alt_word_exists_in_learned(self):
        self.dictionaries.learned_words.update({"AmericanTest": {}})
        expected = {"BritishTest": {AmE: "AmericanTest", TIMES_TO_SPELL: TIMES_TO_SPELL_IF_INCORRECT}}
        self.dictionaries.add_word_to_vocab_manually("BritishTest", alternative_spelling="AmericanTest")
        self.assertEqual(self.dictionaries.vocabulary, expected)
        self.assertNotIn("AmericanTest", self.dictionaries.learned_words)

    def test_add_word_exists_with_double(self):
        expected = {"Essential": {AmE: "TestWord", TIMES_TO_SPELL: TIMES_TO_SPELL_IF_INCORRECT}}
        self.dictionaries.add_word_to_vocab_manually("Essential", alternative_spelling="TestWord")
        self.assertEqual(self.dictionaries.vocabulary, expected)
        self.assertNotIn("Essential", self.dictionaries.common_english_words)

    def test_add_word_double_spelling(self):
        expected = {"BritishTest": {AmE: "AmericanTest", TIMES_TO_SPELL: TIMES_TO_SPELL_IF_INCORRECT}}
        self.dictionaries.add_word_to_vocab_manually("BritishTest", alternative_spelling="AmericanTest")
        self.assertEqual(self.dictionaries.vocabulary, expected)

    def test_add_word_exists_in_common_english(self):
        expected = {"Essential": {'definitions': {'Noun': ['anything indispensable'],
                                                  'Adjective': ['absolutely necessary; vitally necessary',
                                                                'basic and fundamental', 'of the greatest importance',
                                                                'being or relating to or containing the essence of a'
                                                                ' plant etc', 'defining rights and duties as opposed '
                                                                              'to giving the rules by which rights and '
                                                                              'duties are established']},
                                  TIMES_TO_SPELL: TIMES_TO_SPELL_IF_INCORRECT,
                                  }}
        self.dictionaries.add_word_to_vocab_manually("Essential")
        self.assertEqual(self.dictionaries.vocabulary, expected)
        self.assertNotIn("Essential", self.dictionaries.common_english_words)

    def test_add_word_exists_in_commonly_misspelled(self):
        expected = {"Successful": {'definitions': {'Adjective':
                                                       ['having succeeded or being marked by a favorable outcome']},
                                   TIMES_TO_SPELL: TIMES_TO_SPELL_IF_INCORRECT,
                                   }}

        self.dictionaries.add_word_to_vocab_manually("Successful")
        self.assertEqual(self.dictionaries.vocabulary, expected)
        self.assertNotIn("Successful", self.dictionaries.commonly_misspelled)

    def test_add_word_exists_in_learned(self):
        expected = {"TestLearned": {TIMES_TO_SPELL: TIMES_TO_SPELL_IF_INCORRECT}}
        self.dictionaries.learned_words.update({"TestLearned": {}})
        self.dictionaries.add_word_to_vocab_manually("TestLearned")
        self.assertEqual(self.dictionaries.vocabulary, expected)
        self.assertNotIn("TestLearned", self.dictionaries.learned_words)

    def test_add_word(self):
        expected = {"NewWord": {TIMES_TO_SPELL: TIMES_TO_SPELL_IF_INCORRECT}}
        self.dictionaries.add_word_to_vocab_manually("NewWord")
        self.assertEqual(self.dictionaries.vocabulary, expected)
