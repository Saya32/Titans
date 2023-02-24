from django import forms
from django.test import TestCase
from ...forms import CategoryDetailsForm
from ...models import Transaction, User
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

class CategoryDetailsFormTestCase(TestCase):
    """Unit tests of the sign up form."""

    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.form_input = {
            'name':'New',
            'budget':10,
            'start_date':'2022-12-12',
            'end_date': '2023-12-12'
        }

    def test_valid_transaction_form(self):
        form = CategoryDetailsForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = CategoryDetailsForm()
        self.assertIn('name', form.fields)

        self.assertIn('budget', form.fields)
        budget = form.fields['budget']
        self.assertTrue(isinstance(budget, forms.IntegerField))

        self.assertIn('start_date', form.fields)
        start_date = form.fields['start_date']
        self.assertTrue(isinstance(start_date, forms.DateField))

        self.assertIn('end_date', form.fields)
        end_date = form.fields['end_date']
        self.assertTrue(isinstance(end_date, forms.DateField))


    def test_form_uses_model_validation(self):
        self.form_input['budget'] = 61.2222
        form = CategoryDetailsForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_date_paid_should_can_be_none(self):
        self.form_input['date_paid'] = ""
        form = CategoryDetailsForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_time_paid_can_be_none(self):
        self.form_input['time_paid'] = ""
        form = CategoryDetailsForm(data=self.form_input)
        self.assertTrue(form.is_valid())