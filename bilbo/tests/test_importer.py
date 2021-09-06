import unittest
from lxml import etree
from bilbo.importer import Importer
from bilbo.storage.document import Document


TESTDATA_FILENAME = 'bilbo/testFiles/testdata.xml'

TAG_XML = """<TEI xmlns="http://www.tei-c.org/ns/1.0">
<head/>
<body>
<p>
<bibl>H.<hi>L'adieu aux armes</hi>.1929. Arrow Books, 2004. </bibl>
<note place="foot" n="1">Gros, Christian, « La nation en question : identité ou métissage », <hi rendition="#style03">Hérodote</hi>, 2000, 99, p. 107-108.</note>
<bibl><hi>Orban M., Faath E., 2017, « Wikipedia, bibliographies », </hi> OpenEdition Press, Marseille.</bibl>
<note place="foot" n="2"><p>L’évolution des systèmes urbains.</p></note>
</p>
</body>
</TEI>"""


bibl1 = '<bibl xmlns="http://www.tei-c.org/ns/1.0">H.<hi>L\'adieu aux armes</hi>.1929. Arrow Books, 2004. </bibl>'


class TestImporter(unittest.TestCase):
    
    def _load(self):
        parser = etree.XMLParser(remove_blank_text=True)
        self.XML = TAG_XML.replace('\n', '')
        root = etree.XML(self.XML, parser)
        with open(TESTDATA_FILENAME, "wb") as f:
            f.write(etree.tostring(root, encoding='utf8', method='xml'))
    
    def setUp(self):
        self._load()
        self.testdata = Importer(TESTDATA_FILENAME)
        self.doc = self.testdata.parse_xml('bibl')

    def test_parse_xml(self):
        self.check_doc_str_att()
        self.check_section_xml()

    def check_doc_str_att(self):
        self.assertEqual(self.doc.str_value, self.XML)

    def check_section_xml(self):
        h1 = etree.XML(bibl1)
        str1 = etree.tostring(h1)
        str2 = etree.tostring(self.doc.sections[0].section_xml)
        self.assertEqual(str2,str1)



if __name__ == '__main__':
    unittest.main()

