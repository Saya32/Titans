from datetime import date, timedelta
from django.test import TestCase
from decimal import Decimal
from django.urls import reverse
from django.contrib.messages import get_messages
from spendingtrackers.models import Category, Transaction, User
from spendingtrackers.views import view_category
from spendingtrackers.tests.helpers import reverse_with_next, create_transactions, create_categories

class ViewCategoryTestCase(TestCase):
    """Test case of view category view"""

    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.category = Category.objects.create(name='New', user=self.user, budget=Decimal('500.00'))
        self.filtered_category = Category.objects.filter(user = self.user)
        self.client.login(username=self.user.username, password='Password123')
        
    
    def test_view_category(self):
        url = reverse('view_category', kwargs={'id': self.filtered_category[0].pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_category.html')
    
    def test_view_category_does_not_exist(self):
        url = reverse('view_category', kwargs={'id': (Category.objects.count())+1})
        redirect_url = reverse('feed')
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertTemplateUsed(response, 'feed.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Category could not be found!')
    
    def test_view_category_filter_by_date_range(self):
        url = reverse('view_category', kwargs={'id': self.category.pk})
        from_date = '2023-02-01'
        to_date = '2023-02-28'
        response = self.client.post(url, {'from_date': from_date, 'to_date': to_date})
        self.assertEqual(response.status_code, 200)
        transactions = response.context['transactions']
        self.assertEqual(transactions.count(), 0)

        Transaction.objects.create(
            title='Transaction in Feb 2023', 
            amount=100, 
            category=self.category, 
            user=self.user, 
            date_paid='2023-02-15'
        )

        response = self.client.post(url, {'from_date': from_date, 'to_date': to_date})
        self.assertEqual(response.status_code, 200)
        transactions = response.context['transactions']
        self.assertEqual(transactions.count(), 1)
    
    
    def test_view_category_no_warning(self):
        url = reverse('view_category', kwargs={'id': self.category.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        warning_message = response.context['warning_message']
        self.assertIsNone(warning_message)
    
    