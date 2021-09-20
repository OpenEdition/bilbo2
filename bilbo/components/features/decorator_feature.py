""" decorator class """

class WordDecorator:
    """ WordDecorator class """
    def __init__(self, extractor):
        self.__extractor = extractor

    def __call__(self, section, token_id):
        token = section.token_str_lst[token_id][0]
        return self.__extractor(self, token)


class PositionDecorator:
    """ PositionDecorator Class """
    def __init__(self, extractor):
        self.__extractor = extractor

    def __call__(self, section, token_id):
        taille = len(section.token_str_lst)
        return self.__extractor(self, token_id, taille)


class SectionDecorator:
    """ SectionDecorator Class """
    def __init__(self, extractor):
        self.__extractor = extractor

    def __call__(self, section, *args):
        return self.__extractor(self, section, *args)


class XmlDecorator:
    """ SectionDecorator Class """
    def __init__(self, extractor):
        self.__extractor = extractor

    def __call__(self, section, token_id):
        element = section.section_xml
        token_path = section.tokens[token_id].xpath
        return self.__extractor(self, element, token_path)
