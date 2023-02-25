from django.test import TestCase
from django.urls import reverse
from spendingtrackers.forms import TransactionForm
from spendingtrackers.models import User, Transaction
from django.db import models
from spendingtrackers.tests.helpers import reverse_with_next, create_transactions


class DashboardViewTestCase(TestCase):
    """Test case of pending transactions view"""

    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
        'spendingtrackers/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.url = reverse('dashboard')
        self.user = User.objects.get(username='johndoe@example.org')
        create_transactions(self.user, 0, 2)
        self.transactions = Transaction.objects.filter()

    def test_dashboard_url(self):
        self.assertEqual(self.url, '/dashboard/')

    def test_get_dashboard(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_filter_dashboard_by_date_range(self):
        self.client.login(username=self.user.username, password='Password123')
        create_transactions(self.user, 0, 2)
        transaction1 = Transaction.objects.first()
        transaction2 = Transaction.objects.last()
        transaction1.date_paid = '2023-02-15'
        transaction2.date_paid = '2023-02-17'
        transaction1.save()
        transaction2.save()
        response = self.client.post(self.url, {'from_date': '2023-02-14', 'to_date': '2023-02-16'})
        self.assertEqual(response.status_code, 200)
        result = [{'day': '2023-02-16', 'income_rate': '-100.00%', 'expense_rate': '0.0%', 'balance_rate': '0.00%',
                   'now_balance':0, 'now_expense': 0, 'now_income': 0},
                  {'day': '2023-02-15', 'income_rate': '1000.00%', 'expense_rate': '0.0%', 'balance_rate': '-100.00%',
                   'now_balance': 0, 'now_expense': 0, 'now_income': 1000},
                  {'day': '2023-02-14', 'income_rate': '0.0%', 'expense_rate': '0.0%', 'balance_rate': '-0.00%',
                   'now_balance': -1000, 'now_expense': 0, 'now_income': 0}]
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(result, response.context['result'])
