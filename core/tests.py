""" tests for core module """
from datetime import date

from django.shortcuts import reverse
from django.test import TestCase
from django.test.client import Client

from config.tests import TestBase
from . import context_processor, apps


class AppsTestCase(TestCase):
    """ core apps config """

    def test_apps(self):
        """ checkt type """
        self.assertIs(type(apps.AppConfig), type)


class ContextProcessorTestCase(TestCase):
    """ test default context processor """
    client = Client()

    def test_date_to_str(self):
        """ test date to str conversion """
        self.assertIs(
            type(context_processor.date_to_str(date(2000, 1, 1))),
            str
        )

    def test_str_to_date(self):
        """ test str to date conversion """
        self.assertIs(
            type(context_processor.str_to_date("2000-01-01")),
            date
        )

    def test_default(self):
        """ test default context """
        response = self.client.get("/")
        request = response.wsgi_request
        default_context = context_processor.default(request)
        self.assertTrue(
            all([x in default_context.keys()
                 for x in ['time_range_form', 'from', 'to']])
        )


class StartViewTestCase(TestCase):
    """ test start view (home) """

    def setUp(self):
        """ setup StartViewTestCase """
        testbase = TestBase()
        self.client = testbase.client
        self.db_ = testbase.db_

    def test_get_home(self):
        """ test get home """
        response = self.client.get('/')
        self.assertIs(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class DateSetViewTestCase(TestCase):
    """ Date setter test """

    def setUp(self):
        """ setup """
        testbase = TestBase()
        self.client = testbase.client
        self.db_ = testbase.db_

    def test_post(self):
        """ test date setting post """
        post_data = {'frm': '2018-01-01', 'to': '2018-01-31', 'next': '/'}
        response = self.client.post(reverse('set-date'), post_data)
        self.assertRedirects(response, post_data['next'], 302)
