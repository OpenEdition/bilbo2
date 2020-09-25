import unittest
from bilbo.components.shape_data.shape_data import ShapeSection
from bilbo.importer import Importer
from bilbo.libs.opts import Parser
from lxml import etree
from os.path import dirname, abspath
import os



BILBO_HOME = dirname(abspath(__file__))
config_file = os.path.join(BILBO_HOME, "pipeline.cfg")
text = 'OpenEdition Lab, Développement;' 
bibl0 = '<TEI xmlns="http://www.tei-c.org/ns/1.0"><bibl>Start from , <hi>OpenEdition Lab, Développement; </hi> Between inside <p>2011,</p> « End to Bilbo »,. </bibl>Tail of bibl</TEI>'

class TestShapeSection(unittest.TestCase):
    
    def setUp(self):
        imp = Importer(bibl0)
        doc = imp.parse_xml('bibl', False)
        self.shaper = ShapeSection(config_file)
        doc = self.shaper.fit(doc)
        self.section = doc.sections[0]

    def test_expandTag(self):
        expected = [['OpenEdition', 'hi'],[' ', 'hi'], ['Lab', 'hi'],[',', 'c'], [' ', 'hi'], ['Développement', 'hi'], [';', 'c']]
        actual = self.shaper._expandTag(text, 'hi', 'fine')
        self.assertEqual(expected, actual)

    def test_getLabel(self):
        expected = 'hi'
        elements = self.section.section_xml
        for e in elements.getchildren():
            actual = self.shaper._getLabel(e)
            self.assertEqual(actual, expected)
            break
    
    def test_append_text(self):
        expected = [['Start', 'bibl'], ['from', 'bibl'], [',', 'c']]
        element = self.section.section_xml
        actual = self.shaper._append_text(element, 'bibl', self.section).token_str_lst
        self.assertEqual(actual, expected)
    
    def test_append_tail(self):
        expected = [['Between', 'bibl'], ['inside', 'bibl']]
        
        elements = self.section.section_xml
        for e in elements.getchildren():
            actual = self.shaper._append_tail(e, 'bibl', self.section).token_str_lst
            self.assertEqual(actual, expected)
            break

    def test_inside_iter_token(self):
        elements = self.section.section_xml
        self.shaper.extract_from_section(self.section, elements, 'bibl')
        expected=[('from', 'bibl', '{http://www.tei-c.org/ns/1.0}bibl'),
                    ('Lab', 'hi', '{http://www.tei-c.org/ns/1.0}bibl/{http://www.tei-c.org/ns/1.0}hi'),
                    ('Bilbo', 'bibl', '{http://www.tei-c.org/ns/1.0}bibl/{http://www.tei-c.org/ns/1.0}p/following-sibling::text()')]  
        actual = list()
        for token in self.section.tokens:
            actual.append((token.str_value, token.label, token.xpath))

        for triplet in expected:
            self.assertIn(triplet, actual)
    
    def test_outside_iter_token(self):
        elements = self.section.section_xml
        self.shaper.extract_from_section(self.section, elements, 'bibl')
        expected= 'Tail'  
        actual = list()
        for token in self.section.tokens:
            actual.append(token.str_value)
        self.assertNotIn(expected, actual)

if __name__ == '__main__':
    unittest.main()
