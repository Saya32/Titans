""" Unit Test for the ChangePasswordForm. """
from django.test import TestCase
from spendingtrackers.models import User
from spendingtrackers.forms import ChangePasswordForm
from django.core.exceptions import ValidationError
from django import forms

class ChangePasswordFromTestCase(TestCase):

    def setUp(self):
        self.form_input = {
            'email': 'chuliang.li@kcl.ac.uk',
            'his_password': 'Password123*',
            'password': 'Password123#',
            'password_confirmation': 'Password123#'
        }

    def test_valid_change_password_form(self):
        form = ChangePasswordForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = ChangePasswordForm()
        self.assertIn('email', form.fields)

        self.assertIn('his_password', form.fields)
        his_password_widget = form.fields['his_password'].widget
        self.assertTrue(isinstance(his_password_widget, forms.PasswordInput))

        self.assertIn('password', form.fields)
        password_widget = form.fields['password'].widget
        self.assertTrue(isinstance(password_widget, forms.PasswordInput))

        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))
