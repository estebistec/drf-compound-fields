===================
drf_compound_fields
===================

.. image:: https://badge.fury.io/py/drf_compound_fields.png
    :target: http://badge.fury.io/py/drf_compound_fields
    
.. image:: https://travis-ci.org/estebistec/drf_compound_fields.png?branch=master
        :target: https://travis-ci.org/estebistec/drf_compound_fields

.. image:: https://pypip.in/d/drf_compound_fields/badge.png
        :target: https://crate.io/packages/drf_compound_fields?version=latest


Django-REST-framework serializer fields for compound types.

* Free software: BSD license
* Documentation: http://drf_compound_fields.rtfd.org.

Features
--------

Compound Fields
~~~~~~~~~~~~~~~

These fields represent compound datatypes, which build on other fields with some additional aspect such collecting multiple elements.

`ListField`
    A list representation, whose elements are described by a given item field. This means that all elements must meet the definition of
    that field. The item field can be another field type (e.g., CharField) or a serializer. If `item_field` is not given, then the
    list-items are passed through as-is, and can be anything. Note that in this case, any non-native list elements wouldn't be properly
    prepared for data rendering.

    **Signature:** `ListField(item_field=None)`

`DictField`
    A dictionary representation, whose values are described by a given value field. This means that all values must meet the definition of
    that field. The value field can be another field type (e.g., CharField) or a serializer. If `value_field` is not given, then the `dict`
    values are passed through-as-is, and can be anything. Note that in this case, any non-native `dict` values wouldn't be properly
    prepared for data rendering.

    Dictionary keys are presumed to be character strings or convertible to such, and so during processing are casted to `unicode`. If
    necessary, options for unicode conversion (such as the encoding, or error processing) can be provided to a `DictField`. For more info,
    see [py_unicode].

    **Signature:** `DictField(value_field=None, unicode_options=None)`

    If given, unicode_options must be a dict providing options per the [unicode](http://docs.python.org/2/library/functions.html#unicode)
    function.

[py_unicode]: http://docs.python.org/2/howto/unicode.html