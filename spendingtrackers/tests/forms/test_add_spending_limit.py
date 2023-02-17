from django import forms
from django.test import TestCase
from ...forms import CategoryDetailsForm
from ...models import Category, User

class CategoryDetailsFormTestCase(TestCase):
    """Unit tests of the sign up form."""

    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.form_input = {
            'spending_limit': '350',
            'category_choices': 'Groceries',
            'budget': '350',
            'start_date': '2022-10-10',
            'end_date': '2022-11-10'
        }

    def test_valid_category_details_form(self):
        form = CategoryDetailsForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # def test_form_has_necessary_fields(self):
    #     form = CategoryDetailsForm()

    #     self.assertIn('spending_limit', form.fields)
    #     amount = form.fields['spending_limit']
    #     self.assertTrue(isinstance(amount, forms.IntegerField))

    #     self.assertIn('category_choices', form.fields)
    #     category = form.fields['category_choices']
    #     self.assertTrue(isinstance(category, forms.ChoiceField))

    #     self.assertIn('budget', form.fields)
    #     amount = form.fields['budget']
    #     self.assertTrue(isinstance(amount, forms.IntegerField))

    #     self.assertIn('start_date', form.fields)
    #     category = form.fields['start_date']
    #     self.assertTrue(isinstance(category, forms.DateField))

    #     self.assertIn('end_date', form.fields)
    #     amount = form.fields['end_date']
    #     self.assertTrue(isinstance(amount, forms.DateField))

    # def test_form_uses_model_validation(self):
    #     self.form_input['spending_limit'] = '90.5777'
    #     form = SpendingLimitForm(data=self.form_input)
    #     self.assertFalse(form.is_valid())

    # def test_category_should_not_be_none(self):
    #     self.form_input['category_choices'] = ""
    #     form = SpendingLimitForm(data=self.form_input)
    #     self.assertFalse(form.is_valid())

    # def test_budget_should_not_be_none(self):
    #     self.form_input['budget'] = ""
    #     form = SpendingLimitForm(data=self.form_input)
    #     self.assertFalse(form.is_valid())

    # def test_start_date_should_not_be_none(self):
    #     self.form_input['start_date'] = ""
    #     form = SpendingLimitForm(data=self.form_input)
    #     self.assertFalse(form.is_valid())

    # def test_end_date_should_not_be_none(self):
    #     self.form_input['end_date'] = ""
    #     form = SpendingLimitForm(data=self.form_input)
    #     self.assertFalse(form.is_valid())
