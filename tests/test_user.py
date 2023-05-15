import unittest
from app.core.user import User


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User("TestUser", "bear.png", strict_spelling=False)

    def test_user_total_attempts_property(self):
        user = User("TestUserTotalAttempts", "bear.png", strict_spelling=False)
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
