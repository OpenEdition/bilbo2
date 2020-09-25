"""
section
"""
#! -*- coding: utf-8 -*-
class Section(object):
    """
    describe the section stored
    
    :str_value: string value with tags
    :section_naked: string value without tag
    :section_xml: lxml object
    :tokens: list of token object (cf token)
    :token_str_lst: list of string token
    :bibl_status: True if the section contain a bibl tag Fasle otherwise
    """
    def __init__(self, str_value, section_naked, section_xml, \
            tokens=None, token_str_lst=None, bibl_status=True, keys=None):
        self.str_value = str_value
        self.section_naked = section_naked
        self.section_xml = section_xml
        self.bibl_status = bibl_status
        self.keys = keys

        if tokens is None:
            self.tokens = []
        else:
            self.tokens = tokens

        if  token_str_lst is None:
            self.token_str_lst = []
        else:
            self.token_str_lst = token_str_lst

    def print_tokens(self):
        """
        print section
        """
        for token in self.tokens:
            print(token.str_value)
        print("")
