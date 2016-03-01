#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
test_listoritemfield
--------------------

Tests for `drf_compound_fields.fields.ListOrItemField`.

"""


from . import test_settings

from datetime import date

from rest_framework.serializers import ValidationError
from rest_framework import ISO_8601
from rest_framework.serializers import CharField
from rest_framework.serializers import DateField
from rest_framework.serializers import Serializer
import pytest

from drf_compound_fields.fields import ListOrItemField


def test_to_representation_list():
    """
    When given a valid list, the ListOrItemField to_representation method should utilize the list to-native
    logic.
    """
    field = ListOrItemField(child=DateField(format=ISO_8601))
    data = field.to_representation([date.today()])
    assert [date.today().isoformat()] == data


def test_to_internal_value_list():
    """
    When given a valid list, the ListOrItemField to_internal_value method should utilize the list
    from-native logic.
    """
    field = ListOrItemField(child=DateField(format=ISO_8601))
    data = field.to_internal_value([date.today().isoformat()])
    assert [date.today()] == data


def test_to_representation_item():
    """
    When given a valid item, the ListOrItemField to_representation method should utilize the item to-native
    logic.
    """
    field = ListOrItemField(child=DateField(format=ISO_8601))
    data = field.to_representation(date.today())
    assert date.today().isoformat() == data


def test_to_internal_value_item():
    """
    When given a valid item, the ListOrItemField to_internal_value method should utilize the item
    from-native logic.
    """
    field = ListOrItemField(child=DateField(format=ISO_8601))
    data = field.to_internal_value(date.today().isoformat())
    assert date.today() == data


def test_validate_required_missing():
    """
    When given a None value the ListOrItemField validate method should raise a ValidationError.
    """
    field = ListOrItemField(child=DateField(format=ISO_8601))
    with pytest.raises(ValidationError):
        field.to_internal_value(None)


def test_invalid_item():
    """
    When given an invalid value the ListOrItemField validate method should raise a ValidationError.
    """
    field = ListOrItemField(child=CharField(max_length=5))
    with pytest.raises(ValidationError):
        field.to_internal_value('123456')


def test_list_value_invalid_items():
    """
    When given a list with an invalid value the ListOrItemField validate method should raise a
    ValidationError.
    """
    field = ListOrItemField(child=CharField(max_length=5))
    with pytest.raises(ValidationError):
        field.to_internal_value(['12345', '123456'])
