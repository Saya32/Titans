

from django.test import TestCase
from ...models import Category, User, Transaction
from django.core.exceptions import ValidationError
import datetime

class CategoryTest(TestCase):
    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
    ]
    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.category = Category(
            user=self.user,
            name="New",
            budget=40,
            start_date = '2023-12-12',
            end_date = '2024-12-12',
        )
        self.category.save()
    
    def test_valid_category(self):
        self._assert_category_is_valid()
        
    def test_user_should_not_be_blank(self):
        self.category.user = None
        self._assert_category_is_invalid()

    def test_name_may_not_be_blank(self):
        self.category.name = ''
        self._assert_category_is_invalid()
    
    def test_name_should_not_be_too_long(self):
        self.category.name = "X" * 51
        self._assert_category_is_invalid()
    
    
    def test_budget_may_not_be_blank(self):
        self.category.budget = ''
        self._assert_category_is_invalid()

    def test_budget_should_not_be_too_long(self):
        self.category.budget = 999999 * 59999991
        self._assert_category_is_invalid()
    def test_budget_should_not_have_more_than_two_decimal_places(self):
        self.category.budget = 5.234234234
        self._assert_category_is_invalid()
    def test_start_date_may_not_be_blank(self):
        self.category.start_date = None
        self._assert_category_is_invalid()
    def test_end_date_may_not_be_blank(self):
        self.category.end_date = None
        self._assert_category_is_invalid()
    
    def test_get_expenses_no_transactions(self):
        self.assertEqual(self.category.get_expenses(), 0)
    def test_get_income_no_transactions(self):
        self.assertEqual(self.category.get_income(), 0)
    def test_get_balance_no_transactions(self):
        self.assertEqual(self.category.get_balance(), self.category.budget)
   
    def _assert_category_is_valid(self):
        try:
            self.category.full_clean()
        except ValidationError:
            self.fail("Test category should be valid")
    
    def _assert_category_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.category.full_clean()
