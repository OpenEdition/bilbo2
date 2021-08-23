""" XML converter """
#-*- coding: utf-8 -*-
from lxml import etree
import os
import subprocess

TO_TEI = ['bilbo/stylesheets/rule1.xsl', 'bilbo/stylesheets/rule2.xsl', 'bilbo/stylesheets/rule3.xsl', 'bilbo/stylesheets/cleaner.xsl']

TO_JATS = ['bilbo/stylesheets/rule.xsl', 'bilbo/stylesheets/cleaner.xsl', 'bilbo/stylesheets/tei-to-jats.xsl']

class Converter(object):
    """
    XML converter class
    """

    def __init__(self, doc, xsl='TEI'):
        self.document = doc
        self.xsl = TO_TEI if xsl=='TEI' else TO_JATS if xsl=='JATS' else None

    def get_transformer(self, xsl):
        root = etree.parse(xsl)
        transform = etree.XSLT(root)
        return transform

    def apply_transform(self):
        if self.xsl:
            for xsl in self.xsl:
                transform = self.get_transformer(xsl)
                self.document.xml_tree = transform(self.document.xml_tree)
            return self.document
        else:
            return self.document

