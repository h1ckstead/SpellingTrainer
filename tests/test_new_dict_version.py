import unittest
from util import helpers
from core.user import User
from unittest.mock import patch
from core.constants import HIGH_PRIORITY_WORDS, LOW_PRIORITY_WORDS
from core import config
from unittest.mock import ANY


class TestRemoveDuplicates(unittest.TestCase):
    def setUp(self):
        self.to_remove_from = {
            "Accelerate": {
                "definitions": {
                    "Verb": [
                        "move faster",
                        "cause to move faster"
                    ]
                }
            },
            "Harmless": {
                "definitions": {
                    "Adjective": [
                        "not causing or capable of causing harm"
                    ]
                }
            },
        }

    def test_all_matching_keys(self):
        model = self.to_remove_from
        result = helpers.remove_duplicates(self.to_remove_from, model)
        self.assertDictEqual(result, {})

    def test_some_matching_keys(self):
        model = {
            "Harmless": {
                "definitions": {
                    "Adjective": [
                        "not causing or capable of causing harm"
                    ]
                }
            },
        }
        result = helpers.remove_duplicates(self.to_remove_from, model)
        self.assertNotIn("Harmless", result)

    def test_new_definition(self):
        model = {
            "Harmless": {
                "definitions": {
                    "Adjective": [
                        "old definition",
                        "invalid definition"
                    ]
                }
            },
        }
        result = helpers.remove_duplicates(self.to_remove_from, model)
        self.assertNotIn("Harmless", result)
        self.assertEqual(model["Harmless"]["definitions"]["Adjective"], ["not causing or capable of causing harm"])

    def test_times_to_spell_not_deleted(self):
        model = {
            "Harmless": {
                "times_to_spell": 4,
                "definitions": {
                    "Adjective": [
                        "not causing or capable of causing harm"
                    ]
                }
            },
        }
        result = helpers.remove_duplicates(self.to_remove_from, model)
        self.assertNotIn("Harmless", result)
        self.assertIn("times_to_spell", model["Harmless"])

    def test_alt_spelling_added(self):
        self.to_remove_from["Harmless"]["AmE"] = "American spelling"
        model = {
            "Harmless": {
                "times_to_spell": 4,
                "definitions": {
                    "Adjective": [
                        "not causing or capable of causing harm"
                    ]
                }
            },
        }
        result = helpers.remove_duplicates(self.to_remove_from, model)
        self.assertNotIn("Harmless", result)
        self.assertIn("AmE", model["Harmless"])

    def test_alt_spelling_removed(self):
        model = {
            "Harmless": {
                "AmE": "Delete",
                "definitions": {
                    "Adjective": [
                        "not causing or capable of causing harm"
                    ]
                }
            },
        }
        result = helpers.remove_duplicates(self.to_remove_from, model)
        self.assertNotIn("Harmless", result)
        self.assertNotIn("AmE", model["Harmless"])


class TestVerifyDictsVersion(unittest.TestCase):
    def setUp(self):
        self.user = User(name="TestNewDictVersion", strict_spelling=False)

    @patch("util.helpers.update_user_dict")
    def test_high_priority_words_stale(self, mock_update_user_dict):
        self.user.dictionaries.low_priority_words["version"] = config.LOW_PRIORITY_DICT_VERSION
        self.user.dictionaries.high_priority_words["version"] = 0
        self.user.save_progress()
        save_data = helpers.load_save()
        helpers.verify_dicts_version(users=save_data["users"], last_user=self.user)
        mock_update_user_dict.assert_called_once_with(ANY, to_update=HIGH_PRIORITY_WORDS)

    @patch("util.helpers.update_user_dict")
    def test_low_priority_words_stale(self, mock_update_user_dict):
        self.user.dictionaries.high_priority_words["version"] = config.HIGH_PRIORITY_DICT_VERSION
        self.user.dictionaries.low_priority_words["version"] = 0
        self.user.save_progress()
        save_data = helpers.load_save()
        helpers.verify_dicts_version(users=save_data["users"], last_user=self.user)
        mock_update_user_dict.assert_called_once_with(ANY, to_update=LOW_PRIORITY_WORDS)

    @patch("util.helpers.update_user_dict")
    def test_both_dictionaries_stale(self, mock_update_user_dict):
        self.user.dictionaries.high_priority_words["version"] = 0
        self.user.dictionaries.low_priority_words["version"] = 0
        self.user.save_progress()
        save_data = helpers.load_save()
        helpers.verify_dicts_version(users=save_data["users"], last_user=self.user)
        mock_update_user_dict.assert_called()
        assert mock_update_user_dict.call_count == 2

    @patch("util.helpers.update_user_dict")
    def test_neither_dictionaries_stale(self, mock_update_user_dict):
        save_data = helpers.load_save()
        helpers.verify_dicts_version(users=save_data["users"], last_user=self.user)
        mock_update_user_dict.assert_not_called()


