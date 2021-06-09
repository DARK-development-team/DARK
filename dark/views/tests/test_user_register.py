from django.test import TestCase
from django.urls import reverse

from dark.models.user import User

class UserRegisterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_register_url_exists(self):
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_url_template_correct(self):
        response = self.client.get(reverse('user:register'))
        self.assertTemplateUsed(response, template_name='dark/user/register.html')

    def test_register_url_get_inaccessible_logged_in(self):
        user = User.objects.create_user(username='MrTester', password='pass1234')
        self.client.login(username='MrTester', password='pass1234')
        response = self.client.get(reverse('user:register'))
        self.assertRedirects(response, reverse('home:page'))

    def test_register_registration_denied_logged_in(self):
        user = User.objects.create_user(username='MrTester', password='pass1234')
        self.client.login(username='MrTester', password='pass1234')
        response = self.client.post(reverse('user:register'), data={
            'username': 'MrSandman',
            'email': 'testable@gmail.com',
            'password1': '$hElEl1234',
            'password2': '$hElEl1234',
        })
        self.assertRedirects(response, reverse('home:page'))

    def test_registration_logs_in(self):
        self.client.post(reverse('user:register'), data={
            'username': 'MrTester',
            'email': 'testable@gmail.com',
            'password1': '$hElEl1234',
            'password2': '$hElEl1234',
        })
        self.assertEqual(User.objects.all().count(), 1)

    def test_registration_redirects(self):
        response = self.client.post(reverse('user:register'), data={
            'username': 'MrTester',
            'email': 'testable@gmail.com',
            'password1': '$hElEl1234',
            'password2': '$hElEl1234',
        })
        self.assertRedirects(response, reverse('home:page'))
