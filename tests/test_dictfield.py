#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
test_dictfield
--------------

Tests for `drf_compound_fields.fields.DictField`.

"""


# Django settings:
import os
os.environ['DJANGO_SETTINGS_MODULE'] = __name__

from django.conf.global_settings import CACHES  # NOQA
SECRET_KEY = 's3cr3t'


from datetime import date

from django.core.exceptions import ValidationError
from rest_framework import ISO_8601
from rest_framework.fields import CharField
from rest_framework.fields import DateField
import pytest

from drf_compound_fields.fields import DictField


def test_from_native_no_value_field():
    """
    When a DictField has no value-field, from_native should return the data it was given
    un-processed.
    """
    field = DictField()
    data = {"a": 1, "b": 2}
    obj = field.from_native(data)
    assert data == obj


def test_to_native_no_value_field():
    """
    When a DictField has no value-field, to_native should return the data it was given
    un-processed.
    """
    field = DictField()
    obj = {"a": 1, "b": 2}
    data = field.to_native(obj)
    assert obj == data


def test_from_native_with_value_field():
    """
    When a DictField has an value-field, from_native should return a dict of elements resulting
    from the application of the value-field's from_native method to each value of the input
    data dict.
    """
    field = DictField(DateField())
    data = {"a": "2000-01-01", "b": "2000-01-02"}
    obj = field.from_native(data)
    assert {"a": date(2000, 1, 1), "b": date(2000, 1, 2)} == obj


def test_to_native_with_value_field():
    """
    When a DictField has an value-field, to_native should return a dict of elements resulting from
    the application of the value-field's to_native method to each value of the input object dict.
    """
    field = DictField(DateField(format=ISO_8601))
    obj = {"a": date(2000, 1, 1), "b": date(2000, 1, 2)}
    data = field.to_native(obj)
    assert {"a": "2000-01-01", "b": "2000-01-02"} == data


def test_missing_required_dict():
    """
    When a DictField requires a value, then validate should raise a ValidationError on a missing
    (None) value.
    """
    field = DictField()
    with pytest.raises(ValidationError):
        field.validate(None)


def test_validate_non_dict():
    """
    When a DictField is given a non-dict value, then validate should raise a ValidationError.
    """
    field = DictField()
    with pytest.raises(ValidationError):
        field.validate('notADict')


def test_validate_empty_dict():
    """
    When a DictField requires a value, then validate should raise a ValidationError on an empty
    value.
    """
    field = DictField()
    with pytest.raises(ValidationError):
        field.validate({})


def test_validate_elements_valid():
    """
    When a DictField is given a dict whose values are valid for the value-field, then validate
    should not raise a ValidationError.
    """
    field = DictField(CharField(max_length=5))
    try:
        field.validate({"a": "a", "b": "b", "c": "c"})
    except ValidationError:
        assert False, "ValidationError was raised"


def test_validate_elements_invalid():
    """
    When a DictField is given a dict containing values that are invalid for the value-field, then
    validate should raise a ValidationError.
    """
    field = DictField(CharField(max_length=5))
    with pytest.raises(ValidationError):
        field.validate({"a": "012345", "b": "012345"})
