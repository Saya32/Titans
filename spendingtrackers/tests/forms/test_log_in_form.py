"""Unit tests of the log in form."""
from django import forms
from django.test import TestCase
from spendingtrackers.forms import LogInForm
from spendingtrackers.models import User

class LogInFormTestCase(TestCase):
    """Unit tests of the log in form."""

    fixtures = ['spendingtrackers/tests/fixtures/default_user.json']

    # Set up a valid log in data input.
    def setUp(self):
        self.form_input = {
            'username': 'janedoe@example.com',
            'password': 'Password123*'
        }

    # Test log in form accecpts valid input data.
    def test_valid_log_in_form(self):
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test log in form has necessary fields.
    def test_form_has_necessary_fields(self):
        form = LogInForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        password_widget = form.fields['password'].widget
        self.assertTrue(isinstance(password_widget, forms.PasswordInput))

    # Test blank username is rejected.
    def test_form_rejects_blank_username(self):
        self.form_input['username'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # Test blank password is rejected.
    def test_form_rejects_blank_password(self):
        self.form_input['password'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # Test incorrect username is accecpted.
    def test_form_accepts_incorrect_username(self):
        self.form_input['username'] = 'ja'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test incorrect password is accecpted.
    def test_form_accepts_incorrect_password(self):
        self.form_input['password'] = 'wrongpassword'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test valid user can be authenticated.
    def test_form_can_authenticate_valid_user(self):
        fixture = User.objects.get(username='johndoe@example.org')
        #self.form_input['username'] = 'johndoe@example.org'
        #self.form_input['password'] = 'Password123*'
        #form = LogInForm(data=self.form_input)
        form_input = {'username': 'johndoe@example.org', 'password': 'Password123'}
        form = LogInForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, fixture)

    # Test invalid user does not authenticate.
    def test_form_do_not_authenticate_invalid_user(self):
        #self.form_input['password'] = 'wrongpassword'
        #form = LogInForm(data=self.form_input)
        form_input = {'username': 'johndoe@example.org', 'password': 'WrongPassword123'}
        form = LogInForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, None)

    # Test blank username does not authenticate.
    def test_form_do_not_authenticate_invalid_user(self):
        #self.form_input['username'] = ''
        #form = LogInForm(data=self.form_input)
        form_input = {'username': '', 'password': 'Password123*'}
        form = LogInForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, None)

    # Test blank password does not authenticate.
    def test_form_do_not_authenticate_invalid_user(self):
        #self.form_input['password'] = ''
        #form = LogInForm(data=self.form_input)
        form_input = {'username': 'johndoe@example.org', 'password': ''}
        form = LogInForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, None)
