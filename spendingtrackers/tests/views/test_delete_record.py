from django.test import TestCase
from django.urls import reverse
from spendingtrackers.models import User, Transaction
from spendingtrackers.tests.helpers import reverse_with_next

class DeleteTransactionViewTestCase(TestCase):
    """Test case of delete transaction view"""
    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.transactionData = Transaction(
             user=self.user,
            title = 'This is a title',
            description = 'Description of Transaction goes here',
            amount = 1000,
            date_paid = '2023-12-12',
            time_paid = '10:51',
            category = 'Salary',
            receipt = '',
            transaction_type ='Expense'
        )
        self.transactions = Transaction.objects.filter(user = self.user)

    def test_delete_transaction_redirects_correctly(self):
        self.client.login(username=self.user.username, password='Password123')
        self.transactionData.save()
        transaction_url = reverse('delete_record', kwargs={'id': self.transactions[0].pk})
        redirect_url = reverse('feed')
        response = self.client.get(transaction_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_delete_transaction_deletes_correct_transaction(self):
        self.client.login(username=self.user.username, password='Password123')
        self.transactionData.save()
        before_count = Transaction.objects.count()
        pk = self.transactions[0].pk
        transaction_url = reverse('delete_record', kwargs={'id': pk})
        redirect_url = reverse('feed')
        response = self.client.get(transaction_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        after_count = Transaction.objects.count()
        self.assertEqual(before_count - 1, after_count)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

        transaction_url = reverse('update_record', kwargs={'id': pk})
        redirect_url = reverse('feed')
        response = self.client.get(transaction_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_delete_transaction_redirects_if_not_found(self):
        self.client.login(username=self.user.username, password='Password123')
        transaction_url = reverse('delete_record', kwargs={'id': (Transaction.objects.count()) +1})
        redirect_url = reverse('feed')
        response = self.client.get(transaction_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)