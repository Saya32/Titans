"""Tests of the log in view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from spendingtrackers.forms import ChangePasswordForm
from spendingtrackers.models import User
from spendingtrackers.tests.helpers import LogInTester, reverse_with_next
from django.contrib.messages import get_messages

class ChangePasswordViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
        )
        self.url = reverse('change_password')
    
    def test_password_mismatch(self):
        data = {
            'email': self.user.username,
            'his_password': 'password',
            'password': 'newpassword1',
            'password_confirmation': 'newpassword2'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        messages = [str(m) for m in get_messages(response.wsgi_request)]
        self.assertIn('The two passwords are inconsistent!', messages)
        
    def test_invalid_email(self):
        data = {
            'email': 'invalidemail',
            'his_password': 'password',
            'password': 'newpassword1',
            'password_confirmation': 'newpassword1'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        messages = [str(m) for m in get_messages(response.wsgi_request)]
        self.assertIn('email not exists!', messages)
        
    def test_invalid_password(self):
        data = {
            'email': self.user.username,
            'his_password': 'invalidpassword',
            'password': 'newpassword1',
            'password_confirmation': 'newpassword1'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        messages = [str(m) for m in get_messages(response.wsgi_request)]
        self.assertIn('history password error!', messages)
        
    def test_successful_password_change(self):
        data = {
            'email': self.user.username,
            'his_password': 'password',
            'password': 'newpassword1',
            'password_confirmation': 'newpassword1'
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('log_in'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword1'))


# class ChangePasswordViewTestCase(TestCase, LogInTester):
#     """Tests of the change password in view."""

#     fixtures = ['spendingtrackers/tests/fixtures/default_user.json']

#     def setUp(self):
#         self.url = reverse('change_password')
#         self.form_input = {
#             'email': 'chuliang.li@kcl.ac.uk',
#             'his_password': 'Password123*',
#             'password': 'Password123#',
#             'password_confirmation': 'Password123#'
#         }
#         self.user = User.objects.get(username='johndoe@example.org')

#     def test_change_password_url(self):
#         self.assertEqual(self.url, '/change_password/')

#     def test_change_password(self):
#         response = self.client.post(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'change_password.html')
#         form = response.context['form']
#         self.assertTrue(isinstance(form, ChangePasswordForm))
#         self.assertFalse(form.is_bound)
#         messages_list = list(response.context['messages'])
#         self.assertEqual(len(messages_list), 0)
    
#     def test_form_invalid_when_email_field_empty(self):
#         form_data = {
#             'email': '',
#             'his_password': 'Password123*',
#             'password': 'Password123#',
#             'password_confirmation': 'Password123#'
#         }
#         response = self.client.post(self.url, data=form_data)
#         form = response.context['form']
#         self.assertFalse(form.is_valid())
#         self.assertIn('email', form.errors)
    
#     def test_form_invalid_when_password_field_empty(self):
#         form_data = {
#             'email': 'chuliang.li@kcl.ac.uk',
#             'his_password': 'Password123*',
#             'password': '',
#             'password_confirmation': 'Password123#'
#         }
#         response = self.client.post(self.url, data=form_data)
#         form = response.context['form']
#         self.assertFalse(form.is_valid())
#         self.assertIn('password', form.errors)
    
#     def test_form_invalid_when_password_field_empty(self):
#         form_data = {
#             'email': 'chuliang.li@kcl.ac.uk',
#             'his_password': '',
#             'password': 'Password123#',
#             'password_confirmation': 'Password123#'
#         }
#         response = self.client.post(self.url, data=form_data)
#         form = response.context['form']
#         self.assertFalse(form.is_valid())
#         self.assertIn('his_password', form.errors)
    
#     def test_form_invalid_when_passwords_do_not_match(self):
#         form_data = {
#             'email': 'chuliang.li@kcl.ac.uk',
#             'his_password': 'Password123*',
#             'password': 'Password123#',
#             'password_confirmation': 'password'
#         }
#         response = self.client.post(self.url, data=form_data)
#         form = response.context['form']
#         self.assertFalse(form.is_valid())
#         self.assertIn('password_confirmation', form.errors)
    
#     def test_form_invalid_when_his_password_field_empty(self):
#         form_data = {
#             'email': 'chuliang.li@kcl.ac.uk',
#             'his_password': '',
#             'password': 'Password123#',
#             'password_confirmation': 'Password123#'
#         }
#         response = self.client.post(self.url, data=form_data)
#         form = response.context['form']
#         self.assertFalse(form.is_valid())
#         self.assertIn('his_password', form.errors)
    
#     def test_password_mismatch(self):
        
#         self.client.login(username='testuser', password='oldpassword')
        
#         data = {
#             'email': 'testuser@example.com',
#             'his_password': 'oldpassword',
#             'password': 'newpassword',
#             'password_confirmation': 'wrongpassword',
#         }
#         response = self.client.post(self.url, data)
        
#         # Check that the response contains the error message
#         self.assertContains(response, "The two passwords are inconsistent!")
#         # Check that the message was added to the messages framework
#         messages = response.context['messages']
#         self.assertEqual(list(messages)[0].message, "The two passwords are inconsistent!")
        
#         # Check that the password was not changed in the database
#         self.user.refresh_from_db()
#         self.assertTrue(self.user.check_password('oldpassword'))






#     # def test_change_password_unsuccessful(self):
#     #     form_input = {'email': 'johndoe@example.org', 'his_password': 'WrongPassword123.',
#     #                   'password': 'WrongPassword12345,', "password_confirmation": "WrongPassw22ord1234,5"}
#     #     response = self.client.post(self.url, form_input)
#     #     messages_list = list(response.context['messages'])
#     #     self.assertNotEqual(len(messages_list), 1)

#     # def test_change_password_unsuccessful_by_his(self):
#     #     form_input = {'username': 'johndoe@example.org', 'his_password': 'WrongPass22word123.',
#     #                   'password': 'WrongPassword12,345', "password_confirmation": "WrongPasswo,rd12345"}
#     #     response = self.client.post(self.url, form_input)
#     #     messages_list = list(response.context['messages'])
#     #     self.assertNotEqual(len(messages_list), 1)

#     # def test_change_password_unsuccessful_by_user_name(self):
#     #     form_input = {'username': 'johndoe@exam22ple.org', 'his_password': 'WrongPass22word123.',
#     #                   'password': 'WrongPassword1234,5', "password_confirmation": "WrongPa,ssword12345"}
#     #     response = self.client.post(self.url, form_input)
#     #     messages_list = list(response.context['messages'])
#     #     self.assertNotEqual(len(messages_list), 1)
   