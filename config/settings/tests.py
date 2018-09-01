from django.test import TestCase


class SettingsProduction(TestCase):
    def test_vars(self):
        from .production import DEBUG
