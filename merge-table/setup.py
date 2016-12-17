#!/usr/bin/env python
# coding=utf-8

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'CHANGELOG.rst')).read()

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
zip_safe = not on_rtd

version = '0.1.0'

setup(
    name='merge-table',
    version=version,
    description="merge-table is a mysql Tool that auto split table.",
    long_description=README + '\n\n' + NEWS,
    license='MIT License',
    author='kylinfish',
    author_email='kylinfish@126.com',
    keywords='merge-table',
    url='https://github.com/wujuguang/pycorner.git',
    packages=find_packages(),
    include_package_data=True,
    platforms=["any"],
    # zip_safe=zip_safe,
    zip_safe=False,
    classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License'
    ]
)
