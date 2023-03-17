from django.test import TestCase
from django.urls import reverse
from spendingtrackers.forms import TransactionForm
from spendingtrackers.models import User, Transaction
from spendingtrackers.tests.helpers import reverse_with_next, create_transactions, create_categories

class DashboardTestCase(TestCase):
    """Test case of Dashboard view"""

    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
        'spendingtrackers/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.url = reverse('dashboard')
        self.user = User.objects.get(username='johndoe@example.org')
        create_transactions(self.user,0,2)
        create_categories(self.user,0,2)
        self.transactions = Transaction.objects.filter()

    def test_dashboard_url(self):
        self.assertEqual(self.url,'/dashboard/')
    
    def test_get_dashboard(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_chart_balance_graph(self):
        # Create some sample transactions
        self.client.login(username=self.user.username, password='Password123')
        create_transactions(self.user, 0, 2)
        transaction1 = Transaction.objects.first()
        transaction2 = Transaction.objects.last()
        transaction1.date_paid = '01/01/2022'
        transaction2.date_paid = '01/02/202'
        transaction1.transaction_type = 'Income'
        transaction2.transaction_type = 'Expense'
        transaction1.amount = '100'
        transaction2.amount = '50'
        transaction1.save()
        transaction2.save()
        
        response = self.client.post(self.url, {'from_date': '2023-02-14', 'to_date': '2023-02-16'})
        # Check that the labels and data are correct
        self.assertEqual(data['labels'], ['01/01/2022', '01/02/2022'])
        self.assertEqual(data['data'], [100, 50])
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertIn(transaction1, response.context['transactions'])
        self.assertNotIn(transaction2, response.context['transactions'])

    #def test_chart_expense_graph(self):
        # Create some sample transactions
        self.client.login(username=self.user.username, password='Password123')
        transaction1 = Transaction.objects.create(user=user, transaction_type='Income', amount=100, date_paid=datetime.date(2022, 1, 1))
        transaction2 = Transaction.objects.create(user=user, transaction_type='Expense', amount=50, date_paid=datetime.date(2022, 1, 2))
        transaction3 = Transaction.objects.create(user=user, transaction_type='Expense', amount=25, date_paid=datetime.date(2022, 1, 3))
        # Make a request to the view
        request = HttpRequest()
        request.user = user
        response = chart_expense_graph(request)
        data = json.loads(response.content.decode('utf-8'))
        # Check that the labels and data are correct
        self.assertEqual(data['labels'], ['01/01/2022', '01/02/2022', '01/03/2022'])
        self.assertEqual(data['data'], [0, 50, 25])

    #def test_chart_income_graph(self):
        # Create some sample transactions
        self.client.login(username=self.user.username, password='Password123')
        transaction1 = Transaction.objects.create(user=user, transaction_type='Income', amount=100, date_paid=datetime.date(2022, 1, 1))
        transaction2 = Transaction.objects.create(user=user, transaction_type='Expense', amount=50, date_paid=datetime.date(2022, 1, 2))
        transaction3 = Transaction.objects.create(user=user, transaction_type='Expense', amount=25, date_paid=datetime.date(2022, 1, 3))
        # Make a request to the view
        request = HttpRequest()
        request.user = user
        response = chart_income_graph(request)
        data = json.loads(response.content.decode('utf-8'))
        # Check that the labels and data are correct
        self.assertEqual(data['labels'], ['01/01/2022', '01/02/2022', '01/03/2022'])
        self.assertEqual(data['data'], [100, 0, 0])
    
    #def test_expense_structure_with_transactions(self):
        # Create test user
        self.client.login(username=self.user.username, password='Password123')
        # Create test transactions
        Transaction.objects.create(user=user, transaction_type='Expense', category='Food', amount=10.0)
        Transaction.objects.create(user=user, transaction_type='Expense', category='Food', amount=20.0)
        Transaction.objects.create(user=user, transaction_type='Expense', category='Rent', amount=100.0)
        # Log in the user
        self.client.login(username='testuser', password='testpass')
        # Make a request to the view
        response = self.client.get(reverse('expense_structure_with_transactions'))
        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        # Check that the response contains the expected categories and amounts
        self.assertContains(response, '<td>Food</td><td>$30.00</td>', html=True)
        self.assertContains(response, '<td>Rent</td><td>$100.00</td>', html=True)


    #def test_expense_structure_with_no_transactions():
        expense_structure = ExpenseStructure('Groceries')
        assert expense_structure.name == 'Groceries'
        assert expense_structure.total() == 0
        assert expense_structure.average() == 0
        assert expense_structure.min() == None
        assert expense_structure.max() == None
        assert expense_structure.transactions == []

    



    
    #def test_filter_transactions_by_date_range(self):
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
        self.assertTemplateUsed(response, 'records.html')
        self.assertIn(transaction1, response.context['transactions'])
        self.assertNotIn(transaction2, response.context['transactions'])


    # def test_get_pending_transaction_redirects_when_not_logged_in(self): //WHEN LOGIN REQUIRED IS ADDED WE CAN CHANGE THIS
    #     redirect_url = reverse_with_next('log_in', self.url)
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)




