"""Tests of the log in view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from spendingtrackers.forms import ChangePasswordForm
from spendingtrackers.models import User
from spendingtrackers.tests.helpers import LogInTester, reverse_with_next


class ChangePasswordViewTestCase(TestCase, LogInTester):
    """Tests of the change password in view."""

    fixtures = ['spendingtrackers/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('change_password')
        self.user = User.objects.get(username='johndoe@example.org')

    def test_change_password_url(self):
        self.assertEqual(self.url, '/change_password/')

    def test_change_password(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_change_password_successful(self):
        form_input = {'email': 'johndoe@example.org', 'his_password': 'WrongPassword123.',
                      'password': 'WrongPassword12345,', "password_confirmation": "WrongPassword12345,"}

        response = self.client.get(self.url, form_input)
        self.assertEqual(response.status_code, 200)

    def test_change_password_invalid_email(self):
        form_input = {'email': 'johndo22e@example.org', 'his_password': 'WrongPassword123.',
                      'password': 'WrongPassword12345,', "password_confirmation": "WrongPassword12345,"}

        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_change_password_invalid_password(self):
        form_input = {'email': 'johndoe@example.org', 'his_password': '2222.',
                      'password': 'WrongPassw22ord12345,', "password_confirmation": "WrongPassword12345,"}

        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_change_password_invalid_password_confirmation(self):
        form_input = {'email': 'johndoe@example.org', 'his_password': 'WrongPassword123.',
                      'password': 'WrongPassword12345,', "password_confirmation": "Wrong22Password12345,"}

        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_forgot_password_successful(self):
        form_input = {'email': 'johndoe@example.org', 'his_password': 'WrongPassword123.',
                      'password': 'WrongPassword12345,', "password_confirmation": "WrongPassword12345,"}

        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
