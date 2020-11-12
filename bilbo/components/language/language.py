"""shaper module"""
#!-*- coding: utf-8 -*-

from configparser import ConfigParser
from langdetect import detect 
from bilbo.components.component import Estimator

import logging
logger = logging.getLogger(__name__)

class Language(Estimator):
    """
    shape the section to the right form
    """
    _parser_name = 'language' 

    def __init__(self, cfg_file, type_config='ini'):
        super(Language, self).__init__(cfg_file, type_config)

    def transform(self, document):
        super(Language, self).transform(document, mode='tag')

    def fit(self, document):
        if isinstance(document, list):
            raise Exception('You must import Document first')
        else:
            return document

    def predict(self, document):
        """
        tag document's tokens given a model

        :param document: document object or file

        :returns: list of token and label tagged
        """
        result = list()
        for section in document.sections:
            result.append(detect(section.section_naked))
        return result

    def _add_to_doc(self, document, result):
        for i, section in enumerate(document.sections):
            section.lang = result[i]
