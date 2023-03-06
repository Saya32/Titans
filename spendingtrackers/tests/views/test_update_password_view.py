"""Tests of the log in view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from spendingtrackers.models import User
from spendingtrackers.tests.helpers import LogInTester


class UpdatePasswordViewTestCase(TestCase, LogInTester):
    """Tests of the update password in view."""

    fixtures = ['spendingtrackers/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('update_password')
        self.user = User.objects.get(username='johndoe@example.org')

    def test_update_password_url(self):
        self.assertEqual(self.url, '/update_password/')

    def test_update_password(self):
        response = self.client.get(self.url+'?sid=3fef0804-b8b8-11ed-b61e-a2eb1cb544b4')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_password.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_update_password_succesful(self):
        form_input = {"sid": "3fef0804-b8b8-11ed-b61e-a2eb1cb544b4", 'password': 'WrongPassword12345',
                      "password_confirmation": "WrongPassword12345"}

        response = self.client.get(self.url, form_input)
        self.assertEqual(response.status_code, 200)
