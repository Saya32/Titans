from django.test import TestCase
from django.urls import reverse
from spendingtrackers.models import User

class HomeViewTestCase(TestCase):
    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_search_by_name(self):
        response = self.client.get(reverse("home_page"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("home_page"))
        self.assertTemplateUsed(response, "home_page.html")
    

    def test_unauthenticated_user_redirected_to_home_page(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home_page.html")

    def test_feed_used_for_authenticated_user(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get("/")
        self.assertTemplateUsed(response, "feed.html")

  