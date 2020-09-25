""" XML features """
import re
from bilbo.components.features.decorator_feature import SectionDecorator

class XmlFeature:
    """
    Generate feature based on XML datas
    """
    @SectionDecorator
    def italic(self, section):
        """
        append the italic feature in the section/token object

        :param section: section object (cf storage)
        """
        sec = section.str_value.replace('<hi rend="bold"></hi>', "")
        toks = section.tokens
        hinb = 2
        track = 0

        for sect in re.split('<[^>]*?hi', sec):

            if hinb % 2 == 0:
                for j in range(len(toks[track:])):
                    if toks[track+j].str_value == "None":
                        toks[track+j].features["italic"] = "NOITALIC"
                    elif toks[track+j].str_value in sect:
                        toks[track+j].features["italic"] = "NOITALIC"
                    else:
                        track = track+j
                        hinb += 1
                        break
            else:
                for j in range(len(toks[track:])):
                    if toks[track+j].str_value == "None":
                        toks[track+j].features["italic"] = "ITALIC"
                    elif toks[track+j].str_value in sect:
                        toks[track+j].features["italic"] = "ITALIC"
                    else:
                        track = track+j
                        hinb += 1
                        break

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
