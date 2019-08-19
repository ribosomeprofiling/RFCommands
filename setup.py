#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import re

from setuptools import setup, find_packages


classifiers = [\
    "Development Status :: 3 - Alpha",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7"
]


def _read(*parts, **kwargs):
    filepath = os.path.join(os.path.dirname(__file__), *parts)
    encoding = kwargs.pop('encoding', 'utf-8')
    with io.open(filepath, encoding=encoding) as fh:
        text = fh.read()
    return text

def get_version():
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        _read('rfcommands', '_version.py'),
        re.MULTILINE).group(1)
    return version

def get_long_description():
    return _read('README.md')


install_requires = [
    'numpy>=1.16.1',
    'pandas>=0.24.1',
    'click>=7.0',
    'matplotlib>=3.0.2',
    'multiprocess>=0.70.7',
    'pysam>=0.15.0',
    'pyyaml>=5.1'
]

'''
## TODO complete documentation\
extras_require = {
    'docs': [
        'Sphinx>=1.1',
        'numpydoc>=0.5'
    ]
}
'''

description_text = 'Set of command line tools used by RiboFlow pipeline.'

setup(
    name                          = 'rfcommands',
    author                        = 'Hakan Ozadam',
    version                       = get_version(),
    packages                      = find_packages(),
    license                       = 'MIT',
    description                   = description_text,
    long_description              = get_long_description(),
    long_description_content_type = 'text/markdown',
    include_package_data          = True,
    install_requires              = install_requires,
    zip_safe                      = False,
    classifiers                   = [x.strip() for x in classifiers ],
    entry_points                  = {
        'console_scripts': ['rfc=rfcommands.cli.main:cli',]
    }
)
