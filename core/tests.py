from django.shortcuts import reverse
from django.test import TestCase
from datetime import date
from django.test.client import Client

from . import context_processor, apps


class AppsTestCase(TestCase):
    def test_apps(self):
        self.assertEqual(type(apps.AppConfig), type)


class ContextProcessorTestCase(TestCase):
    client = Client()

    def test_date_to_str(self):
        self.assertEqual(
            type(context_processor.date_to_str(date(2000, 1, 1))),
            str
            )

    def test_str_to_date(self):
        self.assertEqual(
            type(context_processor.str_to_date("2000-01-01")),
            date
            )

    def test_default(self):
        response = self.client.get("/")
        request = response.wsgi_request
        default_context = context_processor.default(request)
        self.assertTrue(
            all([x in default_context.keys()
                 for x in ['time_range_form', 'from', 'to']])
            )


class StartViewTestCase(TestCase):
    client = Client()

    def test_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'start.html')


class DateSetViewTestCase(TestCase):
    client = Client()

    def test_post(self):
        post_data = {'from': '2018-01-01', 'to': '2018-01-31', 'next': '/'}
        response = self.client.post(reverse('set-date'), post_data)
        self.assertRedirects(response, post_data['next'], 302)
