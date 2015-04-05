#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
test_partialdictfield
---------------------

Tests for `drf_compound_fields.fields.PartialDictField`.

"""


from . import test_settings

from datetime import date

from rest_framework.serializers import ValidationError
from rest_framework import ISO_8601
from rest_framework.serializers import CharField
from rest_framework.serializers import DateField

from drf_compound_fields.fields import PartialDictField


def test_to_internal_value_with_included_keys():
    """
    When a PartialDictField has an included_keys, to_internal_value should return a dict of elmenents
    resulting from the application of the value-field's to_internal_value method to values of the input
    data dict that are includeded by included_keys.
    """
    field = PartialDictField(included_keys=['a'], child=DateField())
    data = {"a": "2000-01-01", "b": "2000-01-02"}
    obj = field.to_internal_value(data)
    assert {"a": date(2000, 1, 1)} == obj


def test_to_representation_with_included_keys():
    """
    When a PartialDictField has an included_keys, to_representation should return a dict of elmenents
    resulting from the application of the value-field's to_representation method to values of the input
    object dict that are included by included_keys.
    """
    field = PartialDictField(included_keys=['a'], child=DateField(format=ISO_8601))
    obj = {"a": date(2000, 1, 1), "b": date(2000, 1, 2)}
    data = field.to_representation(obj)
    assert {"a": "2000-01-01"} == data


def test_to_internal_value_with_nonexisting_included_keys():
    """
    When a PartialDictField has an included_keys that includes nonexisting keys, to_internal_value should
    ignore them.
    """
    field = PartialDictField(included_keys=['a', 'c'], child=DateField())
    data = {"a": "2000-01-01", "b": "2000-01-02"}
    obj = field.to_internal_value(data)
    assert {"a": date(2000, 1, 1)} == obj


def test_to_representation_with_nonexisting_included_keys():
    """
    When a PartialDictField has an included_keys that includes nonexisting keys, to_representation should
    ignore them.
    """
    field = PartialDictField(included_keys=['a', 'c'], child=DateField(format=ISO_8601))
    obj = {"a": date(2000, 1, 1), "b": date(2000, 1, 2)}
    data = field.to_representation(obj)
    assert {"a": "2000-01-01"} == data


def test_validate_non_included_keys():
    """
    When a dict has invalid values for keys that are not specified in included_keys, it should not
    report errors for those keys.
    """
    field = PartialDictField(included_keys=['a'], child=CharField(max_length=5),
                             required=False)
    data = {'b': '123456'}
    try:
        field.to_internal_value(data)
    except ValidationError:
        assert False, 'Got a ValidationError for a non-included key'
