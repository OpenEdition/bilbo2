#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os.path
import subprocess
import tarfile


cwd = os.path.abspath(".")
libs_dir = "./bilbo/libs/"
extensions = ".tar.gz"


tar_file = [f for f in os.listdir(libs_dir) if f.endswith(extensions)][0]

libsvm_tar = os.path.join(libs_dir, tar_file)
libsvm_dir = os.path.join(libs_dir, tar_file[:-7])


def compile_binary(path, name):
    os.chdir(path)
    cmd = ["make"]
    exit_status = subprocess.call(cmd, shell=True)
    print('{} compilation done\n'.format(name) if (exit_status==0) else '{} compilation Failed\n'.format(name))
    return exit_status

    


if not os.path.isdir(libsvm_dir):
    with tarfile.open(libsvm_tar, "r:gz") as tar:
        tar.extractall(os.path.dirname(libs_dir))
if not (os.path.exists(os.path.join(libsvm_dir, "svm.o"))):
    if (compile_binary(libsvm_dir, 'LIBSVM C++') == 0):
        compile_binary("./python/", 'LIBSM PYTHON')

os.chdir(cwd)




setup(
    name = 'bilbo2',
    version = '1.0',
    packages = find_packages(),
    author = "OpenEdition Lab",
    author_email = "mathieu.orban@openedition.org",
    description = "Automatic reference labeling",
    long_description = open('README.md').read(),
    install_requires= ["lxml>=4.3", "python-crfsuite==0.9.6"],
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
    # C'est un système de plugin, mais on s'en sert presque exclusivement
    # Pour créer des commandes, comme "django-admin".
    # Par exemple, si on veut créer la fabuleuse commande "proclame-sm", on
    # va faire pointer ce nom vers la fonction proclamer(). La commande sera
    # créé automatiquement. 
    # La syntaxe est "nom-de-commande-a-creer = package.module:fonction".
    entry_points = {
        'console_scripts': [
            'bilbo = bilbo.bilbo:Bilbo',
        ],
    },

    license = "AGPLV3",
)
