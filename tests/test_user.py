import unittest

from app.core.user import User
from app.util.helpers import get_avatars_list


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User(name="TestUser", strict_spelling=False, avatar="bear.png")

    def test_user_total_attempts_property(self):
        user = User(name="TestUserTotalAttempts", strict_spelling=False, avatar="bear.png")
        user.attempts_correct = 5
        user.attempts_incorrect = 2
        self.assertEqual(user.total_attempts, 7)

    def test_edit_username(self):
        self.user.edit_username("TestUserEdited")
        self.assertEqual(self.user.name, "TestUserEdited")

    def test_edit_avatar(self):
        self.user.edit_avatar("bunny.png")
        self.assertEqual(self.user.avatar, "bunny.png")

    def test_toggle_strict_spelling(self):
        self.user.toggle_strict_spelling(True)
        self.assertEqual(self.user.strict_spelling, True)

    def test_increment_attempts_correct(self):
        self.user.increment_attempts_correct()
        self.assertEqual(self.user.attempts_correct, 1)

    def test_increment_attempts_incorrect(self):
        self.user.increment_attempts_incorrect()
        self.assertEqual(self.user.attempts_incorrect, 1)

    def test_set_volume(self):
        self.user.set_volume(0.8)
        self.assertEqual(self.user.volume, 0.8)

    def test_toggle_only_from_vocabulary(self):
        self.user.toggle_only_from_vocabulary(state=True)
        self.assertEqual(self.user.only_from_vocabulary, True)


class UserRandomAvatarTest(unittest.TestCase):
    def test_random_avatar(self):
        user = User(name="TestUserRandomAvatar", strict_spelling=False)
        self.assertIn(user.avatar, get_avatars_list())
