"Component"

from bilbo.libs.opts import BilboParser 
from bilbo.utils.loader import binary_resource_stream, text_resource_stream, filename_resource
import os

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

    def _auto_load(cls, mode, path):
        fname = os.path.basename(path)
        resources = ''.join(('resources.models.', cls.get_parser_name()))
        if mode == 'binary':
            return binary_resource_stream(fname, resources)
        elif mode == 'text':
            return text_resource_stream(fname, resources)
        else:
            return filename_resource(fname, resources)
            

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


