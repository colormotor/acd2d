#!/usr/bin/env python3

from setuptools import setup, find_packages
import sys

setup(name='pyacd',
        version='0.1',
        description='ACD2d, Python bindings',
        url='',
        author='Daniel Berio',
        author_email='drand48@gmail.com',
        license='MIT',
        packages=find_packages(),
        install_requires = ['numpy'],
        zip_safe=False)
