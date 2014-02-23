#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
test_in_serializers
-------------------

Tests of the fields cooperation in the serializer interfaces for serialization, de-serialization,
and validation.

"""


# Django settings:
import os
os.environ['DJANGO_SETTINGS_MODULE'] = __name__

from django.conf.global_settings import CACHES
SECRET_KEY = 's3cr3t'


import unittest

from rest_framework import serializers
from rest_framework.compat import six

from drf_compound_fields.fields import DictField
from drf_compound_fields.fields import ListField


class DemoSerializer(serializers.Serializer):
    name = ListField(serializers.CharField(), required=False)
    emails = ListField(serializers.EmailField(), required=False)


class TestSerializerListField(unittest.TestCase):
    """
    Tests for the ListField behavior
    """

    def test_non_list_not_valid(self):
        serializer = DemoSerializer(data={'name': 'notAList'})
        self.assertFalse(serializer.is_valid())

    def test_non_list_errors(self):
        serializer = DemoSerializer(data={'name': 'notAList'})
        self.assertIn('name', serializer.errors)
        self.assertTrue(serializer.errors['name'], six.text_type)
