"Component"

from bilbo.libs.opts import BilboParser 

class Component:
    """Component abstract Class"""
    _parser_name = None


    @classmethod
    def get_parser_name(cls):
        return cls._parser_name


    def __init__(self, cfg_file, type_config):
        self.cfg_file = cfg_file
        self.parser = BilboParser.factory(type_config, self.get_parser_name())
        self._get_opts()

    def _get_opts(self):
        pass

    def fit(self, document):
        pass

    def transform(self, document):
        pass


class Estimator(Component):
    """Estimator Extract Class"""
    def transform(self, document, mode):
        if mode == "train":
            self.train(document)
        elif mode == "tag" or mode== "evaluate":
            results = self.predict(document)
            self._add_to_doc(document, results)
    
    def train(self, document):
        pass

    def predict(self, document):
        pass

    def evaluate(self):
        pass
    
    def _add_to_doc(results):
        pass

    def _from_file_format(document):
        pass

    def _from_bilbo_format(document):
        pass

class Extractor(Component):
    """Extractor Extract Class"""
    def extract_from_section(section, *args):
        pass

    def fit(document):
        pass


