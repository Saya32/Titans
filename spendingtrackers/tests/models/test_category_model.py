from django.test import TestCase
from ...models import Category, User, Transaction
from django.core.exceptions import ValidationError
import datetime

class CategoryTest(TestCase):

    # Set up a user and a category with valid information.
    def setUp(self):
        self.user = User.objects.create_user(
            first_name = 'John',
            last_name = 'Doe',
            username = 'johndoe@example.org',
            currency = "£",
        )

        self.category = Category(
            user = self.user,
            name = 'Grocery',
            budget = 50,
            start_date = '2023-01-01',
            end_date = '2023-01-31',
        )
        self.category.save()

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_valid_user(self):
        self._assert_category_is_valid()


    # Functions:
    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test User information should be valid.')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def _assert_category_is_valid(self):
        try:
            self.category.full_clean()
        except (ValidationError):
            self.fail('Test Category information should be valid.')

    def _assert_category_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.category.full_clean()

    def _create_second_user(self):
        user = User.objects.create_user(
            first_name = 'Jane',
            last_name = 'Doe',
            username = 'janedoe@example.org',
            currency = "£",
        )
        return user

    def _create_second_category(self):
        category = Category(
            user = self.user,
            name = 'Grocery',
            budget = 40,
            start_date = '2023-01-01',
            end_date = '2023-01-31',
        )
        return category


    # User Tests:
    def test_user_cannot_be_blank(self):
        self.category.user = None
        self._assert_category_is_invalid()


    # Name Tests:
    def test_name_cannot_be_blank(self):
        self.category.name = ''
        self._assert_category_is_invalid()

    def test_name_can_be_50_charcters_long(self):
        self.category.name = 'x'*50
        self._assert_category_is_valid()

    def test_name_cannot_be_over_50_characters_long(self):
        self.category.name = 'x'*51
        self._assert_category_is_invalid()

    def test_name_need_not_to_be_unique(self):
        second_category = self._create_second_category()
        self.category.name = second_category.name
        self._assert_category_is_valid()


    # Budget Tests:
    def test_budget_cannot_be_blank(self):
        self.category.budget = ''
        self._assert_category_is_invalid()

    def test_budget_can_be_10_digits_long_only_with_no_more_than_8_digits_before_the_decimal_point(self):
        self.category.budget = 10000000.00
        self._assert_category_is_valid()

    def test_budget_cannot_be_over_8_digits_before_the_decimal_point(self):
        self.category.budget = 1000000000
        self._assert_category_is_invalid()

    def test_budget_cannot_be_over_10_digits_long(self):
        self.category.budget = 10000000000
        self._assert_category_is_invalid()

    def test_budget_can_have_2_decimal_places(self):
        self.category.budget = 10.25
        self._assert_category_is_valid()

    def test_budget_cannot_have_over_2_decimal_places(self):
        self.category.budget = 10.2525
        self._assert_category_is_invalid()


    # Start Date Tests:
    def test_start_date_cannot_be_blank(self):
        self.category.start_date = None
        self._assert_category_is_invalid()


    # End Date Tests:
    def test_end_date_cannot_be_blank(self):
        self.category.end_date = None
        self._assert_category_is_invalid()


    # Expense, Income, Balance Tests;
    def test_get_expenses_with_no_transactions(self):
        self.assertEqual(self.category.get_expenses(), 0)

    def test_get_income_with_no_transactions(self):
        self.assertEqual(self.category.get_income(), 0)

    def test_get_balance_woth_no_transactions(self):
        self.assertEqual(self.category.get_balance(), self.category.budget)
