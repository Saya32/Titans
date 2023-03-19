"""Tests of the log in view."""
from django.contrib import messages
from django.contrib.messages import ERROR
from django.test import TestCase
from django.urls import reverse
from spendingtrackers.models import User
from spendingtrackers.tests.helpers import LogInTester, reverse_with_next
from django.contrib.auth.hashers import make_password, check_password


class ChangePasswordViewTestCase(TestCase, LogInTester):
    """Tests of the update password in view."""

    fixtures = ['spendingtrackers/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('change_password')
        self.user = User.objects.get(username='johndoe@example.org')

    def test_change_password_url(self):
        self.assertEqual(self.url, '/change_password/')

    def test_change_password(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)


    def test_change_password_error(self):
        form_input = {"pin": "johndoe@example.org", 'email': 'johndoe@example.org', 'password': 'aaa1',
                      "password_confirmation": "aaa"}

        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)


# class ChangePasswordViewTestCase(TestCase, LogInTester):
#     """Tests of the change password in view."""

#     fixtures = ['spendingtrackers/tests/fixtures/default_user.json']

#     def setUp(self):
#         self.url = reverse('change_password')
#         self.user = User.objects.get(username='johndoe@example.org')

#     def test_change_password_url(self):
#         self.assertEqual(self.url, '/change_password/')
    
#     def test_change_password_success(self):
#         self.log_in()
#         data = {
#             'email': self.user.username,
#             'his_password': 'test1234',
#             'password': 'newpassword1234',
#             'password_confirmation': 'newpassword1234'
#         }
#         response = self.client.post(self.url, data=data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'log_in.html')
#         messages_list = list(response.context['messages'])
#         self.assertEqual(len(messages_list), 0)

#     def test_change_password_failure(self):
#         self.log_in()
#         data = {
#             'email': self.user.username,
#             'his_password': 'wrongpassword',
#             'password': 'newpassword1234',
#             'password_confirmation': 'newpassword1234'
#         }
#         response = self.client.post(self.url, data=data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'change_password.html')
#         messages_list = list(response.context['messages'])
#         self.assertEqual(len(messages_list), 1)
#         self.assertEqual(str(messages_list[0]), 'history password error!')

    # def test_change_password(self):
    #     response = self.client.post(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'change_password.html')
    #     messages_list = list(response.context['messages'])
    #     self.assertEqual(len(messages_list), 0)


    # def test_change_password_successful(self):
    #     form_input = {'email': 'johndoe@example.org', 'his_password': 'WrongPassword123.',
    #                   'password': 'WrongPassword12345,', "password_confirmation": "WrongPassword12345,"}

    #     response = self.client.get(self.url, form_input)
    #     self.assertEqual(response.status_code, 200)
        
    # def test_change_password_unsuccessful(self):
    #     form_input = {'email': 'johndoe@example.org', 'his_password': 'WrongPassword123.',
    #                   'password': 'WrongPassword12345,', "password_confirmation": "WrongPassw22ord1234,5"}
    #     response = self.client.post(self.url, form_input)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'The two passwords are inconsistent!')
    #     messages_list = list(response.context['messages'])
    #     self.assertEqual(len(messages_list), 1)
    #     self.assertEqual(messages_list[0].level, messages.ERROR)

    # def test_change_password_unsuccessful_by_his(self):
    #     form_input = {'username': 'johndoe@example.org', 'his_password': 'WrongPass22word123.',
    #                   'password': 'WrongPassword12,345', "password_confirmation": "WrongPasswo,rd12345"}
    #     response = self.client.post(self.url, form_input)
    #     messages_list = list(response.context['messages'])
    #     self.assertNotEqual(len(messages_list), 1)

    # def test_change_password_unsuccessful_by_user_name(self):
    #     form_input = {'username': 'johndoe@exam22ple.org', 'his_password': 'WrongPass22word123.',
    #                   'password': 'WrongPassword1234,5', "password_confirmation": "WrongPa,ssword12345"}
    #     response = self.client.post(self.url, form_input)
    #     messages_list = list(response.context['messages'])
    #     self.assertNotEqual(len(messages_list), 1)

    # def test_change_password_error(self):
    #     form_input = {'username': 'johndoe2@exam22ple.org', 'his_password': 'WrongPass22word123.',
    #                   'password': 'WrongPassword1234,5', "password_confirmation": "WrongPassword1234,5"}
    #     response = self.client.post(self.url, form_input)
    #     messages_list = list(response.context['messages'])
    #     self.assertNotEqual(len(messages_list), 1)