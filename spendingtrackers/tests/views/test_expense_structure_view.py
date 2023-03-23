from django.test import TestCase, Client
from django.contrib.auth.models import User
from spendingtrackers.models import User, Transaction
import json
from django.urls import reverse

class ExpenseStructureTestCase(TestCase):
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
            date_paid="2022-03-16"
        )
        self.expense2 = Transaction.objects.create(
            user=self.user, 
            transaction_type="Expense", 
            amount=5, 
            date_paid="2022-03-17"
        )
        
    def test_chart_expense_structure_graph(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('expense_structure'))
        self.assertEqual(response.status_code, 200)

        expected_data = {
            'labels': ['', '', ''],
            'total' : '20.00',
            'percentlabel':[],
            'data': {'': 20}
        }
        self.assertJSONEqual(json.dumps(response.json()), expected_data)
    
    def test_filter_transactions_by_date_range_for_chart_income_graph(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('expense_structure'), {'from_date': '2022-02-14', 'to_date': '2022-03-16'})
        expected_data = {
            'labels': ['',''],
            'total' : '15.00',
            'percentlabel':[],
            'data': {'': 15}
        }
        self.assertJSONEqual(json.dumps(response.json()), expected_data)


