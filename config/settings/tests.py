""" tests for the settings module """
from django.test import TestCase


class SettingsProduction(TestCase):
    """ test production settings """

    def test_vars(self):
        """ Test the vars """
        from .production import DEBUG
        _ = DEBUG
        _ = self
