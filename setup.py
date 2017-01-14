#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError as ex:
    from distutils.core import setup

packages = [
    'odml',
    'odml.tools'
]


setup(name='odML',
      version='1.3dev',
      description='open metadata Markup Language',
      author='Hagen Fritsch',
      author_email='fritsch+gnode@in.tum.de',
      url='http://www.g-node.org/projects/odml',
      packages=packages,
      test_suite='test',
      install_requires=["enum", "lxml"],
      )
