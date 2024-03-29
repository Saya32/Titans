"""Tests of the log in view."""
from django.test import TestCase
from django.urls import reverse
from spendingtrackers.models import User
from spendingtrackers.tests.helpers import LogInTester


class BannerViewTestCase(TestCase, LogInTester):
    """Tests of the change password in view."""

    fixtures = ['spendingtrackers/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('banner')
        self.user = User.objects.get(username='johndoe@example.org')

    def test_banner_url(self):
        self.assertEqual(self.url, '/banner/')
    
    def test_banner_success(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'banner.html')

