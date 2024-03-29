from django.test import TestCase
from django.urls import reverse
from spendingtrackers.models import User, Category, Transaction
from spendingtrackers.helpers import delete_transactions


class DeleteCategoryViewTestCase(TestCase):
    """Test case of delete category view"""
    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.categoryData = Category(
            user=self.user,
            name='Gifts',
            budget=1000,
            start_date='2023-12-12',
            end_date='2024-12-12',
        )
        self.categories = Category.objects.filter(user = self.user)

    def test_delete_category_redirects_correctly(self):
        self.client.login(username=self.user.username, password='Password123')
        self.categoryData.save()
        category_url = reverse('delete_category', kwargs={'id': self.categories[0].pk})
        redirect_url = reverse('feed')
        response = self.client.get(category_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_delete_category_deletes_correct_category(self):
        self.client.login(username=self.user.username, password='Password123')
        self.categoryData.save()
        before_count = Category.objects.count()
        pk = self.categories[0].pk
        category_url = reverse('delete_category', kwargs={'id': pk})
        redirect_url = reverse('feed')
        response = self.client.get(category_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        after_count = Category.objects.count()
        self.assertEqual(before_count - 1, after_count)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

        category_url = reverse('update_record', kwargs={'id': pk})
        redirect_url = reverse('feed')
        response = self.client.get(category_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_delete_category_redirects_if_not_found(self):
        self.client.login(username=self.user.username, password='Password123')
        category_url = reverse('delete_category', kwargs={'id': (Category.objects.count()) +1})
        redirect_url = reverse('feed')
        response = self.client.get(category_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
    
    def test_transactions_delete_when_category_deletes(self):
        self.client.login(username=self.user.username, password='Password123')
        self.categoryData.save()
        self.transactionData = Transaction(
            user=self.user,
            title='This is a title',
            description='Description of Transaction goes here',
            amount=1000,
            date_paid='2023-12-12',
            time_paid='10:51',
            category='Gifts',
            receipt ='',
            transaction_type='Expense',
            category_fk=self.categories[0]

        )
        pk = self.categories[0].pk
        category_url = reverse('delete_category', kwargs={'id': pk})
        delete_transactions(self.user, self.categories[0])
        transaction_count = Transaction.objects.count()
        self.assertEqual(transaction_count,0)
        

