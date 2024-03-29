"""Tests of the log out view."""
from django.test import TestCase
from django.urls import reverse
from spendingtrackers.models import User
from spendingtrackers.helpers import LogInTester

class LogOutViewTestCase(TestCase, LogInTester):
    """Tests of the log out view."""

    def setUp(self):
        self.url = reverse('log_out')
        self.user = User.objects.create_user('johndoe@example.org',
            first_name='John',
            last_name='Doe',
            password='Password123',
            is_active=True,
        )

    def test_log_out_url(self):
        self.assertEqual(self.url,'/log_out/')

    def test_get_log_out(self):
        self.client.login(username='johndoe@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse('home_page')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home_page.html')
        self.assertFalse(self._is_logged_in())