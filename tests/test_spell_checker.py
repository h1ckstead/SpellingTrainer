import unittest
from unittest.mock import patch

from app.core.session import Session
from app.core.spell_checker import SpellChecker
from app.core.user import User
from core.constants import CORRECT, INCORRECT, SPELLING, AmE, BrE, DEFINITIONS


class TestSpellCheck(unittest.TestCase):
    def setUp(self):
        self.user = User(name="TestSpellCheck", strict_spelling=False, avatar="deer.png")
        self.spell_checker = SpellChecker(self.user)
        self.word_dict = {"Bear": {DEFINITIONS: "a large, heavy mammal that has thick fur and a very short tail.",
                                   SPELLING: AmE}}
        self.session = Session()

    @patch("app.core.spell_checker.SpellChecker.strict_spellcheck")
    def test_strict_spellcheck_called(self, strict_spellcheck):
        self.user.strict_spelling = True
        self.spell_checker.spell_check(self.word_dict, "Bear", self.session)
        strict_spellcheck.assert_called_once()

    @patch("app.core.spell_checker.SpellChecker.soft_spellcheck")
    def test_soft_spellcheck_called(self, soft_spellcheck):
        self.spell_checker.spell_check(self.word_dict, "Bear", self.session)
        soft_spellcheck.assert_called_once()


class TestPrepareData(unittest.TestCase):

    def test_prepare_data(self):
        word_dict = {"Bear": {DEFINITIONS: "a large, heavy mammal that has thick fur and a very short tail."}}
        word, user_word = SpellChecker.prepare_data(word_dict, "bear")
        self.assertEqual(word, user_word)


class TestStrictSpellcheckBritish(unittest.TestCase):
    def setUp(self):
        self.user = User(name="TestStrictSpellcheckBritish", strict_spelling=True, avatar="deer.png")
        self.spell_checker = SpellChecker(self.user)
        self.word_dict = {'Colour': {AmE: 'Color', SPELLING: BrE, DEFINITIONS: {
            'Noun': ['a visual attribute of things that results from the light they emit'
                     ' or transmit or reflect']}}}
        self.session = Session()

    def test_correct_british(self):
        status = self.spell_checker.strict_spellcheck("Colour", self.word_dict, "Colour", self.session)
        self.assertEqual(status, CORRECT)

    def test_incorrect_british(self):
        status = self.spell_checker.strict_spellcheck("Colour", self.word_dict, "Color", self.session)
        self.assertEqual(status, INCORRECT)


class TestStrictSpellcheckAmerican(unittest.TestCase):
    def setUp(self):
        self.user = User(name="TestStrictSpellcheckAmerican", strict_spelling=True, avatar="deer.png")
        self.spell_checker = SpellChecker(self.user)
        self.word_dict = {'Colour': {AmE: 'Color', SPELLING: AmE, DEFINITIONS: {
            'Noun': ['a visual attribute of things that results from the light they emit or transmit or reflect']}}}
        self.session = Session()

    def test_correct_american(self):
        status = self.spell_checker.strict_spellcheck("Colour", self.word_dict, "Color", self.session)
        self.assertEqual(status, CORRECT)

    def test_incorrect_american(self):
        status = self.spell_checker.strict_spellcheck("Colour", self.word_dict, "Colour", self.session)
        self.assertEqual(status, INCORRECT)


class TestSoftSpellcheck(unittest.TestCase):
    def setUp(self):
        self.user = User(name="TestSpellCheck", strict_spelling=False, avatar="bear.png", )
        self.spell_checker = SpellChecker(self.user)
        self.word_dict = {"Bear": {DEFINITIONS: "a large, heavy mammal that has thick fur and a very short tail."}}
        self.session = Session()

    @patch("app.core.spell_checker.SpellChecker.soft_spellcheck_alt_spelling")
    def test_alt_called(self, soft_spellcheck_alt_spelling):
        word_dict = {'Colour': {AmE: 'Color', SPELLING: AmE, DEFINITIONS: {
            'Noun': ['a visual attribute of things that results from the light they emit or transmit or reflect']}}}
        self.spell_checker.soft_spellcheck("Colour", word_dict, "Colour", self.session)
        soft_spellcheck_alt_spelling.assert_called_once()

    def test_soft_spellcheck_correct(self):
        status = self.spell_checker.soft_spellcheck("Bear", self.word_dict, "Bear", self.session)
        self.assertEqual(status, CORRECT)

    def test_soft_spellcheck_incorrect(self):
        status = self.spell_checker.soft_spellcheck("Bear", self.word_dict, "Beer", self.session)
        self.assertEqual(status, INCORRECT)


class TestSoftSpellCheckAltSpelling(unittest.TestCase):
    def setUp(self):
        self.user = User(name="TestSpellCheck", strict_spelling=False, avatar="bear.png")
        self.spell_checker = SpellChecker(self.user)
        self.word_dict = {'Colour': {AmE: 'Color', SPELLING: AmE, DEFINITIONS: {
            'Noun': ['a visual attribute of things that results from the light they emit or transmit or reflect']}}}
        self.session = Session()

    def test_british_correct(self):
        status = self.spell_checker.soft_spellcheck_alt_spelling("Colour", self.word_dict, "Colour", self.session)
        self.assertEqual(status, CORRECT)

    def test_american_correct(self):
        status = self.spell_checker.soft_spellcheck_alt_spelling("Colour", self.word_dict, "Color", self.session)
        self.assertEqual(status, CORRECT)

    def test_incorrect(self):
        status = self.spell_checker.soft_spellcheck_alt_spelling("Colour", self.word_dict, "Bear", self.session)
        self.assertEqual(status, INCORRECT)
