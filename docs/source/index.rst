.. bilbo2 documentation master file, created by
   sphinx-quickstart on Wed Jul 10 09:39:15 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to bilbo2's documentation!
===================================

`BILBO2 <https://github.com/OpenEdition/bilbo2>`_ is an open source software for automatic annotation of bibliographic reference. It provides the segmentation and tagging of input string.
Its main purpose is to provide both a complete development and research space for the improvement of bibliographic reference detections and to be a solid tool capable of being used in production like `OpenEdition <https://www.openedition.org/>`_ for example.
What you will find here is the user documentation, the technical documentation and the developper documentation for the Bilbo software.

This documentation is organized into a few main sections :


* :ref:`purpose`
* :ref:`user-docs`
* :ref:`essential`
* :ref:`usage`
* :ref:`configuration`
* :ref:`developer`

.. toctree::
  :maxdepth: 1
  :name: purpose
  :caption: Purpose
  
  purpose.md

.. toctree::
  :maxdepth: 2
  :name: user-docs
  :caption: Getting started
  
  start/web-demo.md
  start/requirements.md
  start/installation.md
  start/usage.md

.. toctree::
  :maxdepth: 2
  :name: essential
  :caption: Essential Things To Know
  
  essential/I-O.md
  essential/pipelines.md
  essential/chaining.md

.. toctree::
  :maxdepth: 2
  :name: usage
  :caption: Usage
  
  usage/toolkit.md
  usage/shell.md
  usage/annotator.md

.. toctree::
  :maxdepth: 2
  :name: configuration
  :caption: Configuration
  
  configuration/options.md
  configuration/knowledge-base.md


.. toctree::
  :maxdepth: 2
  :name: guidelines
  :caption: Guidelines for improved annotation
  
  guidelines/evaluation.md
  guidelines/scores.md

.. toctree::
  :maxdepth: 2
  :name: developer
  :caption: Developer
  
  developer/modules.rst



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
