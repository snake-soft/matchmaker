""" Test module for templatetags """
from types import SimpleNamespace
from django.test import TestCase

from . import attrib_get, join_by_attr, dict_get, list_get, signed


class TemplatetagsTestcase(TestCase):
    """ templatetags tests """

    def setUp(self):
        """ setup creates testobjects """
        self.obj1 = SimpleNamespace(color='red')
        self.obj2 = SimpleNamespace(color='green')
        self.obj3 = SimpleNamespace(color='blue')

    def test_attrib_get(self):
        """ test attrib_get tag """
        attrib_get.attrib_get(self.obj1, 'color')

    def test_join_by_attr(self):
        """ test join_by_attr tag """
        the_list = [self.obj1, self.obj2, self.obj3]
        join_by_attr.join_by_attr(the_list, "color", ". ")

    def test_dict_get(self):
        """ test dict_get tag """
        the_dict = {
            1: self.obj1,
            2: self.obj2,
            3: self.obj3,
        }
        dict_get.dict_get(the_dict, 2)

    @staticmethod
    def test_list_get():
        """ test list_get tag """
        the_list = ["1", "2", "3", "4"]
        list_get.list_get(the_list, 2)

    @staticmethod
    def test_signed():
        """ test signed tag """
        signed.signed("1")
        signed.signed(100)
        signed.signed(-1000)
        signed.signed(-1000.0)
