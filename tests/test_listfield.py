#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
test_listfield
--------------

Tests for `drf_compound_fields.fields.ListField`.

"""


from . import test_settings

from datetime import date

from rest_framework.serializers import ValidationError
from rest_framework import ISO_8601
from rest_framework.serializers import CharField
from rest_framework.serializers import DateField
import pytest

from drf_compound_fields.fields import ListField


def test_to_internal_value_with_item_field():
    """
    When a ListField has an item-field, to_internal_value should return a list of elements resulting from
    the application of the item-field's to_internal_value method to each element of the input data list.
    """
    field = ListField(child=DateField())
    data = ["2000-01-01", "2000-01-02"]
    obj = field.to_internal_value(data)
    assert [date(2000, 1, 1), date(2000, 1, 2)] == obj


def test_to_representation_with_item_field():
    """
    When a ListField has an item-field, to_representation should return a list of elements resulting from
    the application of the item-field's to_representation method to each element of the input object list.
    """
    field = ListField(child=DateField(format=ISO_8601))
    obj = [date(2000, 1, 1), date(2000, 1, 2)]
    data = field.to_representation(obj)
    assert ["2000-01-01", "2000-01-02"] == data


def test_missing_required_list():
    """
    When a ListField requires a value, then validate should raise a ValidationError on a missing
    (None) value.
    """
    field = ListField(child=DateField())
    with pytest.raises(ValidationError):
        field.to_internal_value(None)


def test_validate_non_list():
    """
    When a ListField is given a non-list value, then validate should raise a ValidationError.
    """
    field = ListField(child=DateField())
    with pytest.raises(ValidationError):
        field.to_internal_value('notAList')


def test_errors_non_list():
    """
    When a ListField is given a non-list value, then there should be one error related to the type
    mismatch.
    """
    field = ListField(child=DateField())
    try:
        field.to_internal_value('notAList')
        assert False, 'Expected ValidationError'
    except ValidationError as e:
        pass

def test_validate_elements_valid():
    """
    When a ListField is given a list whose elements are valid for the item-field, then validate
    should not raise a ValidationError.
    """
    field = ListField(child=CharField(max_length=5))
    try:
        field.to_internal_value(["a", "b", "c"])
    except ValidationError:
        assert False, "ValidationError was raised"


def test_validate_elements_invalid():
    """
    When a ListField is given a list containing elements that are invalid for the item-field, then
    validate should raise a ValidationError.
    """
    field = ListField(child=CharField(max_length=5))
    with pytest.raises(ValidationError):
        field.to_internal_value(["012345", "012345"])
