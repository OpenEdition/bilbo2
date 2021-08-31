#!-*- coding: utf-8 -*-
"""tokenizer module"""
import os
import re

class DefaultTokenizer:
    _vocab_path = ''
    _regex_rules = None
    
    def __init__(self):
        """ Constructs a new tokenizer """

        self.resources = os.path.dirname(__file__) + self._vocab_path
        """ The path of the resources folder. """

        self.lexicon = {}
        """ The dictionary containing the lexicon. """

        self.regexp = re.compile(self._regex_rules)

        self.loadlist(self.resources+'abbrs.list')
        """ Loads the default lexicon (path is /resources/abbrs.list). """

        #self.loadlist(self.resources+'villes.list')
        #""" Loads the city lexicon (path is /resources/villes.list). """

    def tokenize(self, text):
        print("Abstract Class should be implemented in a given langage")

    def loadlist(self, path):
        """ Load a resource list and generate the corresponding regexp part. """

        # Reading the input file sequentially
        for line in open(path, 'r'):
            # Get the word
            word = line.strip().lower()
            # Add the word to the lexicon
            self.lexicon[word] = 1




class Tokenizer:
    """
    Tokenizer class
    tokenize a given string
    """
    def __new__(cls, lang):
        from bilbo.tokenizers.fr import FrenchTokenizer
        from bilbo.tokenizers.en import EnglishTokenizer
        tokenizers = {'fr':FrenchTokenizer, 'en': EnglishTokenizer}
        return tokenizers[lang]()
