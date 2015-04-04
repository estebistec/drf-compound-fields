#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
test_in_serializers
-------------------

Tests of the fields cooperation in the serializer interfaces for serialization, de-serialization,
and validation.

"""


from . import test_settings

from rest_framework import serializers
from rest_framework.compat import six

from drf_compound_fields.fields import DictField
from drf_compound_fields.fields import ListField
from drf_compound_fields.fields import ListOrItemField


class ListSerializer(serializers.Serializer):
    emails = ListField(serializers.EmailField(), required=False)


class EmbeddedSerializer(serializers.Serializer):
    value = serializers.EmailField()


class ContainerListSerializer(serializers.Serializer):
    embedded = ListField(EmbeddedSerializer())


class ContainerSerializer(serializers.Serializer):
    embedded = ListOrItemField(EmbeddedSerializer())


def test_non_list():
    serializer = ListSerializer(data={'emails': 'notAList'})
    assert not serializer.is_valid(), 'Non-list value should not be allowed'
    assert 'emails' in serializer.errors, 'Non-list value should produce a field error'
    assert serializer.errors['emails'], 'Non-list value error should be non-empty'


def test_invalid_list_item():
    serializer = ListSerializer(data={'emails': ['some.where@out.there', 'notAnEmail']})
    assert not serializer.is_valid(), 'Invalid list-item should not be allowed'
    assert 'emails' in serializer.errors, 'Invalid list-item should produce a field error'
    assert serializer.errors['emails'], 'Invalid list-item errors should be non-empty {0}'.format(
        serializer.errors['emails'])
    assert [1] == list(six.iterkeys(serializer.errors['emails'][0]))


def test_invalid_embedded_list():
    assert not ContainerSerializer(data={'embedded': [{'value': 'notAnInteger'}]}).is_valid()


def test_invalid_embedded_item():
    assert not ContainerSerializer(data={'embedded': {'value': 'notAnInteger'}}).is_valid()


def test_empty_list():
    serializer = ListSerializer(data={'emails': []})
    assert serializer.is_valid(), 'Empty list should be allowed'


def test_valid_list():
    serializer = ListSerializer(data={'emails': ['some.where@out.there']})
    assert serializer.is_valid(), 'Valid list should be allowed'


def test_invalid_list_embedded():
    serializer = ContainerListSerializer(data={'embedded': [{'value': 'text'}]})
    assert not serializer.is_valid(), 'List field should be invalid'
    assert 'embedded' in serializer.errors, 'Invalid field value should produce a field error'


class DictSerializer(serializers.Serializer):
    emails = DictField(serializers.EmailField(), required=False)


def test_non_dict():
    serializer = DictSerializer(data={'emails': 'notADict'})
    assert not serializer.is_valid(), 'Non-dict value should not be allowed'
    assert 'emails' in serializer.errors, 'Non-dict value should produce a field error'
    assert serializer.errors['emails'], 'Non-dict value error should be non-empty'


def test_invalid_dict_value():
    serializer = DictSerializer(data={'emails': {'a': 'some.where@out.there',
                                      'b': 'notAnEmail'}})
    assert not serializer.is_valid(), 'Invalid dict-value should not be allowed'
    assert 'emails' in serializer.errors, 'Invalid dict-value should produce a field error'
    assert serializer.errors['emails'], 'Invalid dict-value errors should be non-empty {0}'.format(
        serializer.errors['emails'])
    assert ['b'] == list(six.iterkeys(serializer.errors['emails'][0]))


def test_empty_dict():
    serializer = DictSerializer(data={'emails': {}})
    assert serializer.is_valid(), 'Empty dict should be allowed'


def test_valid_dict():
    serializer = DictSerializer(data={'emails': {'a': 'some.where@out.there'}})
    assert serializer.is_valid(), 'Valid dict shouild be allowed'
