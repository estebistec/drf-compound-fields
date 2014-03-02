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

from drf_compound_fields.fields import DictField
from drf_compound_fields.fields import ListField


class TestSerializerListField(unittest.TestCase):
    """
    Tests for the ListField behavior in a declared serializer.
    """

    class Serializer(serializers.Serializer):
        emails = ListField(serializers.EmailField(), required=False)

    def test_non_list(self):
        serializer = self.Serializer(data={'emails': 'notAList'})
        self.assertFalse(serializer.is_valid(), 'Non-list value allowed')
        self.assertIn('emails', serializer.errors, 'No error for non-list value')
        self.assertTrue(serializer.errors['emails'], 'Empty error for non-list value')

    def test_invalid_list_item(self):
        serializer = self.Serializer(data={'emails': ['some.where@out.there', 'notAnEmail']})
        self.assertFalse(serializer.is_valid(), 'Invalid list-item allowed')
        self.assertIn('emails', serializer.errors, 'No error for invalid list-item')
        self.assertTrue(serializer.errors['emails'], 'Empty error for invalid list-item {}'.format(
                serializer.errors['emails']))

    def test_empty_list(self):
        serializer = self.Serializer(data={'emails': []})
        self.assertTrue(serializer.is_valid())

    def test_valid_list(self):
        serializer = self.Serializer(data={'emails': ['some.where@out.there']})
        self.assertTrue(serializer.is_valid())
