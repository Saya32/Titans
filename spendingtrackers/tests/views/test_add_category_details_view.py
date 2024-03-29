"""Test case of new transaction view"""
from django.test import TestCase
from django.urls import reverse
from spendingtrackers.models import User, Category
from spendingtrackers.forms import CategoryDetailsForm
from spendingtrackers.tests.helpers import reverse_with_next

class AddCategoryDetailsViewTestCase(TestCase):
    """Test case of new transaction view"""

    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
        'spendingtrackers/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.data = {
            'name':'Gifts',
            'budget':1000,
            'start_date':'2023-12-12',
            'end_date':'2024-12-12',
        }
        self.url = reverse('add_category_details')

    def test_add_category_view_url(self):
        self.assertEqual(self.url,f'/add_category_details/')

    def test_get_add_new_category_details(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_category_details.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CategoryDetailsForm))
        self.assertFalse(form.is_bound)

    def test_get_add_new_category_redirects_when_not_logged_in(self): 
         redirect_url = reverse_with_next('log_in', self.url)
         response = self.client.get(self.url)
         self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_add_category(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(self.url, self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')

    def test_unsuccessful_add_category(self):
        self.client.login(username=self.user.username, password="Password123")
        count_before = Category.objects.count()
        self.data['start_date'] = "not a date"
        response = self.client.post(self.url, self.data)
        count_after = Category.objects.count()
        self.assertEqual(count_after, count_before)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_category_details.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CategoryDetailsForm))
        self.assertTrue(form.is_bound)
    
    def test_add_existing_category(self):
        self.client.login(username=self.user.username, password="Password123")
        Category.objects.create(name=self.data['name'], user=self.user)
        response = self.client.post(self.url, self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        message = str(messages[0])
        self.assertIn('Error:', message)
        self.assertIn('Category exists', message)