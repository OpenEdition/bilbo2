""" Local features """
from bilbo.components.features.decorator_feature import WordDecorator, PositionDecorator

class LocalFeature:
    """
    Local features class
    """
    @WordDecorator
    def cap(self, word):
        """
        return the morphological feature of a given token

        :param word: word to get the feature from

        :returns: feature for the word
        """
        if word.isupper():
            return "ALLCAP"
        if word.istitle():
            return "FIRSTCAP"
        if word.islower():
            return "ALLSMALL"
        if any(map(str.isupper, word)):
            return "NIMPCAP"
        return "NONIMPCAP"

    @WordDecorator
    def numbersMixed(self, word):
        """
        return if the token is a number or not

        :param word: word to get the feature from

        :returns: feature for the word
        """
        if any(map(str.isdigit, word)):
            return "NUMBERS"
        return "NONUMBERS"

    @WordDecorator
    def dash(self, word):
        """
        return if the token contains a dash or not

        :param word: word to get the feature from

        :returns: feature for the word
        """
        if len(word.split("-")) >= 2:
            count = 0
            for p in word.split("-"):
                if p.replace("(", "").replace(")", "")\
                        .replace("[", "").replace("]", "")\
                        .isdigit() is False:
                    count = 100
                else:
                    continue
            if count > 0:
                return "NODASH"
            elif count == 0:
                return "DASH"
        return "NODASH"

    @WordDecorator
    def initial(self, word):
        """
        return if the token is an initial or not

        :param word: word to get the feature from

        :returns: feature for the word
        """
        if len(word) == 2:
            if word[0].isupper() and word[1] == ".":
                return "INITIAL"
            return "NOINITIAL"
        return "NOINITIAL"

    @PositionDecorator
    def biblPosition(self, indice, taille):
        """
        return the relative position of the token in its section

        :param word: word to get the feature from

        :returns: feature for the word
        """
        position = float(indice/taille)
        if position <= 1/3:
            return 'BIBL_START'
        if 1/3 < position < 2/3:
            return 'BIBL_IN'
        return 'BIBL_END'
