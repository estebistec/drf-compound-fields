#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
test_dictfield
--------------

Tests for `drf_compound_fields.fields.DictField`.

"""


from . import test_settings

from datetime import date

from rest_framework.serializers import ValidationError
from rest_framework import ISO_8601
from rest_framework.serializers import CharField
from rest_framework.serializers import DateField
import pytest

from drf_compound_fields.fields import DictField


def test_to_internal_value_with_child():
    """
    When a DictField has an value-field, to_internal_value should return a dict of elements resulting
    from the application of the value-field's to_internal_value method to each value of the input
    data dict.
    """
    field = DictField(child=DateField())
    data = {"a": "2000-01-01", "b": "2000-01-02"}
    obj = field.to_internal_value(data)
    assert {"a": date(2000, 1, 1), "b": date(2000, 1, 2)} == obj


def test_to_representation_with_child():
    """
    When a DictField has an value-field, to_representation should return a dict of elements resulting from
    the application of the value-field's to_representation method to each value of the input object dict.
    """
    field = DictField(child=DateField(format=ISO_8601))
    obj = {"a": date(2000, 1, 1), "b": date(2000, 1, 2)}
    data = field.to_representation(obj)
    assert {"a": "2000-01-01", "b": "2000-01-02"} == data


def test_validate_non_dict():
    """
    When a DictField is given a non-dict value, then validate should raise a ValidationError.
    """
    field = DictField(child=DateField())
    with pytest.raises(ValidationError):
        field.to_internal_value('notADict')


def test_validate_elements_valid():
    """
    When a DictField is given a dict whose values are valid for the value-field, then validate
    should not raise a ValidationError.
    """
    field = DictField(child=CharField(max_length=5))
    try:
        field.to_internal_value({"a": "a", "b": "b", "c": "c"})
    except ValidationError:
        assert False, "ValidationError was raised"


def test_validate_elements_invalid():
    """
    When a DictField is given a dict containing values that are invalid for the value-field, then
    validate should raise a ValidationError.
    """
    field = DictField(child=CharField(max_length=5))
    with pytest.raises(ValidationError):
        field.to_internal_value({"a": "012345", "b": "012345"})
