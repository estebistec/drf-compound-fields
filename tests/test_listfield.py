#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
test_listfield
--------------

Tests for `drf_compound_fields.fields.ListField`.

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

from drf_compound_fields.fields import ListField


def test_from_native_no_item_field():
    """
    When a ListField has no item-field, from_native should return the data it was given
    un-processed.
    """
    field = ListField()
    data = list(range(5))
    obj = field.from_native(data)
    assert data == obj


def test_to_native_no_item_field():
    """
    When a ListField has no item-field, to_native should return the data it was given
    un-processed.
    """
    field = ListField()
    obj = list(range(5))
    data = field.to_native(obj)
    assert data == obj


def test_from_native_with_item_field():
    """
    When a ListField has an item-field, from_native should return a list of elements resulting
    from the application of the item-field's from_native method to each element of the input
    data list.
    """
    field = ListField(DateField())
    data = ["2000-01-01", "2000-01-02"]
    obj = field.from_native(data)
    assert [date(2000, 1, 1), date(2000, 1, 2)] == obj


def test_to_native_with_item_field():
    """
    When a ListField has an item-field, to_native should return a list of elements resulting
    from the application of the item-field's to_native method to each element of the input
    object list.
    """
    field = ListField(DateField(format=ISO_8601))
    obj = [date(2000, 1, 1), date(2000, 1, 2)]
    data = field.to_native(obj)
    assert ["2000-01-01", "2000-01-02"] == data


def test_missing_required_list():
    """
    When a ListField requires a value, then validate should raise a ValidationError on a missing
    (None) value.
    """
    field = ListField()
    with pytest.raises(ValidationError):
        field.validate(None)


def test_validate_non_list():
    """
    When a ListField is given a non-list value, then validate should raise a ValidationError.
    """
    field = ListField()
    with pytest.raises(ValidationError):
        field.validate('notAList')


def test_errors_non_list():
    """
    When a ListField is given a non-list value, then there should be one error related to the
    type mismatch.
    """
    field = ListField()
    try:
        field.validate('notAList')
        assert False, 'Expected ValidationError'
    except ValidationError as e:
        assert 'notAList is not a list', e.messages[0]


def test_validate_empty_list():
    """
    When a ListField requires a value, then validate should raise a ValidationError on an empty
    value.
    """
    field = ListField()
    with pytest.raises(ValidationError):
        field.validate([])


def test_validate_elements_valid():
    """
    When a ListField is given a list whose elements are valid for the item-field, then validate
    should not raise a ValidationError.
    """
    field = ListField(CharField(max_length=5))
    try:
        field.validate(["a", "b", "c"])
    except ValidationError:
        assert False, "ValidationError was raised"


def test_validate_elements_invalid():
    """
    When a ListField is given a list containing elements that are invalid for the item-field,
    then validate should raise a ValidationError.
    """
    field = ListField(CharField(max_length=5))
    with pytest.raises(ValidationError):
        field.validate(["012345", "012345"])
