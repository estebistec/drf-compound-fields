#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
test_listoritemfield
--------------------

Tests for `drf_compound_fields.fields.ListOrItemField`.

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

from drf_compound_fields.fields import ListOrItemField


def test_to_native_list():
    """
    When given a valid list, the ListOrItemField to_native method should utilize the list to-native
    logic.
    """
    field = ListOrItemField(DateField(format=ISO_8601))
    data = field.to_native([date.today()])
    assert [date.today().isoformat()] == data


def test_from_native_list():
    """
    When given a valid list, the ListOrItemField from_native method should utilize the list
    from-native logic.
    """
    field = ListOrItemField(DateField(format=ISO_8601))
    data = field.from_native([date.today().isoformat()])
    assert [date.today()] == data


def test_to_native_item():
    """
    When given a valid item, the ListOrItemField to_native method should utilize the item to-native
    logic.
    """
    field = ListOrItemField(DateField(format=ISO_8601))
    data = field.to_native(date.today())
    assert date.today().isoformat() == data


def test_from_native_item():
    """
    When given a valid item, the ListOrItemField from_native method should utilize the item
    from-native logic.
    """
    field = ListOrItemField(DateField(format=ISO_8601))
    data = field.from_native(date.today().isoformat())
    assert date.today() == data


def test_validate_required_missing():
    """
    When given a None value the ListOrItemField validate method should raise a ValidationError.
    """
    field = ListOrItemField()
    with pytest.raises(ValidationError):
        field.validate(None)


def test_invalid_item():
    """
    When given an invalid value the ListOrItemField validate method should raise a ValidationError.
    """
    field = ListOrItemField(CharField(max_length=5))
    with pytest.raises(ValidationError):
        field.validate('123456')


def test_list_value_invalid_items():
    """
    When given a list with an invalid value the ListOrItemField validate method should raise a
    ValidationError.
    """
    field = ListOrItemField(CharField(max_length=5))
    with pytest.raises(ValidationError) as e:
        field.validate(['12345', '123456'])
        assert [1] == e.messages[0].keys()
