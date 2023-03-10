from django.test import TestCase
from django.urls import reverse
from spendingtrackers.models import User, Category
from spendingtrackers.forms import CategoryDetailsForm
from spendingtrackers.tests.helpers import reverse_with_next, create_categories

class UpdateCategoryViewTestCase(TestCase):
    """Test case of edit category view"""
    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
    ]
    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.data = {
            'name':'Gifts',
            'budget':1000,
            'start_date':'2022-12-12',
            'end_date': '2023-12-12'
        }
        create_categories(self.user,1,3)
        self.categories = Category.objects.filter(user = self.user)

    def test_edit_category_details_displays_correct_page(self):
        self.client.login(username=self.user.username, password='Password123')
        category_url = reverse('edit_category_details', kwargs={'id': self.categories[0].pk})
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_category_details.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CategoryDetailsForm))
        self.assertContains(response, "")

    def test_redirect_with_incorrect_category_id(self):
        self.client.login(username=self.user.username, password='Password123')
        category_url = reverse('edit_category_details', kwargs={'id': (Category.objects.count()) +1})
        redirect_url = reverse('category')
        response = self.client.get(category_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'category.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_update_correctly_saves(self):
        self.client.login(username=self.user.username, password='Password123')
        category_url = reverse('edit_category_details', kwargs={'id': self.categories[0].pk})
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_category_details.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CategoryDetailsForm))
        self.assertContains(response, "2022-12-12")

        before_count = Category.objects.count()
        update_response = self.client.post(category_url, self.data, follow=True)
        after_count = Category.objects.count()
        self.assertEqual(before_count, after_count)

        self.assertEqual(update_response.status_code, 200)
        self.assertTemplateUsed(update_response, 'category.html')
        messages_list = list(update_response.context['messages'])
        self.assertEqual(len(messages_list), 1)

        self.categories = Category.objects.filter(user = self.user)
        self.assertEqual(self.categories[0].budget, 1000)

    def test_update_does_not_save_if_form_is_invalid(self):
        self.client.login(username=self.user.username, password='Password123')
        category_url = reverse('edit_category_details', kwargs={'id': self.categories[0].pk})
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_category_details.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CategoryDetailsForm))
        self.assertContains(response, "2023-12-12")

        self.data['budget'] ='a'

        before_count = Category.objects.count()
        update_response = self.client.post(category_url, self.data, follow=True)
        after_count = Category.objects.count()
        self.assertEqual(before_count, after_count)

        self.assertEqual(update_response.status_code, 200)
        self.assertTemplateUsed(update_response, 'edit_category_details.html')
        
        self.categories = Category.objects.filter(user = self.user)
        self.assertEqual(self.categories[0].budget, 1000)