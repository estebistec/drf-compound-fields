#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='drf-compound-fields',
    version='0.1.0',
    description='Django-REST-framework serializer fields for compound types.',
    long_description=readme + '\n\n' + history,
    author='Steven Cummings',
    author_email='cummingscs@gmail.com',
    url='https://github.com/estebistec/drf-compound-fields',
    packages=[
        'drf_compound_fields',
    ],
    package_dir={'drf_compound_fields': 'drf_compound_fields'},
    include_package_data=True,
    install_requires=[
        'Django==1.6.2',
        'djangorestframework==2.3.13'
    ],
    license="BSD",
    zip_safe=False,
    keywords='rest_framework rest apis services fields compound',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
