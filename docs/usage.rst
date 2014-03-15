========
Usage
========

The following sections explain how and when you would use each of the provided fields. Note that
while the examples have been simplified to dictionary data, object conversions (via
`restore_object` methods) are valid as well.

`ListField`
-----------

**Signature**::

    ListField(item_field=None)

Use this field to create lists of simple types. If the item field is not given, then values are
passed through as-is.

Declare a serializer with a list field::

    from drf_compound_fields.fields import ListField
    from rest_framework import serializers

    class SkillsProfileSerializer(serializers.Serializer):
        name = serializers.CharField()
        skills = ListField(serializers.CharField(min_length=3))

Serialize an object with a list::

    serializer = SkillsProfileSerializer({'name': 'John Smith', 'skills': ['Python', 'Ruby']})
    print serializer.data

Output::

    {'name': u'John Smith', 'skills': [u'Python', u'Ruby']}

Deserialize an object with a list::

    serializer = SkillsProfileSerializer(data={'name': 'John Smith', 'skills': ['Python', 'Ruby']})
    assert serializer.is_valid(), serializer.errors
    print serializer.object

Output::

    {'skills': ['Python', 'Ruby'], 'name': 'John Smith'}

Get validation errors from invalid data::

    serializer = SkillsProfileSerializer(data={'name': 'John Smith', 'skills': ['Python', 'io']})
    assert serializer.is_valid(), serializer.errors

Output::

    Traceback (most recent call last):
      File "demo.py", line 36, in <module>
        assert serializer.is_valid(), serializer.errors
    AssertionError: {'skills': [{1: [u'Ensure this value has at least 3 characters (it has 2).']}]}

*NOTE* You can technically pass serializers to `ListField`. However, since you can just tell a
serializer to
`deal with multiple objects <http://www.django-rest-framework.org/api-guide/serializers#dealing-with-multiple-objects>`_,
it is recommended that you stick with this method.

`ListOrItemField`
-----------------

**Signature**::

    ListOrItemField(item_field=None)

A field whose values are either a value or lists of values described by the given item field. If
the item field is not given, then values are passed through as-is.

Declare a serializer with a list-or-item field::

    from drf_compound_fields.fields import ListField
    from drf_compound_fields.fields import ListOrItemField
    from rest_framework import serializers

    class SkillsProfileSerializer(serializers.Serializer):
        name = serializers.CharField()
        skills = ListField(serializers.CharField(min_length=3))
        social_links = ListOrItemField(serializers.URLField())

Serialize with an item value::

    print SkillsProfileSerializer({
        'name': 'John Smith',
        'skills': ['Python'],
        'social_links': 'http://chrp.com/johnsmith'
    }).data

Output::

    {'name': u'John Smith', 'skills': [u'Python'], 'social_links': u'http://chrp.com/johnsmith'}

Serialize with a list value::

    data = SkillsProfileSerializer({
        'name': 'John Smith',
        'skills': ['Python'],
        'social_links': ['http://chrp.com/johnsmith', 'http://myface.com/johnsmith']
    }).data
    import pprint
    pprint.pprint(data)

Output::

    {'name': u'John Smith',
     'skills': [u'Python'],
     'social_links': [u'http://chrp.com/johnsmith', u'http://myface.com/johnsmith']}

Get validation errors for an item value::

    serializer = SkillsProfileSerializer(data={
        'name': 'John Smith',
        'skills': ['Python'], 'social_links': 'not_a_url'
    })
    assert serializer.is_valid(), serializer.errors

Output::

    Traceback (most recent call last):
      File "demo.py", line 23, in <module>
        assert serializer.is_valid(), serializer.errors
    AssertionError: {'social_links': [u'Invalid value.']}

Get validation errors for a list value::

    serializer = SkillsProfileSerializer(data={
        'name': 'John Smith',
        'skills': ['Python'],
        'social_links': ['http://chrp.com/johnsmith', 'not_a_url']
    })
    assert serializer.is_valid(), serializer.errors

