
"""Unit tests for the User model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from spendingtrackers.models import User


class UserModelTestCase(TestCase):

    # Set Up a user with valid information.
    def setUp(self):
        self.user = User.objects.create_user(
            first_name = 'John',
            last_name = 'Doe',
            username = 'johndoe@example.org',
            currency = "£",
            pin = "123",
        )

    def test_valid_user(self):
        self._assert_user_is_valid()


    # Functions:
    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid.')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def _create_second_user(self):
        user = User.objects.create_user(
            first_name = 'Jane',
            last_name = 'Doe',
            username = 'janedoe@example.org',
            currency = "£",
            pin = "345",
        )
        return user


    # Username Tests:
    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        another_user = self._create_second_user()
        self.user.username = another_user.username
        self._assert_user_is_invalid()

    def test_username_email_must_contain_username(self):
        self.user.username = '@example.org'
        self._assert_user_is_invalid()

    def test_username_email_must_contain_an_at_symbol(self):
        self.user.username = 'johndoe.example.org'
        self._assert_user_is_invalid()

    def test_username_email_cannot_contain_more_than_one_at_symbol(self):
        self.user.username = 'johndoe@@example.org'
        self._assert_user_is_invalid()

    def test_username_email_must_contain_a_domain(self):
        self.user.username = 'johndoe@example'
        self._assert_user_is_invalid()

    def test_username_email_must_contain_a_domain_name(self):
        self.user.username = 'johndoe@.com'
        self._assert_user_is_invalid()


    # First Name Tests:
    def test_first_name_cannot_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_donnot_need_to_be_unique(self):
        another_user = self._create_second_user()
        self.user.first_name = another_user.first_name
        self._assert_user_is_valid()

    def test_first_name_can_be_50_characters_long(self):
        self.user.first_name = 'x'*50
        self._assert_user_is_valid()

    def test_first_name_cannot_be_over_50_characters_long(self):
        self.user.first_name = 'x'*51
        self._assert_user_is_invalid()


    # Last Name Tests:
    def test_last_name_cannot_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_donot_need_to_be_unique(self):
        another_user = self._create_second_user()
        self.user.last_name = another_user.last_name
        self._assert_user_is_valid()

    def test_last_name_can_be_50_characters_long(self):
        self.user.last_name = 'x'*50
        self._assert_user_is_valid()

    def test_last_name_cannot_be_over_50_characters_long(self):
        self.user.last_name = 'x'*51
        self._assert_user_is_invalid()


    # Currency Tests:
    def test_currency_cannot_be_blank(self):
        self.user.currency = ''
        self._assert_user_is_invalid()

    def test_currency_donot_need_to_be_unique(self):
        another_user = self._create_second_user()
        self.user.currency = another_user.currency
        self._assert_user_is_valid()

    def test_currency_can_be_1_character_long(self):
        self.user.currency = '$'
        self._assert_user_is_valid()

    def test_currency_cannot_be_over_1_character_long(self):
        self.user.currency = '$$'
        self._assert_user_is_invalid()

    def test_currency_can_be_pounds(self):
        self.user.currency = '£'
        self._assert_user_is_valid()

    def test_currency_can_be_dollars(self):
        self.user.currency = '$'
        self._assert_user_is_valid()

    def test_currency_can_be_euros(self):
        self.user.currency = '€'
        self._assert_user_is_valid()

    def test_currency_can_be_rupees(self):
        self.user.currency = '₹'
        self._assert_user_is_valid()

    def test_currency_can_be_yuan(self):
        self.user.currency = '¥'
        self._assert_user_is_valid()

    def test_currency_cannot_be_any_others(self):
        self.user.currency = '!'
        self._assert_user_is_invalid()

    
    def test_pin_cannot_be_blank(self):
        self.user.pin = ''
        self._assert_user_is_invalid()

    def test_pin_does_not_need_to_be_unique(self):
        another_user = self._create_second_user()
        self.user.pin = another_user.pin
        self._assert_user_is_valid()

    def test_pin_can_be_50_characters_long(self):
        self.user.pin = 'x'*50
        self._assert_user_is_valid()

    def test_pin_cannot_be_over_50_characters_long(self):
        self.user.pin = 'x'*51
        self._assert_user_is_invalid()

