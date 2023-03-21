from django.test import TestCase
from django.contrib.auth.models import User
from spendingtrackers.models import User, Transaction
import json
from django.urls import reverse

class ChartExpenseGraphTestCase(TestCase):
    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        
        # Create some test transactions
        self.expense1 = Transaction.objects.create(
            user=self.user, 
            transaction_type="Expense", 
            amount=10, 
            date_paid="2022-03-15"
        )
        self.expense2 = Transaction.objects.create(
            user=self.user, 
            transaction_type="Expense", 
            amount=5, 
            date_paid="2022-03-17"
        )
        
    def test_chart_expense_graph(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('chart_expense_graph'))
        self.assertEqual(response.status_code, 200)

        expected_data = {
            'labels': ['03/15/2022', '03/17/2022'],
            'data': [10.0, 5.0]
        }
        self.assertJSONEqual(json.dumps(response.json()), expected_data)