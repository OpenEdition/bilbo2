#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name = 'bilbo2',
    version = '1.1.0',
    packages = find_packages(),
    author = "OpenEdition Lab",
    author_email = "mathieu.orban@openedition.org",
    description = "Automatic reference labeling",
    long_description = open('README.md').read(),
    install_requires= ["lxml>=4.3", "python-crfsuite==0.9.6", "libsvm==3.23.0.4"," langdetect>=1.0.8"],
    extras_require = {'develop': ['unittest-xml-reporting']},
    #Include MANIFEST.in file
    include_package_data = True,
    url = 'https://github.com/OpenEdition/bilbo',

    classifiers=[
        "License :: Public Domain",
        "Programming Language :: Python",
        "Operating System :: Linux / UNIX",
        "Programming Language :: Python :: 3.5",
        "Topic :: Automatic labeling",
        "Topic :: Bibliography",
    ],
    # La syntaxe est "nom-de-commande-a-creer = package.module:fonction".
    entry_points = {
        'console_scripts': [
            'bilbo = bilbo.bilbo:Bilbo',
        ],
    },

    license = "AGPLV3",
)
