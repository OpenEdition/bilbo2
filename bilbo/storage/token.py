"""
Token
"""
#! -*- coding: utf-8 -*-
class Token(object):
    """
    Describe the token object

    :str_value: string value
    :label: label associated
    :feature: list of feature
    """
    def __init__(self, str_value, label, features=None, predict_label=None, separator=True):
        self.str_value = str_value
        self.label = label
        self.predict_label = predict_label
        self.xpath = None
        if features is None:
            self.features = {}
        else:
            self.features = features
        self.separator = ' ' if separator is True else ''
    
    @property
    def tail(self):
        return 'following-sibling' in self.xpath

    def printToken(self):
        """
        Print token
        """
        print(self.str_value, self.label)

    @property
    def word(self):
        return self.str_value + self.separator

    

