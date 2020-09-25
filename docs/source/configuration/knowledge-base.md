# Knowledge Base #

Knowledge Base are located in resources/ path at the root at bilbo_v2 . There are splitted in three ways:
* Training Corpus [corpus](#corpus)
* External List [external](#external)
* Model and specific pattern [model](#model)


## Corpus
They are used to train bilbo automatic annotation. This is annotated data used in supervised machine learning algorithms.
XML / TEI corpus are available in 4 langages (pt, fr, de, en) for bibliographies references. 
Only a mixed corpus of french and english is avalaible for footnote.

## Externals list ##


List can be simple or with multiwords, you must specifiy type of list in [options](../configuration/options.html#listfeaturesexternes): 
* Authors (fullname, surname, forename).
* Abbreviation (month, page, editor).
* Journals
* Place

## Models ##
Models are splited in two ways (in bibl and note directory). There are contains feature templates pattern (CRF++ format), see [documentation](https://taku910.github.io/crfpp/#templ).
Note that we are used crf++ templates with crf-suite for convenience. A script is handling conversion between the both input format.

In note we are used crf and svm model. To svm model see installation and data format [documentation](https://github.com/cjlin1/libsvm/blob/master/README) in libsvm README. 
