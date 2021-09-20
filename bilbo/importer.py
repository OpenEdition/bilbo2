""" importer """
#!-*- coding: utf-8 -*-

from lxml import etree

from bilbo.storage.document import Document
from bilbo.storage.section import Section
import logging

logger = logging.getLogger(__name__)

class Importer:
    """
    Importer class
    """
    def __init__(self, xml_file):
        self.xml_file = xml_file

    def parse_xml(self, tag_separator, is_file=True):
        """
        Parse en XML file to split it into section objects

        :returns: document object
        """
        doc, cur_document = self.load(tag_separator, is_file)
        for elements in doc.iter():
            path = doc.getpath(elements)
            name_label = doc.xpath('name('+path+')')
            if name_label == tag_separator:
                section_naked = ''.join(doc.xpath(path+'//text()'))
                if section_naked:
                    str_value = etree.tostring(elements, encoding='utf8', method='xml').decode('utf-8')
#            if tag_separator in elements.tag[-4:]:
                    cur_section = Section(str_value, section_naked, elements)
                    cur_document.sections.append(cur_section)
        logger.debug('Parsing is done')
        return cur_document

    def load(self, tag_separator, is_file=True):
        parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)

        if is_file:
            doc = etree.parse(self.xml_file, parser)
            logger.debug('Load XML File')
        else:
            doc_element = etree.XML(self.xml_file, parser)
            doc = doc_element.getroottree()
            logger.debug('Load XML string')
        root = doc.getroot()
        str_ = etree.tostring(root, encoding='utf8', method='xml').decode('utf-8')
        doc_object = Document(str_, doc, tag_separator)
        return doc, doc_object

