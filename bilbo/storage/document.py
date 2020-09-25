"""
Document
"""
#! -*- coding: utf-8 -*-
class Document(object):
    """
    Class that describe a document.
    
    :str_value: string value with tags
    :xml_tree: lxml object
    :section: cf section
    """
    def __init__(self, str_value, xml_tree, tag, sections=None):
        self.str_value = str_value
        self.xml_tree = xml_tree
        self.tag = tag
        if sections is None:
            self.sections = []
        else:
            self.sections = sections

    def genereDocumentPivot(self):
        """
        print the document stored
        """
        for section in self.sections:
            section.print_tokens()

