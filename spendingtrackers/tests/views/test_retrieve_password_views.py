"""Tests of the log in view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from spendingtrackers.models import User
from spendingtrackers.tests.helpers import LogInTester


class UpdatePasswordViewTestCase(TestCase, LogInTester):
    """Tests of the retrieve_password in view."""

    fixtures = ['spendingtrackers/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('retrieve_password')
        self.user = User.objects.get(username='johndoe@example.org')

    def test_retrieve_password_url(self):
        self.assertEqual(self.url, '/retrieve_password/')

    def test_retrieve_password(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'retrieve_password.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_retrieve_password_succesful(self):
        form_input = {"email": "johndoe@example.org"}

        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
