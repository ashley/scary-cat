#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='scary-cat',
    install_requires=requirements,
    packages=find_packages(),
    entry_points = {
        'console_scripts': ['scary-cat=scary_cat.scary_cat:main']
    }
)
