from django.test import TestCase
from ...models import Transaction, User
from django.core.exceptions import ValidationError
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile

class TransactionTest(TestCase):

    # Set up a user and a category with valid information.
    def setUp(self):
        self.user = User.objects.create_user(
            first_name = 'John',
            last_name = 'Doe',
            username = 'johndoe@example.org',
            currency = "£",
        )

        self.transaction = Transaction(
            user = self.user,
            transaction_type = 'Expense',
            title = 'Transaction to XXX',
            amount = 20,
            description='Description of this transaction',
            date_paid = '2023-01-01',
            time_paid = '10:10',
            category = 'Grocery',
            receipt = None,
        )
        self.transaction.save()

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_valid_transaction(self):
        self._assert_transaction_is_valid()


    # Functions:
    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test User information should be valid.')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def _assert_transaction_is_valid(self):
        try:
            self.transaction.full_clean()
        except (ValidationError):
            self.fail('Test Transaction information should be valid.')

    def _assert_transaction_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.transaction.full_clean()

    def _create_second_user(self):
        user = User.objects.create_user(
            first_name = 'Jane',
            last_name = 'Doe',
            username = 'janedoe@example.org',
            currency = "£",
        )
        return user

    def _create_second_transaction(self):
        transaction = Transaction(
            user = self.user,
            transaction_type = 'Income',
            title = 'Transaction from XXX',
            amount = 30,
            description='Description of this transaction',
            date_paid = '2023-01-02',
            time_paid = '11:10',
            category = 'Grocery',
            receipt = None,
        )
        return transaction


    # User Tests:
    def test_user_cannot_be_blank(self):
        self.transaction.user = None
        self._assert_transaction_is_invalid()


    # Transaction Type Tests:
    def test_transaction_type_cannot_be_blank(self):
        self.transaction.transaction_type = ''
        self._assert_transaction_is_invalid()

    def test_transaction_type_cannot_be_over_10_characters_long(self):
        self.transaction.transaction_type = 'x'*10
        self._assert_transaction_is_invalid()

    def test_transaction_type_can_be_Expense(self):
        self.transaction.transaction_type = 'Expense'
        self._assert_transaction_is_valid()

    def test_transaction_type_can_be_Income(self):
        self.transaction.transaction_type = 'Income'
        self._assert_transaction_is_valid()


    # Title Tests:
    def test_title_cannot_be_blank(self):
        self.transaction.title = ''
        self._assert_transaction_is_invalid()

    def test_title_can_be_30_characters_long(self):
        self.transaction.title = 'x'*30
        self._assert_transaction_is_valid()

    def test_title_cannot_be_over_30_characters_long(self):
        self.transaction.title = 'x'*31
        self._assert_transaction_is_invalid()


    # Description Tests:
    def test_description_can_be_blank(self):
        self.transaction.description = ''
        self._assert_transaction_is_valid()

    def test_description_can_be_200_characters_long(self):
        self.transaction.description = 'x'*200
        self._assert_transaction_is_valid()

    def test_description_cannot_be_over_200_characters_long(self):
        self.transaction.description = 'x'*201
        self._assert_transaction_is_invalid()


    # Amount Tests:
    def test_amount_cannot_be_blank(self):
        self.transaction.amount = ''
        self._assert_transaction_is_invalid()

    def test_amount_can_be_10_digits_long_only_with_no_more_than_8_digits_before_the_decimal_point(self):
        self.transaction.amount = 10000000.00
        self._assert_transaction_is_valid()

    def test_amount_cannot_be_over_8_digits_before_the_decimal_point(self):
        self.transaction.amount = 1000000000
        self._assert_transaction_is_invalid()

    def test_amount_cannot_be_over_10_digits_long(self):
        self.transaction.amount = 10000000000
        self._assert_transaction_is_invalid()

    def test_amount_can_have_2_decimal_places(self):
        self.transaction.amount = 10.25
        self._assert_transaction_is_valid()

    def test_amount_cannot_have_over_2_decimal_places(self):
        self.transaction.amount = 10.2525
        self._assert_transaction_is_invalid()


    # Date Paid Tests:
    def test_date_can_be_blank(self):
        self.transaction.date_paid = None
        self._assert_transaction_is_valid()


    # Time Paid Tests:
    def test_time_can_be_blank(self):
        self.transaction.time_paid = None
        self._assert_transaction_is_valid()


    # Category Tests:
    def test_category_cannot_be_blank(self):
        self.transaction.category = ''
        self._assert_transaction_is_invalid()

    def test_category_can_be_50_characters_long(self):
        self.transaction.category = 'x'*50
        self._assert_transaction_is_valid()

    def test_category_cannot_be_over_50_characters_long(self):
        self.transaction.category = 'x'*51
        self._assert_transaction_is_invalid()

    def test_category_need_not_to_be_unique(self):
        second_transaction = self._create_second_transaction()
        self.transaction.category = second_transaction.category
        self._assert_transaction_is_valid()


    # Receipt Tests:
    def test_receipt_can_be_blank(self):
        self.transaction.receipt = ''
        self._assert_transaction_is_valid()


    # str Method Tests:
    def test_str_method_can_return_transaction_title(self):
        show_title = 'Transaction to XXX'
        self.assertEqual(str(self.transaction), show_title)


# Example got from here: https://stackoverflow.com/questions/63476979/unit-testing-django-model-with-an-image-not-quite-understanding-simpleuploaded
    def test_receipt_url_returns_url_if_present(self):
        self.transaction.receipt = SimpleUploadedFile(name='receipt_test.jpg', content='', content_type='receipt/jpg')
        self.assertIsNotNone(self.transaction.receipt_url())

    def test_receipt_url_returns_none_if_not_present(self):
        self.assertIsNone(self.transaction.receipt_url())
