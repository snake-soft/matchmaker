from django.test import TestCase

from . import apps


class AppsTestCase(TestCase):

    def test_apps(self):
        self.assertEqual(type(apps.AppConfig), type)
