from django import forms
from django.test import TestCase
from ...forms import TransactionForm
from ...models import Transaction, User
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

class SignUpFormTestCase(TestCase):
    """Unit tests of the sign up form."""

    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.form_input = {
            'title': 'Shopping',
            'description': 'At asda',
            'amount': 20,
            'date_paid': '2022-12-12',
            'time_paid': '10:10',
            'category': 'Groceries',
            'receipt': '',
            'transaction_type': 'Expense'
        }

    def test_valid_transaction_form(self):
        form = TransactionForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = TransactionForm()
        self.assertIn('title', form.fields)

        self.assertIn('description', form.fields)
        
        self.assertIn('amount', form.fields)
        amount = form.fields['amount']
        self.assertTrue(isinstance(amount, forms.IntegerField))

        self.assertIn('date_paid', form.fields)
        date_paid = form.fields['date_paid']
        self.assertTrue(isinstance(date_paid, forms.DateField))

        self.assertIn('time_paid', form.fields)
        time_paid = form.fields['time_paid']
        self.assertTrue(isinstance(time_paid, forms.TimeField))

        self.assertIn('category', form.fields)
        category = form.fields['category']
        self.assertTrue(isinstance(category, forms.ChoiceField))

        self.assertIn('receipt', form.fields)
        receipt = form.fields['receipt']
        self.assertTrue(isinstance(receipt, forms.ImageField))
        
        self.assertIn('transaction_type', form.fields)
        transaction_type = form.fields['transaction_type']
        self.assertTrue(isinstance(transaction_type, forms.ChoiceField))



    def test_form_uses_model_validation(self):
        self.form_input['amount'] = 61.2222
        form = TransactionForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_date_paid_should_not_be_none(self):
        self.form_input['date_paid'] = ""
        form = TransactionForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_time_paid_should_not_be_none(self):
        self.form_input['time_paid'] = ""
        form = TransactionForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    

