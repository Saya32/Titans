"""Tests of the log in view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from spendingtrackers.models import User
from spendingtrackers.tests.helpers import LogInTester


class SignSuccessViewTestCase(TestCase, LogInTester):
    """Tests of the change password in view."""

    fixtures = ['spendingtrackers/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('sign_success')
        self.user = User.objects.get(username='johndoe@example.org')

    def test_sign_success_url(self):
        self.assertEqual(self.url, '/sign_success/')

