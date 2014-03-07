===================
drf-compound-fields
===================

.. image:: https://badge.fury.io/py/drf-compound-fields.png
    :target: http://badge.fury.io/py/drf-compound-fields

.. image:: https://travis-ci.org/estebistec/drf-compound-fields.png?branch=master
        :target: https://travis-ci.org/estebistec/drf-compound-fields

.. image:: https://pypip.in/d/drf-compound-fields/badge.png
        :target: https://crate.io/packages/drf-compound-fields?version=latest

.. image:: https://coveralls.io/repos/estebistec/drf-compound-fields/badge.png?branch=master
   :target: https://coveralls.io/r/estebistec/drf-compound-fields?branch=master
   :alt: Test coverage


Django-REST-framework serializer fields for compound types.

* Free software: BSD license
* `Documentation <http://drf-compound-fields.rtfd.org>`_
* `Source code <https://github.com/estebistec/drf-compound-fields>`_
* `Issue tracker <https://github.com/estebistec/drf-compound-fields/issues>`_
* `CI server <https://travis-ci.org/estebistec/drf-compound-fields>`_
* IRC: no channel but see AUTHORS for individual nicks on freenode.
* Mailing list: None yet, but please log an `issue <https://github.com/estebistec/drf-compound-fields/issues>`_ if you want to have discussions about this package.

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
    see the `Python Unicode HOWTO <http://docs.python.org/2/howto/unicode.html>`_.

    **Signature:** `DictField(value_field=None, unicode_options=None)`

    If given, unicode_options must be a dict providing options per the [unicode](http://docs.python.org/2/library/functions.html#unicode)
    function.

`PartialDictField`
    A similar field to `DictField`, but only includes values whose keys are listed in `included_keys`

    **Signature:** `PartialDictField(included_keys, value_field=None, unicode_options=None)`
