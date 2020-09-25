#-*- encoding:utf-8 -*-


from bilbo.tokenizers.tokenizers import DefaultTokenizer



class EnglishTokenizer(DefaultTokenizer):
    def tokenize(self, option):
        print("YES")
