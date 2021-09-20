""" XML features """
import re
from bilbo.components.features.decorator_feature import SectionDecorator, XmlDecorator

class XmlFeature:
    """
    Generate feature based on XML datas
    """
    @XmlDecorator
    def italic(self, element, xpath):
        """
        append the italic feature in the section/token object

        :param section: section object (cf storage)
        """
        path = XmlFeature.format_xpath(element, xpath)
        parent_path =  ''.join((path,'/','../[@rend="italic"]'))
        self_path = ''.join((path,'[@rend="italic"]'))
        if ((element.find(parent_path)) is not None or (element.find(self_path) is not None)):
            return "ITALIC"
        else:
            return "NOITALIC"

    @staticmethod
    def format_xpath(element, xpath):
        element_path = ''.join((element.getroottree().getelementpath(element),'/'))
        relative_path = xpath.replace(element_path, '').replace('/following-sibling::text()', '')
        return relative_path
        
    @SectionDecorator
    def global_boolean(self, section, key, value):
        for token in section.tokens:
            feat_dict = token.features
            if feat_dict[key]==value:
                return True

    @SectionDecorator
    def punc_counter(self, section, limit=2):
        punc = set(r'!\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~“”«»')
        counter = 0
        for token in section.tokens:
            if token.str_value in punc:
                counter+=1
            if (counter > limit):
                return 0
        return counter
