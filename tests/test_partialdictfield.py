#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
test_partialdictfield
---------------------

Tests for `drf_compound_fields.fields.PartialDictField`.

"""


from . import test_settings

from datetime import date

from django.core.exceptions import ValidationError
from rest_framework import ISO_8601
from rest_framework.fields import CharField
from rest_framework.fields import DateField

from drf_compound_fields.fields import PartialDictField


def test_from_native_with_included_keys():
    """
    When a PartialDictField has an included_keys, from_native should return a dict of elmenents
    resulting from the application of the value-field's from_native method to values of the input
    data dict that are includeded by included_keys.
    """
    field = PartialDictField(included_keys=['a'], value_field=DateField())
    data = {"a": "2000-01-01", "b": "2000-01-02"}
    obj = field.from_native(data)
    assert {"a": date(2000, 1, 1)} == obj


def test_to_native_with_included_keys():
    """
    When a PartialDictField has an included_keys, to_native should return a dict of elmenents
    resulting from the application of the value-field's to_native method to values of the input
    object dict that are included by included_keys.
    """
    field = PartialDictField(included_keys=['a'], value_field=DateField(format=ISO_8601))
    obj = {"a": date(2000, 1, 1), "b": date(2000, 1, 2)}
    data = field.to_native(obj)
    assert {"a": "2000-01-01"} == data


def test_from_native_with_nonexisting_included_keys():
    """
    When a PartialDictField has an included_keys that includes nonexisting keys, from_native should
    ignore them.
    """
    field = PartialDictField(included_keys=['a', 'c'], value_field=DateField())
    data = {"a": "2000-01-01", "b": "2000-01-02"}
    obj = field.from_native(data)
    assert {"a": date(2000, 1, 1)} == obj


def test_to_native_with_nonexisting_included_keys():
    """
    When a PartialDictField has an included_keys that includes nonexisting keys, to_native should
    ignore them.
    """
    field = PartialDictField(included_keys=['a', 'c'], value_field=DateField(format=ISO_8601))
    obj = {"a": date(2000, 1, 1), "b": date(2000, 1, 2)}
    data = field.to_native(obj)
    assert {"a": "2000-01-01"} == data


def test_validate_non_included_keys():
    """
    When a dict has invalid values for keys that are not specified in included_keys, it should not
    report errors for those keys.
    """
    field = PartialDictField(included_keys=['a'], value_field=CharField(max_length=5),
                             required=False)
    data = {'b': '123456'}
    try:
        field.run_validators(data)
    except ValidationError:
        assert False, 'Got a ValidationError for a non-included key'
