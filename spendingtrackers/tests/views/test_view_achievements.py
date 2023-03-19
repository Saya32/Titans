from django.test import TestCase
from django.urls import reverse
from ...models import User, Achievement
from ...views import view_achievements
from ...helpers import set_achievements, get_achievements, update_achievements

class ViewAchievementTestCase(TestCase):
    """Test case of view achievements view"""

    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.client.login(username=self.user.username, password='Password123')

    def test_view_achievements(self):
        url = reverse('view_achievements')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_achievements.html')
