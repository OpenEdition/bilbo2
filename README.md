# Bilbo2 : Automatic reference labeling

Bilbo2 is an open source software for automatic annotation of bibliographic reference. It provides the segmentation and tagging of input XML document.
Rewritten in python3 from Scratch, it comes from BILBO. Compare to the old one, a particular attention has been paid to the possibility of easily adding new algorithms of machine learning and test parameters. It can be used as much in live systems as for research.





## Installation

### Dependencies

Bilbo2 requires:

* **python3.5**
* **gcc** and **g++** (used by LIBSVM compilation)
* **git** >= 1.7.10 (needed by github)
* **pip** and **setuptools** , necessary for launch python installation
* **libxml2-dev**

User installation


```console
python3 setup.py install --user
```

The documentation includes more detailed [Installation Instructions](https://bilbo2-openedition.readthedocs.io/en/latest/start/installation.html)


## Usage


For an overview and a test of cli usage, from a terminal, run:

```
cd bilbo2
/bin/bash bilbo/tests/bilbo_demo.sh -v
```

You can add -v argument to see output. 

See [docs](https://bilbo2-openedition.readthedocs.io/en/latest/usage/toolkit.html) for complete cli usage.

See [examples](https://github.com/OpenEdition/bilbo2/blob/master/examples/examples.ipynb) for python interface usage

## Author and contributors
(C)Copyright 2019 OpenEdition by [Mathieu Orban](mailto:mathieu.orban@openedition.org)
Main contributors are **Yann Weber**, **Jérémy Trione**. Special acknowledgements for Yoann Dupont(https://github.com/YoannDupont)


## License

Bilbo2 is free and opensource. This project is licensed under the GNU AFFERO GENERAL PUBLIC LICENCE - see the LICENSE.txt file for details

## External resources used by Bilbo2

Currently it is based on Conditional Random Fields (CRFs), machine learning technique to segment and label sequence data and on Support-Vector machines, machine learning technique to classify data.

As external softwares, it is used `python-crfsuite`_ for CRF learning and inference and and `libSVM`_ is used for sequence classification.
1. [Python-crfsuite](https://github.com/scrapinghub/python-crfsuite) Machine learning tools to segment and label sequence data with linear-chain CRF.
2. [LibSVM](https://www.csie.ntu.edu.tw/~cjlin/libsvm/) A Library for Support Vector Machines by Chih-Chung Chang and Chih-Jen Lin
3. [Lxml](https://lxml.de/) Library for processing XML and HTML in the Python Language.
4. [setuptools](https://pypi.python.org/pypi/setuptools): to install Bilbo2.


## Contributing

* Source code: https://github.com/OpenEdition/bilbo2
* Issue tracker: https://github.com/OpenEdition/bilbo2/Issues

Feel free to submit ideas, bugs reports, pull requests or regular patches.



## Tests

In order to run tests, launch:

```
cd bilbo2
python3 -m bilbo.tests.tests
```