class TestUpdateUserDicts(unittest.TestCase):
    def setUp(self):
        self.user = User(name="TestUpdateUserDicts", strict_spelling=False)
        self.users = {self.user.name: self.user}

    def test_empty_vocab_and_learned(self):
        expected_high_priority_words = helpers.load_dictionary(HIGH_PRIORITY_WORDS)
        expected_low_priority_words = helpers.load_dictionary(LOW_PRIORITY_WORDS)
        self.user.dictionaries.high_priority_words = {"old_data"}
        self.user.dictionaries.low_priority_words = {"old_data"}
        new_dicts = [HIGH_PRIORITY_WORDS, LOW_PRIORITY_WORDS]
        for to_update in new_dicts:
            helpers.update_user_dict(self.users, to_update=to_update)
        self.assertDictEqual(self.user.dictionaries.high_priority_words, expected_high_priority_words)
        self.assertDictEqual(self.user.dictionaries.low_priority_words, expected_low_priority_words)

    @patch("core.user.User.save_progress")
    @patch("util.helpers.remove_duplicates")
    def test_empty_vocab_update_high_priority(self, mock_remove_duplicates, mock_save_progress):
        expected_to_remove_from = helpers.load_dictionary(HIGH_PRIORITY_WORDS)["data"]
        self.user.dictionaries.learned_words = {"some_data"}
        helpers.update_user_dict(self.users, to_update=HIGH_PRIORITY_WORDS)
        mock_remove_duplicates.assert_called_once_with(to_remove_from=expected_to_remove_from, model={"some_data"})

    @patch("core.user.User.save_progress")
    @patch("util.helpers.remove_duplicates")
    def test_empty_vocab_update_low_priority(self, mock_remove_duplicates, mock_save_progress):
        expected_to_remove_from = helpers.load_dictionary(LOW_PRIORITY_WORDS)["data"]
        self.user.dictionaries.learned_words = {"some_data"}
        helpers.update_user_dict(self.users, to_update=LOW_PRIORITY_WORDS)
        mock_remove_duplicates.assert_called_once_with(to_remove_from=expected_to_remove_from, model={"some_data"})

    @patch("core.user.User.save_progress")
    @patch("util.helpers.remove_duplicates")
    def test_empty_learned_update_high_priority(self, mock_remove_duplicates, mock_save_progress):
        expected_to_remove_from = helpers.load_dictionary(HIGH_PRIORITY_WORDS)["data"]
        self.user.dictionaries.vocabulary = {"some_data"}
        helpers.update_user_dict(self.users, to_update=HIGH_PRIORITY_WORDS)
        mock_remove_duplicates.assert_called_once_with(to_remove_from=expected_to_remove_from, model={"some_data"})

    @patch("core.user.User.save_progress")
    @patch("util.helpers.remove_duplicates")
    def test_empty_learned_update_low_priority(self, mock_remove_duplicates, mock_save_progress):
        expected_to_remove_from = helpers.load_dictionary(LOW_PRIORITY_WORDS)["data"]
        self.user.dictionaries.vocabulary = {"some_data"}
        helpers.update_user_dict(self.users, to_update=LOW_PRIORITY_WORDS)
        mock_remove_duplicates.assert_called_once_with(to_remove_from=expected_to_remove_from, model={"some_data"})
