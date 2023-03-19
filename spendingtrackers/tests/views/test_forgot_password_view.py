"""Tests of the log in view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from spendingtrackers.models import User
from spendingtrackers.tests.helpers import LogInTester
from django.contrib.auth.hashers import make_password, check_password


class ForgotPasswordViewTestCase(TestCase, LogInTester):
    """Tests of the update password in view."""

    fixtures = ['spendingtrackers/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('forgot_password')
        self.user = User.objects.get(username='johndoe@example.org')

    def test_forgot_password_url(self):
        self.assertEqual(self.url, '/forgot_password/')

    def test_forgot_password(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forgot_password.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_forgot_password_succesful(self):
        form_input = {"pin": "johndoe@example.org", 'email': 'johndoe@example.org', 'password': 'WrongPassword12345',
                      "password_confirmation": "WrongPassword12345"}

        response = self.client.get(self.url, form_input)
        self.assertEqual(response.status_code, 200)

    # def test_forgot_password_error(self):
    #     form_input = {"pin": "johndoe@example.org", 'email': 'johndoe@example.org', 'password': 'aaa1',
    #                   "password_confirmation": "aaa"}

    #     response = self.client.post(self.url, form_input)
    #     self.assertEqual(response.status_code, 200)
    #     messages_list = list(response.context['messages'])
    #     self.assertEqual(len(messages_list), 1)
    #     self.assertEqual(messages_list[0].level, messages.ERROR)

    # def test_forgot_password_succesful(self):
    #     form_input = {"pin": "1234", 'email': 'johndoe@example.org', 'password': 'NewPassword123',
    #                   "password_confirmation": "NewPassword123"}
    #     response = self.client.post(self.url, form_input)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'SUCCESS!')
    #     user = User.objects.get(username='johndoe@example.org')
    #     self.assertTrue(check_password('NewPassword123', user.password))

    def test_forgot_password_invalid_email(self):
        form_input = {"pin": "1234", 'email': 'invalidemail@example.org', 'password': 'NewPassword123',
                      "password_confirmation": "NewPassword123"}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'email does not exist!')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_forgot_password_invalid_pin(self):
        form_input = {"pin": "4321", 'email': 'johndoe@example.org', 'password': 'NewPassword123',
                      "password_confirmation": "NewPassword123"}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'pin error!')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_forgot_password_invalid_password_format(self):
        form_input = {"pin": "1234", 'email': 'johndoe@example.org', 'password': 'weakpassword',
                      "password_confirmation": "weakpassword"}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Password must contain an uppercase character, a lowercase character and a number')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    # def test_forgot_password_password_mismatch(self):
    #     form_input = {"pin": "1234", 'email': 'johndoe@example.org', 'password': 'NewPassword123',
    #                   "password_confirmation": "MismatchPassword123"}
    #     response = self.client.post(self.url, form_input)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'The two passwords are inconsistent!')
    #     messages_list = list(response.context['messages'])
    #     self.assertEqual(len(messages_list), 1)
    #     self.assertEqual(messages_list[0].level, messages.ERROR)