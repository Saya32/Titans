from django.test import TestCase
from django.urls import reverse
from ...models import User, Achievement, Transaction, Category
from ...views import view_achievements
from ...helpers import set_achievements, get_achievements, update_achievements, set_achievements
from spendingtrackers.tests.helpers import reverse_with_next, create_categories, create_transactions


class AchievementsViewTestCase(TestCase):
    """Test case of pending transactions view"""

    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
        'spendingtrackers/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.url = reverse('view_achievements')
        self.user = User.objects.get(username='johndoe@example.org')
        create_transactions(self.user,0,16)
        create_categories(self.user,0,16)
        self.transactions = Transaction.objects.filter()

    def test_view_achievements_url(self):
        self.assertEqual(self.url,'/view_achievements/')
    
    def test_get_view_achievements_redirects_when_not_logged_in(self):  
         redirect_url = reverse_with_next('log_in', self.url)
         response = self.client.get(self.url)
         self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
        
 