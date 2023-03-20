from decimal import Decimal
from spendingtrackers.models import Category, Transaction, User
from django.test import TestCase, Client
from django.urls import reverse
from spendingtrackers.models import Category, Transaction
from spendingtrackers.views import overall
from spendingtrackers.tests.helpers import reverse_with_next
from ...helpers import get_user_balance,get_user_income,get_user_budget,get_user_expense
from datetime import datetime

class OverallTestCase(TestCase):
    """Test case of overall view"""

    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.category = Category.objects.create(name='New', user=self.user, budget=Decimal('500.00'))
        self.filtered_category = Category.objects.filter(user = self.user)
        self.client.login(username=self.user.username, password='Password123')
    
    def test_overall(self):
        url = reverse('overall')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'overall.html')
    
    def test_view_category_filter_by_date_range(self):
        url = reverse('overall')
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
    
    def test_view_category_filter_by_date_range_outside_range(self):
        url = reverse('overall')
        from_date = '2023-02-01'
        to_date = '2023-02-28'
        Transaction.objects.create(
            title='Transaction Jan 2023', 
            amount=100, 
            category=self.category, 
            user=self.user, 
            date_paid='2023-01-15'
        )
        response = self.client.post(url, {'from_date': from_date, 'to_date': to_date})
        self.assertEqual(response.status_code, 200)
        transactions = response.context['transactions']
        self.assertEqual(transactions.count(), 0)
    
    def test_no_transactions(self):
        url = reverse('overall')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'overall.html')
        self.assertEqual(response.context['transactions'].count(), 0)
        self.assertEqual(response.context['expense'], 0)
        self.assertEqual(response.context['income'], 0)
        self.assertEqual(response.context['balance'], 500)
        self.assertIsNone(response.context['warning_message'])
    
    def test_negative_balance(self):
        url = reverse('overall')
        Transaction.objects.create(
        title='Expense',
        amount=510,
        category=self.category,
        user=self.user,
        date_paid=datetime.now().date()
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'overall.html')
        self.assertEqual(response.context['transactions'].count(), 1)
        self.assertEqual(response.context['expense'], 510)
        self.assertEqual(response.context['income'], 0)
        self.assertEqual(response.context['balance'], -10)
        self.assertEqual(response.context['warning_message'], "Warning: You have exceeded your budget for this category.")
    
    def test_budget_warning(self):
        url = reverse('overall')
        Transaction.objects.create(
        title='Expense',
        amount=450,
        category=self.category,
        user=self.user,
        date_paid=datetime.now().date()
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'overall.html')
        self.assertEqual(response.context['transactions'].count(), 1)
        self.assertEqual(response.context['expense'], 450)
        self.assertEqual(response.context['income'], 0)
        self.assertEqual(response.context['balance'], 50)
        self.assertEqual(response.context['warning_message'], "Warning: You have used 90.00% of your budget for this category.")
    