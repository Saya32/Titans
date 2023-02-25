"""Unit tests of the change password form."""
from django import forms
from django.test import TestCase
from spendingtrackers.forms import ChangePasswordForm
from spendingtrackers.models import User


class ChangePasswordTestCase(TestCase):
    """Unit tests of the change password form."""

    fixtures = ['spendingtrackers/tests/fixtures/default_user.json']

    def setUp(self):
        self.form_input = {'username': 'johndoe@example.org', 'his_password': 'WrongPassword123',
                           'password': 'WrongPassword12345', "password_confirmation": "WrongPassw22ord12345"}

    def test_form_contains_required_fields(self):
        form = ChangePasswordForm()
        self.assertIn('username', form.fields)
        self.assertIn('his_password', form.fields)
        self.assertIn('password', form.fields)
        self.assertIn('password_confirmation', form.fields)
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = ChangePasswordForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_username(self):
        self.form_input['username'] = ''
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_password(self):
        self.form_input['password'] = ''
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_incorrect_username(self):
        self.form_input['username'] = 'ja'
        form = ChangePasswordForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_incorrect_password(self):
        self.form_input['password'] = 'pwd'
        form = ChangePasswordForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_can_authenticate_valid_user(self):
        fixture = User.objects.get(username='johndoe@example.org')
        form_input = {'username': 'johndoe@example.org', 'password': 'Password123'}
        form = ChangePasswordForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, fixture)

    def test_invalid_credentials_do_not_authenticate(self):
        form_input = {'username': 'johndoe@example.org', 'password': 'WrongPassword123'}
        form = ChangePasswordForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, None)

    def test_blank_password_does_not_authenticate(self):
        form_input = {'username': 'johndoe@example.org', 'password': ''}
        form = ChangePasswordForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, None)

    def test_blank_username_does_not_authenticate(self):
        form_input = {'username': '', 'password': 'Password123'}
        form = ChangePasswordForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, None)
