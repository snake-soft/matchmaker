from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User

from config.tests import TestBase
from . import apps


class AppsTestCase(TestCase):

    def test_apps(self):
        self.assertEqual(type(apps.AppConfig), type)


class AccountViewsTestCase(TestCase):
    def setUp(self):
        tb = TestBase()
        self.client = tb.client
        self.db = tb.db

    def test_get_signup(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_post_signup(self):
        response = self.client.post(reverse('signup'), {
            'username': ['test1'],
            'password1': ['QWERasdf1234'],
            'password2': ['QWERasdf1234'],
            })
        self.assertRedirects(response, '/', 302)
        self.assertIs(len(User.objects.filter(username='test1')), 1)
