"""shaper module"""
#!-*- coding: utf-8 -*-

from configparser import ConfigParser
from lxml import etree

from bilbo.tokenizers.tokenizers import Tokenizer
from bilbo.storage.token import Token
from bilbo.components.component import Extractor

import logging
logger = logging.getLogger(__name__)

class ShapeSection(Extractor):
    """
    shape the section to the right form
    """
    _parser_name = 'shaper' 
    _module_name = 'shaper' 

    def __init__(self, cfg_file, type_config='ini', lang='fr'):
        super(ShapeSection, self).__init__(cfg_file, type_config)
        self.tokenizer = Tokenizer(lang)

    def _get_opts(self):
        self.tokenizer_option = self.parser.getArgs(self.cfg_file, "tokenizerOption")
        self.tags_options = self.parser.getArgs(self.cfg_file, "tagsOptions")
        self.verbose = self.parser.getArgs(self.cfg_file, "verbose")

    def _getLabel(self, element):
        """
        Gets label from the xml tag
        :param element: xml element
        :returns: label
        """
        label  = element.xpath('local-name()')
        label = ''.join((label, '_', element.get("level"))) if element.get("level") is not None else label 
        return label

    def _expandTag(self, text, tag, tokenizer_option):
        """
        Expands the tag of the string to each token

        :param text: text to tokenize
        :param tag: tag of the associated text
        :param tokenizer_option: option of the tokenizer

        :returns: list of token annotated [token, label]
        """
        # tag_option = dictionnary read from the cfg_file importer.crg.ini
        # it allow to specify the tag : tag[read] = tag_wanted
        tag_option = eval(self.tags_options)
        punc = set("!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~“”«»")
        tokens_tagged = []
        for token in self.tokenizer.tokenize(text):
            if token in punc:
                tokens_tagged.append([token, "c"])
            else:
                if tag in tag_option:
                    logger.debug('Tag %s is map to %s' % (tag, tag_option[tag]))
                    tokens_tagged.append([token, tag_option[tag]])
                else:
                    tokens_tagged.append([token, tag])
        return tokens_tagged

    def _transform(self, doc):
        """
        Parse an XML section and shape it to the section object
        :param section: XML section
        """
        tag = doc.tag
        logger.info('Start to extract for each section corresponding token')
        for section in doc.sections:
            elements = section.section_xml
            cur_section = section
            self.extract_from_section(cur_section, elements, tag)
            logger.debug('One section is finished')
        return doc

    def extract_from_section(self, section, elements, tag, last_label=None):
        label = last_label if last_label else self._getLabel(elements)
        if elements.text:
            self._append_text(elements, label, section)
        for element in elements.getchildren():
            self.extract_from_section(section, element, tag, None)
        if (elements.tail and tag!=label and elements.tail.strip()):
            label_tag = tag
            self._append_tail(elements, label_tag, section)

    def _append_to_section(self, text, section, path):
        len_txt = len(text) - 1
        for index, value in enumerate(text):
            if value[0] == ' ':
                continue
            if index == len_txt:
                sep = False
            else:
                sep = True if text[index+1][0] == ' ' else False
            token = Token(value[0], value[1], separator=sep)
            token.xpath = path
            section.tokens.append(token)
            section.token_str_lst.append([value[0], value[1]])
        return section

    def _append_text(self, element, label, section):
        text = self._expandTag(element.text, label,\
                self.tokenizer_option)
        path = element.getroottree().getelementpath(element)
        return self._append_to_section(text, section, path)
    
    def _append_tail(self, element, label, section):
        text = self._expandTag(element.tail.strip(), label,\
                self.tokenizer_option)
        path = element.getroottree().getelementpath(element) + '/following-sibling::text()'
        return self._append_to_section(text, section, path)
