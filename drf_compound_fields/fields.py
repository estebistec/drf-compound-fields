#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compound fields for processing values that are lists and dicts of values described by embedded
fields.

"""


from rest_framework.compat import six
from rest_framework.serializers import DictField
from rest_framework.serializers import Field
from rest_framework.serializers import ListField





class ListOrItemField(Field):
    """
    A field whose values are either a value or lists of values described by the given item field.
    The item field can be another field type (e.g., CharField) or a serializer.
    """

    def __init__(self, child, *args, **kwargs):
        super(ListOrItemField, self).__init__(*args, **kwargs)
        self.item_field = child
        self.list_field = ListField(child=child, *args, **kwargs)

    def to_representation(self, obj):
        if isinstance(obj, list):
            return self.list_field.to_representation(obj)
        return self.item_field.to_representation(obj)

    def to_internal_value(self, data):
        if isinstance(data, list):
            return self.list_field.to_internal_value(data)
        # Force field validation. Not necessary on the list_field since DRF calls it recursively.
        self.item_field.run_validation(data)
        return self.item_field.to_internal_value(data)

class PartialDictField(DictField):
    """
    A dict field whose values are filtered to only include values for the specified keys.
    """

    def __init__(self, included_keys, child, *args, **kwargs):
        self.included_keys = included_keys
        super(PartialDictField, self).__init__(child=child, *args, **kwargs)

    def to_representation(self, obj):
        return super(PartialDictField, self).to_representation(self._filter_dict(obj))

    def to_internal_value(self, data):
        return super(PartialDictField, self).to_internal_value(self._filter_dict(data))

    def _filter_dict(self, value):
        if isinstance(value, dict):
            return dict(
                (k, v)
                for k, v in six.iteritems(value)
                if k in self.included_keys
            )
        return value
