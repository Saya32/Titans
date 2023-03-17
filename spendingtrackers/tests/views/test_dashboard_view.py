from django.test import TestCase
from django.urls import reverse
from spendingtrackers.models import User

class DashboardTestCase(TestCase):
    fixtures = ['spendingtrackers/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')

    def test_url_exists_at_correct_location(self):
        self.client.login(username=self.user.username, password='Password123')
        dash_url = reverse('dashboard')
        response = self.client.get(dash_url)
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        self.client.login(username=self.user.username, password='Password123')
        dash_url = reverse('dashboard')
        response = self.client.get(dash_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

