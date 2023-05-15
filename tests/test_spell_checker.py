import unittest
from app.core.spell_checker import SpellChecker
from app.core.user import User
from unittest.mock import patch

CORRECT = "Correct"
INCORRECT = "Incorrect"


class TestSpellCheck(unittest.TestCase):
    def setUp(self):
        self.user = User("TestSpellCheck", "deer.png", strict_spelling=False)
        self.spell_checker = SpellChecker(self.user)
        self.word_dict = {"Bear": {"Definition": "a large, heavy mammal that has thick fur and a very short tail.",
                                   'Spelling': 'AmE'}}

    @patch("app.core.spell_checker.SpellChecker.strict_spellcheck")
    def test_strict_spellcheck_called(self, strict_spellcheck):
        self.user.strict_spelling = True
        self.spell_checker.spell_check(self.word_dict, "Bear")
        strict_spellcheck.assert_called_once()

    @patch("app.core.spell_checker.SpellChecker.soft_spellcheck")
    def test_soft_spellcheck_called(self, soft_spellcheck):
        self.spell_checker.spell_check(self.word_dict, "Bear")
        soft_spellcheck.assert_called_once()

    # TODO: More through end to end spell checks


class TestPrepareData(unittest.TestCase):

    def test_prepare_data(self):
        word_dict = {"Bear": {"Definition": "a large, heavy mammal that has thick fur and a very short tail."}}
        word, user_word = SpellChecker.prepare_data(word_dict, "bear")
        self.assertEqual(word, user_word)


class TestStrictSpellcheckBritish(unittest.TestCase):
    def setUp(self):
        self.user = User("TestStrictSpellcheckBritish", "deer.png", strict_spelling=True)
        self.spell_checker = SpellChecker(self.user)
        self.word_dict = {'Colour': {'AmE': 'Color', 'Spelling': 'BrE', 'Definition': {
            'Noun': ['a visual attribute of things that results from the light they emit'
                     ' or transmit or reflect']}}}

    def test_correct_british(self):
        status = self.spell_checker.strict_spellcheck("Colour", self.word_dict, "Colour")
        self.assertEqual(status, CORRECT)

    def test_incorrect_british(self):
        status = self.spell_checker.strict_spellcheck("Colour", self.word_dict, "Color")
        self.assertEqual(status, INCORRECT)


class TestStrictSpellcheckAmerican(unittest.TestCase):
    def setUp(self):
        self.user = User("TestStrictSpellcheckAmerican", "deer.png", strict_spelling=True)
        self.spell_checker = SpellChecker(self.user)
        self.word_dict = {'Colour': {'AmE': 'Color', 'Spelling': 'AmE', 'Definition': {
            'Noun': ['a visual attribute of things that results from the light they emit or transmit or reflect']}}}

    def test_correct_american(self):
        status = self.spell_checker.strict_spellcheck("Colour", self.word_dict, "Color")
        self.assertEqual(status, CORRECT)

    def test_incorrect_american(self):
        status = self.spell_checker.strict_spellcheck("Colour", self.word_dict, "Colour")
        self.assertEqual(status, INCORRECT)


class TestSoftSpellcheck(unittest.TestCase):
    def setUp(self):
        self.user = User("TestSpellCheck", "bear.png", strict_spelling=False)
        self.spell_checker = SpellChecker(self.user)
        self.word_dict = {"Bear": {"Definition": "a large, heavy mammal that has thick fur and a very short tail."}}

    @patch("app.core.spell_checker.SpellChecker.soft_spellcheck_alt_spelling")
    def test_alt_called(self, soft_spellcheck_alt_spelling):
        word_dict = {'Colour': {'AmE': 'Color', 'Spelling': 'AmE', 'Definition': {
            'Noun': ['a visual attribute of things that results from the light they emit or transmit or reflect']}}}
        self.spell_checker.soft_spellcheck("Colour", word_dict, "Colour")
        soft_spellcheck_alt_spelling.assert_called_once()

    def test_soft_spellcheck_correct(self):
        status = self.spell_checker.soft_spellcheck("Bear", self.word_dict, "Bear")
        self.assertEqual(status, CORRECT)

    def test_soft_spellcheck_incorrect(self):
        status = self.spell_checker.soft_spellcheck("Bear", self.word_dict, "Beer")
        self.assertEqual(status, INCORRECT)


class TestSoftSpellCheckAltSpelling(unittest.TestCase):
    def setUp(self):
        self.user = User("TestSpellCheck", "bear.png", strict_spelling=False)
        self.spell_checker = SpellChecker(self.user)
        self.word_dict = {'Colour': {'AmE': 'Color', 'Spelling': 'AmE', 'Definition': {
            'Noun': ['a visual attribute of things that results from the light they emit or transmit or reflect']}}}

    def test_british_correct(self):
        status = self.spell_checker.soft_spellcheck_alt_spelling("Colour", self.word_dict, "Colour")
        self.assertEqual(status, CORRECT)

    def test_american_correct(self):
        status = self.spell_checker.soft_spellcheck_alt_spelling("Colour", self.word_dict, "Color")
        self.assertEqual(status, CORRECT)

    def test_incorrect(self):
        status = self.spell_checker.soft_spellcheck_alt_spelling("Colour", self.word_dict, "Bear")
        self.assertEqual(status, INCORRECT)
