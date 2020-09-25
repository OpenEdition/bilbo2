""" main features """
from bilbo.libs.opts import Parser
from bilbo.components.features.features import FeatureHandler
from bilbo.components.features.localfeatures import LocalFeature
from bilbo.components.features.xmlfeatures import XmlFeature
from bilbo.components.features.externalfeatures import DictionnaryFeature, ListFeature, ExternalFeature
from bilbo.storage.section import Section
from bilbo.storage.document import Document
from bilbo.storage.token import Token
from bilbo.utils.bilbo_logger import get_logger


def create_document(lines):
    sections = list()
    for line in lines:
        tokens = [Token(token, 'Nolabel') for token in line.split()]
        tokens_str = [[token, 'Nolabel'] for token in line.split()]
        sec = Section(line, None, None, tokens, tokens_str)
        sections.append(sec)
    return Document(None, None, None, sections)
    
## Ajouter un module de lecture de fichiers
## Puis transformation en objet pour annoter en features

if __name__ == "__main__":
    args = Parser.parse_arguments()
    verbosity = args.verbose
    logger = get_logger(name=__name__, verbosity=args.verbose)
    configFeatures = args.cfgfeatures
    feat = FeatureHandler(configFeatures)
    if args.input:
        with open(args.input, 'r') as f:
            lines = f.readlines()
    if args.sentence:
        lines = [args.sentence]
    doc = create_document(lines)
    feat.loadFonctionsFeatures()
    doc = feat.transform(doc)
    feat.save_features(doc)
