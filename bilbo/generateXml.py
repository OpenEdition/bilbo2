""" XML generator """
#-*- coding: utf-8 -*-
from lxml import etree
import copy
from  bilbo.converter import Converter
import subprocess


class GenerateXml(object):
    """
    XML generator class
    """

    def text_element(self, t, path):
        start = 0
        st=''
        for j, token in enumerate(t):
            if ((token.xpath == path) and (j==0 or token.predict_label==t[j-1].predict_label)):
                #st += ''.join((' ', token.str_value, ' '))
                st += token.word
                tag = token.predict_label
                start += 1
                if start < len(t):
                    continue
                else:
                    return self.pop_element(st, tag, t, start)
            elif ((token.xpath == path) and (t[j].predict_label!=t[j-1].predict_label)): 
                tag = t[j-1].predict_label
                return self.pop_element(st, tag, t, start)
            elif (token.xpath != path):
                tag = t[j-1].predict_label
                return self.pop_element(st, tag, t, start, False)
            else:
                print('BIZARRE')

    def pop_element(self, st, tag, l, start, in_path=True):
        child = self.create_child_element(st, tag)
        for _ in range(start):
           del l[0]
        return (in_path, child, l)

    def create_child_element(self, st, tag):
        tag = 'NoLabel' if tag is None else tag
        TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0"
        TEI = "{%s}" % TEI_NAMESPACE
        NSMAP = {None : TEI_NAMESPACE}
        child=etree.Element(TEI + tag, nsmap=NSMAP)
        child.text = st
        child.attrib['bilbo']='True'
        return child

    def add_child_element(self, elements, child):
        elements.text = None
        elements.insert(0, child)
        return child


    def add_child_tail_element(self, elements, child):
        elements.tail = None
        elements.addnext(child)
        return child

    def iter_in_path(self, e,l, is_tail = False):
        path_tail = '/following-sibling::text()' if is_tail else ''
        get_exact_path = lambda path_tail : ''.join((e.getroottree().getelementpath(e), path_tail)) 
        path = get_exact_path(path_tail)
        i=0
        in_path = True
        while in_path:
            in_path,child,l = self.text_element(l, path)
            if i==0:
                self.add_child_tail_element(e, child) if is_tail else self.add_child_element(e, child)
            if i>0:
                    last_child.addnext(child)
            i = i +1
            last_child=child

    def process_element(self, e, l):
        if e.text:
            try:
                self.iter_in_path(e, l)
            except TypeError:
                pass
        try:
            for element in e.xpath('.//*[not(@bilbo)]'):
                self.process_element(element, l)
        except TypeError:
            pass
        if (e.tail and e.xpath('local-name()')!=self.document.tag):
            self.iter_in_path(e, l, True)

    def generate_xml(self, doc, output, format_):
        self.document = doc
        for s in doc.sections:
            e = s.section_xml
            l = copy.deepcopy(s.tokens)
            self.process_element(e,l)
        conv = Converter(doc, format_)#XSLT transform not activated for now
        doc= conv.apply_transform()
        self.write_output(doc, output)
        #lines = subprocess.Popen(['xsltproc', TO_TEI1, '/tmp/tmp.xml'])
        #with open(output_file, 'w') as f:
        #    f.write(lines)    
        

    
    def write_output(self, doc, output_file):
        with open(output_file, 'w') as f:
            f.write(etree.tostring(doc.xml_tree, encoding='unicode', pretty_print=True))
