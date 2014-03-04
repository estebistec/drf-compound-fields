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
        self.assertFalse(serializer.is_valid(), 'Non-list value should not be allowed')
        self.assertIn('emails', serializer.errors, 'Non-list value should produce a field error')
        self.assertTrue(serializer.errors['emails'], 'Non-list value error should be non-empty')

    def test_invalid_list_item(self):
        serializer = self.Serializer(data={'emails': ['some.where@out.there', 'notAnEmail']})
        self.assertFalse(serializer.is_valid(), 'Invalid list-item should not be allowed')
        self.assertIn('emails', serializer.errors,
                'Invalid list-item should produce a field error')
        self.assertTrue(serializer.errors['emails'],
                'Invalid list-item errors should be non-empty {}'.format(
                        serializer.errors['emails']))
        self.assertTrue([error for error in serializer.errors['emails'] if error],
                'Invalid dict-value errors should each be non-empty {}'.format(
                        serializer.errors['emails']))

    def test_empty_list(self):
        serializer = self.Serializer(data={'emails': []})
        self.assertTrue(serializer.is_valid(), 'Empty list should be allowed')

    def test_valid_list(self):
        serializer = self.Serializer(data={'emails': ['some.where@out.there']})
        self.assertTrue(serializer.is_valid(), 'Valid list should be allowed')


class TestSerializerDictField(unittest.TestCase):
    """
    Tests for the DictField behavior in a declared serializer.
    """

    class Serializer(serializers.Serializer):
        emails = DictField(serializers.EmailField(), required=False)

    def test_non_dict(self):
        serializer = self.Serializer(data={'emails': 'notADict'})
        self.assertFalse(serializer.is_valid(), 'Non-dict value should not be allowed')
        self.assertIn('emails', serializer.errors, 'Non-dict value should produce a field error')
        self.assertTrue(serializer.errors['emails'], 'Non-dict value error should be non-empty')

    def test_invalid_dict_value(self):
        serializer = self.Serializer(data={'emails': {'a': 'some.where@out.there',
                'b': 'notAnEmail'}})
        self.assertFalse(serializer.is_valid(), 'Invalid dict-value should not be allowed')
        self.assertIn('emails', serializer.errors,
                'Invalid dict-value should produce a field error')
        self.assertTrue(serializer.errors['emails'],
                'Invalid dict-value errors should be non-empty {}'.format(
                        serializer.errors['emails']))
        self.assertTrue([error for error in serializer.errors['emails'] if error],
                'Invalid dict-value errors should each be non-empty {}'.format(
                        serializer.errors['emails']))

    def test_empty_dict(self):
        serializer = self.Serializer(data={'emails': {}})
        self.assertTrue(serializer.is_valid(), 'Empty dict should be allowed')

    def test_valid_dict(self):
        serializer = self.Serializer(data={'emails': {'a': 'some.where@out.there'}})
        self.assertTrue(serializer.is_valid(), 'Valid dict shouild be allowed')
