"""Unit tests of the sign up form."""
from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from spendingtrackers.forms import SignUpForm
from spendingtrackers.models import User

class SignUpFormTestCase(TestCase):
    """Unit tests of the sign up form."""

    # Set up a valid sign up data.
    def setUp(self):
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'janedoe@example.com',
            'currency': '£',
<<<<<<< HEAD
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
            'pin': 'Password123'
=======
            'new_password': 'Password123*',
            'password_confirmation': 'Password123*'
        }
        self.form_input_wrong = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'currency': '£',
            'new_password': 'Password123*',
            'password_confirmation': 'Password123*'
>>>>>>> main
        }

    # Form accepts valid input data.
    def test_valid_sign_up_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Form rejects invalid input data.
    def test_invalid_sign_up_form(self):
        form = SignUpForm(data=self.form_input_wrong)
        self.assertFalse(form.is_valid())


    # Form has necessary fields.
    def test_form_has_necessary_fields(self):
        form = SignUpForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)

        self.assertIn('username', form.fields)
        email_field = form.fields['username']
        self.assertTrue(isinstance(email_field, forms.EmailField))

        self.assertIn('new_password', form.fields)
<<<<<<< HEAD
        self.assertIn('pin', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
=======
        password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(password_widget, forms.PasswordInput))

>>>>>>> main
        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_widget, forms.PasswordInput))


    # Form uses model validation.
    def test_form_uses_model_validation(self):
        self.form_input['username'] = 'jd'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())


    # New password and password confirmation has correct format
    def test_passwords_must_contain_lowercase_character(self):
        self.form_input['new_password'] = 'PASSWORD123*'
        self.form_input['password_confirmation'] = 'PASSWORD123*'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_passwords_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'password123*'
        self.form_input['password_confirmation'] = 'password123*'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_passwords_must_contain_special_character(self):
        self.form_input['new_password'] = 'Password123'
        self.form_input['password_confirmation'] = 'Password123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_passwords_must_contain_number(self):
        self.form_input['new_password'] = 'Passwordabc*'
        self.form_input['password_confirmation'] = 'Passwordabc*'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())


    # New password and passwor confirmation must be identical.
    def test_password_confirmation_and_new_password_are_identical(self):
        self.form_input['password_confirmation'] = 'WrongPassword'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())


    # Sign up form data must be saved correctly.
    def test_form_must_save_correctly(self):
        form = SignUpForm(data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)
        user = User.objects.get(username='janedoe@example.com')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        is_password_correct = check_password('Password123*', user.password)
        self.assertTrue(is_password_correct)
