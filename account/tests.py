""" Tests for account module """
from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User

from config.tests import TestBase
from . import apps


class AppsTestCase(TestCase):
    """ Tests for apps config """

    def test_apps(self):
        """ checkt type """
        self.assertEqual(type(apps.AppConfig), type)


class AccountViewsTestCase(TestCase):
    """ Tests for account views """

    def setUp(self):
        testbase = TestBase()
        self.client = testbase.client
        self.db_ = testbase.db_

    def test_get_signup(self):
        """ check for template used at get signup """
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_post_signup(self):
        """ check for template used at post signup """
        response = self.client.post(reverse('signup'), {
            'username': ['test1'],
            'password1': ['QWERasdf1234'],
            'password2': ['QWERasdf1234'],
        })
        self.assertRedirects(response, '/', 302)
        self.assertIs(len(User.objects.filter(username='test1')), 1)
