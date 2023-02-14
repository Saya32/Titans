from django.test import TestCase
from ...models import Transaction, User
from django.core.exceptions import ValidationError
import datetime


class TransactionTest(TestCase):
    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
    ]
    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.transaction = Transaction(
            user=self.user,
            transaction_type='Expense',
            title="TitleOne",
            amount=40,
            description='Description One',
            date_paid = '2023-12-12',
            time_paid = '20:20',
            category='Salary',
            receipt=None,
        )
    
    def test_valid_transaction(self):
        self._assert_transaction_is_valid()
        
    def test_user_should_not_be_blank(self):
        self.transaction.user = None
        self._assert_transaction_is_invalid()


    def test_transaction_type_should_not_be_blank(self):
        self.transaction.transaction_type = ""
        self._assert_transaction_is_invalid()
    

    def test_title_may_not_be_blank(self):
        self.transaction.title = ''
        self._assert_transaction_is_invalid()
    
    def test_title_should_not_be_too_long(self):
        self.transaction.title = "X" * 51
        self._assert_transaction_is_invalid()
    
    def test_description_may_be_blank(self):
        self.transaction.description = ''
        self._assert_transaction_is_valid()
    
    def test_description_should_not_be_too_long(self):
        self.transaction.title = "X" * 300
        self._assert_transaction_is_invalid()

    def test_amount_may_not_be_blank(self):
        self.transaction.amount = ''
        self._assert_transaction_is_invalid()


    def test_amount_should_not_be_too_long(self):
        self.transaction.amount = 999999 * 59999991
        self._assert_transaction_is_invalid()

    def test_amount_should_not_have_more_than_two_decimal_places(self):
        self.transaction.amount = 5.234234234
        self._assert_transaction_is_invalid()


    def test_category_may_not_be_blank(self):
        self.transaction.category = ''
        self._assert_transaction_is_invalid()
    
    def test_reciept_may_be_blank(self):
        self.transaction.receipt = ''
        self._assert_transaction_is_valid()

    
    def _assert_transaction_is_valid(self):
        try:
            self.transaction.full_clean()
        except ValidationError:
            self.fail("Test transaction should be valid")
    
    def _assert_transaction_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.transaction.full_clean()