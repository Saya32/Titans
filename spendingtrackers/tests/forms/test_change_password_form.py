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
            'password': 'Password123',
            'password_confirmation': 'Password123'
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


    # Email test:
    def test_email_cannot_be_blank(self):
        self.form_input['email'] = ''
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_email_can_be_50_characters_long(self):
        self.form_input['email'] = 'x'*50
        form = ChangePasswordForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_email_cannot_be_over_50_characters_long(self):
        self.form_input['email'] = 'x'*51
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())


    # History Password tests:
    def test_his_password_must_contain_uppercase_character(self):
        self.form_input['his_password'] = 'password123'
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_his_password_must_contain_lowercase_character(self):
        self.form_input['his_password'] = 'PASSWORD123'
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_his_password_must_contain_number(self):
        self.form_input['his_password'] = 'Password'
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())


    # New Password test:
    def test_password_must_contain_uppercase_character(self):
        self.form_input['password'] = 'password123'
        self.form_input['password_confirmation'] = 'password123'
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['password'] = 'PASSWORD123'
        self.form_input['password_confirmation'] = 'PASSWORD123'
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['password'] = 'Password'
        self.form_input['password_confirmation'] = 'Password'
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_and_his_password_cannot_be_identical(self):
        self.form_input['password'] = 'Password123*'
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_and_password_confirmation_are_identical(self):
        self.form_input['password_confirmation'] = 'ponbiubijbuinassword123'
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())
