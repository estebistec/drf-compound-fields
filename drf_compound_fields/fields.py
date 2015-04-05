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
    be another field type (e.g., CharField) or a serializer. However, for serializers, you should
    instead just use it with the `many=True` option.
    """

    default_error_messages = {
        'invalid_type': _('%(value)s is not a list'),
    }
    empty = []

    def __init__(self, item_field=None, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)
        self.item_field = item_field

    def initialize(self, parent, field_name):
        super(ListField, self).initialize(parent, field_name)
        if self.item_field:
            self.item_field.initialize(parent, field_name)

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
            values = [
                self.item_field.from_native(item_data)
                for item_data in data
            ]
            if self.item_field.errors:
                raise NestedValidationError(self.item_field.errors)
            return values
        return data

    def validate(self, value):
        super(ListField, self).validate(value)

        self.validate_is_list(value)

        if self.item_field:
            errors = {}
            for index, item in enumerate(value):
                try:
                    self.item_field.validate(item)
                except ValidationError as e:
                    errors[index] = e.messages

            if errors:
                raise NestedValidationError(errors)

    def run_validators(self, value):
        super(ListField, self).run_validators(value)

        if self.item_field:
            errors = {}
            for index, item in enumerate(value):
                try:
                    self.item_field.run_validators(item)
                except ValidationError as e:
                    errors[index] = e.messages

            if errors:
                raise NestedValidationError(errors)

    def validate_is_list(self, value):
        if value is not None and not isinstance(value, list):
            raise ValidationError(
                self.error_messages['invalid_type'],
                code='invalid_type',
                params={'value': value}
            )


class ListOrItemField(WritableField):
    """
    A field whose values are either a value or lists of values described by the given item field.
    The item field can be another field type (e.g., CharField) or a serializer.
    """

    def __init__(self, item_field=None, *args, **kwargs):
        super(ListOrItemField, self).__init__(*args, **kwargs)
        self.item_field = item_field
        self.list_field = ListField(item_field)

    def initialize(self, parent, field_name):
        super(ListOrItemField, self).initialize(parent, field_name)
        if self.item_field:
            self.item_field.initialize(parent, field_name)
        self.list_field.initialize(parent, field_name)

    def to_native(self, obj):
        if isinstance(obj, list):
            return self.list_field.to_native(obj)
        elif self.item_field:
            return self.item_field.to_native(obj)
        return obj

    def from_native(self, data):
        if isinstance(data, list):
            return self.list_field.from_native(data)
        elif self.item_field:
            return self.item_field.from_native(data)
        return data

    def field_from_native(self, data, files, field_name, into):
        if isinstance(data, list):
            return self.list_field.field_from_native(data, files, field_name, into)
        elif self.item_field:
            return self.item_field.field_from_native(data, files, field_name, into)
        else:
            super(ListOrItemField, self).field_from_native(data, files, field_name, into)

    def validate(self, value):
        super(ListOrItemField, self).validate(value)
        if isinstance(value, list):
            self.list_field.validate(value)
        elif self.item_field:
            self.item_field.validate(value)

    def run_validators(self, value):
        super(ListOrItemField, self).run_validators(value)
        if isinstance(value, list):
            self.list_field.run_validators(value)
        elif self.item_field:
            self.item_field.run_validators(value)


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

    def initialize(self, parent, field_name):
        super(DictField, self).initialize(parent, field_name)
        if self.value_field:
            self.value_field.initialize(parent, field_name)

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
                    self.value_field.validate(v)
                except ValidationError as e:
                    errors[k] = e.messages

            if errors:
                raise NestedValidationError(errors)

    def run_validators(self, value):
        super(DictField, self).run_validators(value)

        if self.value_field:
            errors = {}
            for k, v in six.iteritems(value):
                try:
                    self.value_field.run_validators(v)
                except ValidationError as e:
                    errors[k] = e.messages

            if errors:
                raise NestedValidationError(errors)

    def validate_is_dict(self, value):
        if value is not None and not isinstance(value, dict):
            raise ValidationError(
                self.error_messages['invalid_type'],
                code='invalid_type',
                params={'value': value}
            )


class PartialDictField(DictField):
    """
    A dict field whose values are filtered to only include values for the specified keys.
    """

    def __init__(self, included_keys, value_field=None, unicode_options=None,
                 *args, **kwargs):
        self.included_keys = included_keys
        super(PartialDictField, self).__init__(value_field, unicode_options,
                                               *args, **kwargs)

    def to_native(self, obj):
        return super(PartialDictField, self).to_native(self._filter_dict(obj))

    def from_native(self, data):
        return super(PartialDictField, self).from_native(self._filter_dict(data))

    def validate(self, value):
        super(PartialDictField, self).validate(self._filter_dict(value))

    def run_validators(self, value):
        super(PartialDictField, self).run_validators(self._filter_dict(value))

    def _filter_dict(self, value):
        if isinstance(value, dict):
            return dict(
                (k, v)
                for k, v in six.iteritems(value)
                if k in self.included_keys
            )
        return value
