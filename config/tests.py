from django.test import TestCase


class WsgiTestCase(TestCase):
    def test_wsgi(self):
        from .wsgi import application