Output::

    Traceback (most recent call last):
      File "demo.py", line 23, in <module>
        assert serializer.is_valid(), serializer.errors
    AssertionError: {'social_links': [{1: [u'Invalid value.']}]}

`DictField`
-----------

**Signature**::

    DictField(value_field=None, unicode_options=None)

A field whose values are dicts of values described by the given value field. The value field
can be another field type (e.g., CharField) or a serializer.

If `value_field` is not given, then the `dict` values are passed through-as-is, and can be
anything. Note that in this case, any non-native `dict` values wouldn't be properly prepared for
data rendering.

If given, unicode_options must be a dict providing options per the
`unicode <http://docs.python.org/2/library/functions.html#unicode>`_ function.

Dictionary keys are presumed to be character strings or convertible to such, and so during
processing are casted to `unicode`. If necessary, options for unicode conversion (such as the
encoding, or error processing) can be provided to a `DictField`. For more info, see the
`Python Unicode HOWTO <http://docs.python.org/2/howto/unicode.html>`_.

Declare a serializer with a dict field::

    from drf_compound_fields.fields import DictField
    from rest_framework import serializers

    class UserBookmarksSerializer(serializers.Serializer):
        username = serializer.CharField()
        links = DictField(serializers.URLField())

Serialize an object with a dict::

    serializer = UserBookmarksSerializer({
        'username': 'jsmith',
        'links': {
            'Order of the Stick': 'http://www.giantitp.com/comics/oots.html',
            'The Hypertext Application Language': 'http://stateless.co/hal_specification.html'
        }
    })
    import pprint
    pprint.pprint(serializer.data)

Output::

    {'links': {u'Order of the Stick': u'http://www.giantitp.com/comics/oots.html',
               u'The Hypertext Application Language': u'http://stateless.co/hal_specification.html'},
     'username': u'jsmith'}

Deserialize an object with a dict::

    serializer = UserBookmarksSerializer(data={
        'username': u'jsmith',
        'links': {
            'Order of the Stick': u'http://www.giantitp.com/comics/oots.html',
            'The Hypertext Application Language': u'http://stateless.co/hal_specification.html'
        }
    })
    assert serializer.is_valid(), serializer.errors
    import pprint
    pprint.pprint(serializer.object)

Output::

    {'links': {u'Order of the Stick': u'http://www.giantitp.com/comics/oots.html',
               u'The Hypertext Application Language': u'http://stateless.co/hal_specification.html'},
     'username': u'jsmith'}

Get validation errors from invalid data::

    serializer = UserBookmarksSerializer(data={
        'username': u'jsmith',
        'links': {
            'Order of the Stick': u'not_a_url',
            'The Hypertext Application Language': u'http://stateless.co/hal_specification.html'
        }
    })
    assert serializer.is_valid(), serializer.errors

Output::

    Traceback (most recent call last):
      File "demo.py", line 25, in <module>
        assert serializer.is_valid(), serializer.errors
    AssertionError: {'links': [{u'Order of the Stick': [u'Invalid value.']}]}

`PartialDictField`
------------------

**Signature**::

    PartialDictField(included_keys, value_field=None, unicode_options=None)

A dict field whose values are filtered to only include values for the specified keys.

Declare a serializer with a partial dict field::

    from drf_compound_fields.fields import PartialDictField
    from rest_framework import serializers

    class UserSerializer(serializers.Serializer):
        user_details = PartialDictField(['favorite_food'], serializers.CharField())

Serialize an object with a partial dict::

    serializer = UserSerializer({'user_details': {'favorite_food': 'pizza', 'height': '52in'}})
    import pprint
    pprint.pprint(serializer.data)

Output::

    {'user_details': {u'favorite_food': u'pizza'}}

Deserialize data with a partial dict::

    serializer = UserSerializer(data{'user_details': {'favorite_food': 'pizza', 'height': '52in'}})
    import pprint
    pprint.pprint(serializer.object)

Output::

    {'user_details': {u'favorite_food': u'pizza'}}
