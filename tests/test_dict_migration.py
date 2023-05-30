import os
import unittest
from unittest.mock import patch

from core import constants
from core.user import User
from util import helpers
import json


@unittest.skip
class TestDictMigration(unittest.TestCase):
    def setUp(self):
        def load_test_data(filename):
            parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
            relative_path = f'tests/data_for_tests/{filename}'
            full_path = os.path.join(parent_dir, relative_path)
            with open(helpers.get_path(full_path), mode='r') as document:
                return json.load(document)

        vocabulary = load_test_data("migration_vocabulary.json")
        learned_words = load_test_data("migration_learned_words.json")

        user = User(name='TestDictMigration', strict_spelling=False)
        user.dictionaries.vocabulary = vocabulary
        user.dictionaries.learned_words = learned_words
        user.dictionaries.high_priority_words = {"version": 0}
        user.dictionaries.low_priority_words = {"version": 0}
        user.save_progress()

        self.expected_vocabulary = load_test_data("migration_expected_vocab.json")
        self.expected_learned_words = load_test_data("migration_expected_learned_words.json")

        self.high_priority_words = load_test_data("migration_high_priority.json")
        self.low_priority_words = load_test_data("migration_low_priority.json")

        self.expected_high_priority_words = load_test_data("migration_expected_high_priority.json")
        self.expected_low_priority_words = load_test_data("migration_expected_low_priority.json")

    @patch('util.helpers.load_dictionary')
    def test_dict_migration(self, mock_load_dictionary):
        def mock_load_dictionary_impl(name):
            if name == constants.HIGH_PRIORITY_WORDS:
                return self.high_priority_words
            elif name == constants.LOW_PRIORITY_WORDS:
                return self.low_priority_words

        mock_load_dictionary.side_effect = mock_load_dictionary_impl
        saved_data = helpers.load_save()
        helpers.verify_dicts_version(saved_data)
        user = helpers.load_save()["TestDictMigration"]
        self.assertDictEqual(user.dictionaries.vocabulary, self.expected_vocabulary)
        self.assertDictEqual(user.dictionaries.learned_words, self.expected_learned_words)
        self.assertDictEqual(user.dictionaries.high_priority_words, self.expected_high_priority_words)
        self.assertDictEqual(user.dictionaries.low_priority_words, self.expected_low_priority_words)
