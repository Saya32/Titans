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
        set_achievements(self.user)
        get_achievements(self.user)
        update_achievements(self.user)

    def test_view_achievements_url(self):
        self.assertEqual(self.url,'/view_achievements/')
    
    def test_view_achievements_success(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'view_achievements.html')
    
    
    def test_get_view_achievements_redirects_when_not_logged_in(self):  
         redirect_url = reverse_with_next('log_in', self.url)
         response = self.client.get(self.url)
         self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    

    def test_default_achievement(self):
        self.client.login(username=self.user.username, password="Password123") 
        achievements = Achievement.objects.filter(user=self.user)
        self.assertTrue(achievements[0].unlocked)

    def test_category_achievements(self):
        self.client.login(username=self.user.username, password="Password123") 
        achievements = Achievement.objects.filter(user=self.user)
        self.assertTrue(achievements[1].unlocked)
        self.assertTrue(achievements[2].unlocked)
        self.assertTrue(achievements[3].unlocked)
    

    def test_transaction_achievements(self):
        self.client.login(username=self.user.username, password="Password123") 
        achievements = Achievement.objects.filter(user=self.user)
        self.assertTrue(achievements[4].unlocked)
        self.assertTrue(achievements[5].unlocked)
        self.assertTrue(achievements[6].unlocked)
 