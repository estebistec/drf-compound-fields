#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
    from setuptools.command.test import test as TestCommand

    class PyTest(TestCommand):

        def finalize_options(self):
            TestCommand.finalize_options(self)
            self.test_args = []
            self.test_suite = True

        def run_tests(self):
            #import here, cause outside the eggs aren't loaded
            import pytest
            errno = pytest.main(self.test_args)
            sys.exit(errno)

except ImportError:
    from distutils.core import setup, Command

    class PyTest(Command):

        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            import subprocess
            import sys

            errno = subprocess.call([sys.executable, 'runtests.py'])
            raise SystemExit(errno)

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='drf-compound-fields',
    version='0.2.0',
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
    zip_safe=False,
    install_requires=[
        'Django==1.6.2',
        'djangorestframework==2.3.13'
    ],
    test_suite='tests',
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    license="BSD",
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
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
