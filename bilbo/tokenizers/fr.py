#-*- encoding:utf-8 -*-

from bilbo.tokenizers.tokenizers import DefaultTokenizer
import re

class FrenchTokenizer(DefaultTokenizer):
    
    _vocab_path = '/resources/'
    _regex_rules = r'''(?xumsi)
            (?:[lcdjmnts]|qu)['’]                         # Contractions
            | (?:http|https)://[\w\-]+(?:\.[\w\-]+)+\S*         # Adresses web
            | \d+[.,]\d+                                    # Les réels en/fr
            | \w{1}\.                                       # Contraction forename
            | [.]+                                         # Les ponctuations
            | \w+                                           # Les mots pleins
            | [^\w\s]                                       # -
            | \s
            '''
   #         | \w{1}\.\w{1}\.                                # Contraction forename
    
    def tokenize(self, text):
        """
        Tokenize the sentence given in parameter and return a list of tokens. 
        This is a two-steps process: 1. tokenize text using punctuation marks,
        2. merge over-tokenized units using the lexicon or a regex (for 
        compounds, '^[A-Z][a-z]+-[A-Z][a-z]+$').
        """
        
        #=======================================================================
        # STEP 1 : tokenize with punctuation
        #=======================================================================
        text = text.replace(u'\u2019', '\'')
        tokens = self.regexp.findall(text)
        
        #=======================================================================
        # STEP 2 : merge over-tokenized units using the lexicons
        #=======================================================================
        
        # A temporary list used for merging tokens
        tmp_list = []
        # First counter
        i = 0
        # Second counter
        j = 0
        
        # Loop and search for mis-tokenized tokens
        while i < len(tokens):
            # The second counter indicates the ending character
            j = i
            # While the second counter does not exceed the last word
            while j <= len(tokens):
                # The candidate container
                candidate = ''
                # Construct the candidate token from i to j
                for k in range(i, j):
                    candidate += tokens[k]
                # If the candidate word must be tokenized (in the dictionary or
                # corresponds to a compound with uppercase first letters)
                if candidate.lower() in self.lexicon or \
                   (re.search(r'(?u)^[A-Z]\w+-[A-Z]\w+$', candidate) and \
                    j-i < 3):
                    # Place first counter on the last word
                    i = j-1
                    # Replace the i-th token by the candidate
                    tokens[i] = candidate
                    # Stop the candidate construction
                    break                    
                # Increment second counter
                j += 1
            # Add the token to the temporary list
            tmp_list.append(tokens[i])
            # Increment First counter
            i += 1
        # Return the tokenized text
        return tmp_list




