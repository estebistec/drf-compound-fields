.. :changelog:

History
-------

0.2.2 (2014-08-10)
++++++++++++++++++

Correct validation behaviors when fields are used in embedded serializers. Also correction to the
`list` and `dict` type checks for `None` values (#15, #16, #18).

* Implement `initialize` and `field_from_native` to ensure proper validation in embedded
  serializers.
* Give the fields distinct `validate` and `run_validators` implementations that don't call each
  other.
* Don't apply the `list` and `dict` type checks for `None` values.

0.2.1 (2014-04-23)
++++++++++++++++++

Loosen dependency versions

* Remove explicit dependency on Django
* Loosen rest-framework to any version before 3

0.2.0 (2014-03-16)
++++++++++++++++++

* Documentation (#3)
* Collect messages of nested errors, instead of error objects (#12)
* Add ListOrItemField type (#5, #11)
* Fix PartialDictField validation and handling of badly-typed values
* Switch project tests to py.test (#10)

0.1.0 (2014-03-06)
++++++++++++++++++

First PyPI release of rest-framework serializer compound-fields (#1). Provides:

* ListField (#4, #7)
* DictField
* PartialDictField (#8, #9)
