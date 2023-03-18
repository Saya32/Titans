"""Tests of the log in view."""
from django.contrib import messages
from django.test import TestCase
from django.contrib.auth.hashers import check_password, make_password
from django.urls import reverse
from spendingtrackers.forms import ChangePasswordForm
from spendingtrackers.models import User
from spendingtrackers.tests.helpers import LogInTester, reverse_with_next
from django.test.client import Client


# class ChangePasswordViewTestCase(TestCase, LogInTester):
#     """Tests of the change password in view."""

#     fixtures = ['spendingtrackers/tests/fixtures/default_user.json']

#     def setUp(self):
#         self.url = reverse('change_password')
#         self.form_input = {
#             'email': 'johndoe@example.org',
#             'his_password': 'password',
#             'password': 'new_password',
#             'password_confirmation': 'new_password'
#         }
#         self.user = User.objects.get(username='johndoe@example.org')

#     def test_change_password_url(self):
#         self.assertEqual(self.url, '/change_password/')

#     def test_change_password(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'change_password.html')
#         form = response.context['form']
#         self.assertTrue(isinstance(form, ChangePasswordForm))
#         self.assertFalse(form.is_bound)

#     def test_change_password_successful(self):
#         form_input = {'email': 'johndoe@example.org', 'his_password': 'WrongP@ssword123.',
#                       'password': 'WrongP@ssword12345,', "password_confirmation": "WrongP@ssword12345,"}

#         response = self.client.get(self.url, form_input)
#         self.assertEqual(response.status_code, 200)
        
#     def test_change_password_unsuccessful(self):
#         form_input = {'email': 'johndoe@example.org', 'his_password': 'WrongPassword123.',
#                       'password': 'WrongPassword12345,', "password_confirmation": "WrongPassw22ord1234,5"}
#         response = self.client.post(self.url, form_input)
#         messages_list = list(response.context['messages'])
#         self.assertNotEqual(len(messages_list), 1)

#     def test_change_password_unsuccessful_by_his(self):
#         form_input = {'username': 'johndoe@example.org', 'his_password': 'WrongPass22word123.',
#                       'password': 'WrongPassword12,345', "password_confirmation": "WrongPasswo,rd12345"}
#         response = self.client.post(self.url, form_input)
#         messages_list = list(response.context['messages'])
#         self.assertNotEqual(len(messages_list), 1)

#     def test_change_password_unsuccessful_by_user_name(self):
#         form_input = {'username': 'johndoe@exam22ple.org', 'his_password': 'WrongPass22word123.',
#                       'password': 'WrongPassword1234,5', "password_confirmation": "WrongPa,ssword12345"}
#         response = self.client.post(self.url, form_input)
#         messages_list = list(response.context['messages'])
#         self.assertNotEqual(len(messages_list), 1)

class ChangePasswordViewTestCase(TestCase):
    """Tests of the change password in view."""

    fixtures = ['spendingtrackers/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('change_password')
        self.user = User.objects.get(username='johndoe@example.org')

    def test_change_password_url(self):
        self.assertEqual(self.url, '/change_password/')

    def test_change_password_success(self):
        c = Client()
        c.login(username='johndoe@example.org', password='password')
        response = c.post(self.url, {'email': 'johndoe@example.org', 'his_password': 'password', 'password': 'new_password', 'password_confirmation': 'new_password'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')

    def test_change_password_inconsistent_passwords(self):
        c = Client()
        c.login(username='johndoe@example.org', password='password')
        response = c.post(self.url, {'email': 'johndoe@example.org', 'his_password': 'password', 'password': 'new_password', 'password_confirmation': 'new_password_wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The two passwords are inconsistent!")

    def test_change_password_email_not_exists(self):
        c = Client()
        c.login(username='johndoe@example.org', password='password')
        response = c.post(self.url, {'email': 'not_exists@example.org', 'his_password': 'password', 'password': 'new_password', 'password_confirmation': 'new_password'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "email not exists!")

    def test_change_password_history_password_error(self):
        c = Client()
        c.login(username='johndoe@example.org', password='password')
        response = c.post(self.url, {'email': 'johndoe@example.org', 'his_password': 'wrong_password', 'password': 'new_password', 'password_confirmation': 'new_password'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "history password error!")

    def test_change_password_form(self):
        form_data = {'email': 'johndoe@example.org', 'his_password': 'password', 'password': 'new_password', 'password_confirmation': 'new_password'}
        form = ChangePasswordForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {'email': 'johndoe@example.org', 'his_password': 'password', 'password': 'new_password', 'password_confirmation': 'new_password_wrong'}
        form = ChangePasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password_confirmation'], ['Confirmation does not match password.'])