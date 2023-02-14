from django import forms
from django.test import TestCase
from ...forms import SpendingLimitForm
from ...models import Category, User

class SpendingLimitFormTestCase(TestCase):
    """Unit tests of the sign up form."""

    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.form_input = {
            'spending_limit': '350',
            'category_choices': 'Groceries'
        }

    def test_valid_spending_limit_form(self):
        form = SpendingLimitForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = SpendingLimitForm()

        self.assertIn('spending_limit', form.fields)
        amount = form.fields['spending_limit']
        self.assertTrue(isinstance(amount, forms.IntegerField))

        self.assertIn('category_choices', form.fields)
        category = form.fields['category_choices']
        self.assertTrue(isinstance(category, forms.ChoiceField))

    def test_form_uses_model_validation(self):
        self.form_input['spending_limit'] = '90.5777'
        form = SpendingLimitForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_category_should_not_be_none(self):
        self.form_input['category_choices'] = ""
        form = SpendingLimitForm(data=self.form_input)
        self.assertFalse(form.is_valid())
