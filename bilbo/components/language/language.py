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
    _module_name = 'language' 

    def __init__(self, cfg_file, type_config='ini'):
        super(Language, self).__init__(cfg_file, type_config)
        self.default = self.parser.getArgs(self.cfg_file, "default", type_opt='dict')

    def transform(self, document, mode):
        super(Language, self).transform(document, mode)

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
        logger.info('Start to predict')         
        result = list()
        for section in document.sections:
            result.append(detect(section.section_naked))
        return result

    def train(self, document):
        """
        :param document: document object or file
        """
        logger.warn('For train language detection is not implemented')         
        pass

    def _add_to_doc(self, document, result):
        for i, section in enumerate(document.sections):
            section.lang = self.map_lang(self.default, result[i])
            logger.debug('Lang is :{}'.format(section.lang))         

    def map_lang(self, rule, detected):
        if rule is None:
            return lang
        for lang in rule.get('lang', list()):
            if detected == lang:
                return lang
        return rule.get('default')
