.. image:: https://badge.fury.io/py/drf-compound-fields.png
    :target: http://badge.fury.io/py/drf-compound-fields

.. image:: https://travis-ci.org/estebistec/drf-compound-fields.png?branch=master
        :target: https://travis-ci.org/estebistec/drf-compound-fields

.. image:: https://pypip.in/d/drf-compound-fields/badge.png
        :target: https://crate.io/packages/drf-compound-fields?version=latest

.. image:: https://coveralls.io/repos/estebistec/drf-compound-fields/badge.png?branch=master
   :target: https://coveralls.io/r/estebistec/drf-compound-fields?branch=master
   :alt: Test coverage

Overview
========

`Django-REST-framework <http://www.django-rest-framework.org/>`_
`serializer fields <http://www.django-rest-framework.org/api-guide/fields>`_ for compound types.
Django-REST-framework provides the ability to
`deal with multiple objects <http://www.django-rest-framework.org/api-guide/serializers#dealing-with-multiple-objects>`_
using the `many=True` option on serializers. That allows for lists of objects and for fields to be
lists of objects.

This package expands on that and provides fields allowing:

* Lists of simple (non-object) types, described by other serializer fields.
* Fields that allow values to be a list or individual item of some type.
* Dictionaries of simple and object types.
* Partial dictionaries which include keys specified in a list.

A quick example::

    from drf_compound_fields.fields import DictField
    from drf_compound_fields.fields import ListField
    from drf_compound_fields.fields import ListOrItemField
    from drf_compound_fields.fields import ListField
    from rest_framework import serializers

    class EmailContact(serializers.Serializer):
        email = serializers.EmailField()
        verified = serializers.BooleanField()

    class UserProfile(serializers.Serializer):
        username = serializers.CharField()
        email_contacts = EmailContact(many=True)  # List of objects: possible with REST-framework alone
        # This is the new stuff:
        skills = ListField(serializers.CharField())  # E.g., ["javascript", "python", "ruby"]
        name = ListOrItemField(serializers.CharField())  # E.g., "Prince" or ["John", "Smith"]
        bookmarks = DictField(serializers.URLField())  # E.g., {"./": "http://slashdot.org"}
        measurements = PartialDictField(included_keys=['height', 'weight'], serializers.IntegerField())

See the :doc:`usage <usage>` for more information.

Project info
============

* Free software: BSD license
* `Documentation <https://drf-compound-fields.readthedocs.io>`_
* `Source code <https://github.com/estebistec/drf-compound-fields>`_
* `Issue tracker <https://github.com/estebistec/drf-compound-fields/issues>`_
* `CI server <https://travis-ci.org/estebistec/drf-compound-fields>`_
* IRC: no channel but see AUTHORS for individual nicks on freenode.
* Mailing list: None yet, but please log an `issue <https://github.com/estebistec/drf-compound-fields/issues>`_ if you want to have discussions about this package.
