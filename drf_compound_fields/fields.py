#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compound fields for processing values that are lists and dicts of values described by embedded
fields.

"""


from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from rest_framework.compat import six
from rest_framework.fields import WritableField
from rest_framework.serializers import NestedValidationError


class ListField(WritableField):
    """
    A field whose values are lists of items described by the given item field. The item field can
    be another field type (e.g., CharField) or a serializer.
    """

    default_error_messages = {
        'invalid_type': _('%(value)s is not a list'),
    }
    empty = []

    def __init__(self, item_field=None, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)
        self.item_field = item_field

    def to_native(self, obj):
        if self.item_field and obj:
            return [
                self.item_field.to_native(item)
                for item in obj
            ]
        return obj

    def from_native(self, data):
        self.validate_is_list(data)
        if self.item_field and data:
            return [
                self.item_field.from_native(item_data)
                for item_data in data
            ]
        return data

    def validate(self, value):
        super(ListField, self).validate(value)

        self.validate_is_list(value)

        if self.item_field:
            errors = {}
            for index, item in enumerate(value):
                try:
                    self.item_field.run_validators(item)
                    self.item_field.validate(item)
                except ValidationError as e:
                    errors[index] = e

            if errors:
                raise NestedValidationError(errors)

    def validate_is_list(self, value):
        if not isinstance(value, list):
            raise ValidationError(self.error_messages['invalid_type'], code='invalid_type',
                    params={'value': value})


class DictField(WritableField):
    """
    A field whose values are dicts of values described by the given value field. The value field
    can be another field type (e.g., CharField) or a serializer.
    """

    default_error_messages = {
        'invalid_type': _('%(value)s is not a dict'),
    }
    default_unicode_options = {}
    empty = {}

    def __init__(self, value_field=None, unicode_options=None, *args, **kwargs):
        super(DictField, self).__init__(*args, **kwargs)
        self.value_field = value_field
        self.unicode_options = unicode_options or self.default_unicode_options

    def to_native(self, obj):
        if self.value_field and obj:
            return dict(
                (six.text_type(key, **self.unicode_options), self.value_field.to_native(value))
                for key, value in obj.items()
            )
        return obj

    def from_native(self, data):
        self.validate_is_dict(data)
        if self.value_field and data:
            return dict(
                (six.text_type(key, **self.unicode_options), self.value_field.from_native(value))
                for key, value in data.items()
            )
        return data

    def validate(self, value):
        super(DictField, self).validate(value)

        self.validate_is_dict(value)

        if self.value_field:
            errors = {}
            for k, v in six.iteritems(value):
                try:
                    self.value_field.run_validators(v)
                    self.value_field.validate(v)
                except ValidationError as e:
                    errors[k] = e

            if errors:
                raise NestedValidationError(errors)

    def validate_is_dict(self, value):
        if not isinstance(value, dict):
            raise ValidationError(self.error_messages['invalid_type'],  code='invalid_type',
                    params={'value': value})
