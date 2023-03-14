
from django.test import TestCase
from django.urls import reverse
from spendingtrackers.forms import CategoryDetailsForm
from spendingtrackers.models import User, Category
from spendingtrackers.tests.helpers import reverse_with_next, create_categories

class CategoryViewTestCase(TestCase):
    """Test case of pending categories view"""

    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
        'spendingtrackers/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.url = reverse('category')
        self.user = User.objects.get(username='johndoe@example.org')
        create_categories(self.user,0,2)
        self.categories = Category.objects.filter()

    def test_category_url(self):
        self.assertEqual(self.url,'/category/')
    
    def test_get_category(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')
    
    def test_category_shows_student_only_their_categorys(self):
        self.client.login(username=self.user.username, password='Password123')
        other_user = User.objects.get(username='janedoe@example.org')
        create_categories(other_user, 10, 20)
        create_categories(self.user, 30, 40)
        response = self.client.get(self.url)
        for count in range (10,20):
            self.assertNotContains(response, f'Category__{count}')
        for count in range (30,40):
            self.assertContains(response, f'Category__{count}')


    def test_category_redirects_when_not_logged_in(self): 
         redirect_url = reverse_with_next('log_in', self.url)
         response = self.client.get(self.url)
         self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)