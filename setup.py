#!/usr/bin/env python

from distutils.core import setup

setup(
    name='groupmebot',
    version='1.0',
    author='Matt Molo',
    author_email='matt@mattmolo.com',
    url='https://github.com/groupme-bot/',
    packages=['groupmebot'],
    install_requires=["Flask", "requestify"],
    description='A library to handle forward-slash commnads on GroupMe.',
)
