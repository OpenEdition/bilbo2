""" Features """

import time
from bilbo.components.features.externalfeatures import DictionnaryFeature, ListFeature
from bilbo.components.features.externalfeatures import ExternalFeature
from bilbo.components.features.localfeatures import LocalFeature
from bilbo.components.features.regexfeatures import RegexFeature
from bilbo.components.features.xmlfeatures import XmlFeature
from bilbo.components.component import Component

import logging
logger = logging.getLogger(__name__)

class FeatureHandler(Component):
    """
    Feature handler
    """
    _parser_name = 'features' 
    _auto_config = False 

    def __init__(self, cfg_file, type_config='ini'):
        super(FeatureHandler, self).__init__(cfg_file, type_config)
        ExternalFeature._auto_config = FeatureHandler._auto_config 
        self._orderedFeatures()

    def _get_opts(self):
        self.lst_fct = self.parser.getArgs(self.cfg_file,  "listFeatures", type_opt='lst')
        self.lst_fct_regex = self.parser.getArgs(self.cfg_file, "listFeaturesRegex", type_opt='eval')
        self.lst_fct_ext = self.parser.getArgs(self.cfg_file, "listFeaturesExternes", type_opt='eval')
        self.lst_fct_xml = self.parser.getArgs(self.cfg_file,  "listFeaturesXML", type_opt='lst')
        self.verbose = self.parser.getArgs(self.cfg_file, "verbose")
        self.lst_f_reg = None
        self.lst_f_ext = None

    def _orderedFeatures(self):
        feat_keys = []
        feat_keys.extend(self.lst_fct)
        for key_name, _ in self.lst_fct_regex:
            feat_keys.append(key_name)
        for key_name, _, _  in self.lst_fct_ext:
            feat_keys.append(key_name)
        feat_keys.extend(self.lst_fct_xml)
        self._keys = feat_keys

    def format_to_list(self, doc):
        feats_list = list()
        for sec in doc.sections:
            for tok in sec.tokens:
                feat = tok.str_value+" "
                for key in self._keys:
                    feat += tok.features[key]+" "
                feat += tok.label
                logger.debug('Features extracted: %s' % feat)
                feats_list.append(feat+"\n")
            feats_list.append("\n")
        return feats_list

    def print_features(self, doc):
        for line in self.format_to_list(doc):
            print(line)

    def save_features(self, doc):
        """
        Write the features for each token in the output file specify in the cli

        :param doc: document object
        """
        if self.parser.getArgs(self.cfg_file, "output"):
            with open(self.parser.getArgs(self.cfg_file, "output"), "w") as f:
                f.writelines(self.format_to_list(doc))
        else:
            return
        

    def loadFonctionsFeatures(self):
        """
        Load function for the features
        """
        self.lst_f_ext = {}
        for tuple_lst in self.lst_fct_ext:
            (func_name, lst_name, style_lst) = (tuple_lst[0], tuple_lst[1], tuple_lst[2])
            f_ext = ExternalFeature.factory(style_lst, func_name, lst_name)
            self.lst_f_ext[(func_name, lst_name, style_lst)] = f_ext

        self.lst_f_reg = {}
        for reg_lst in self.lst_fct_regex:
            (func_name, pattern) = (reg_lst[0], reg_lst[1])
            f_reg = RegexFeature(func_name, pattern)
            self.lst_f_reg[(func_name, pattern)] = f_reg

    def transform(self, document):
        """
        Generate the features and push them into the section
        """
        document.keys = self._keys
        for section in document.sections:
            for xml_f in self.lst_fct_xml:
                f_xml = getattr(XmlFeature(), xml_f, None)
                f_xml(section)
            # Features locales
            logger.debug('Start to process local features')         
            for i in range(len(section.token_str_lst)):
                for f_name in self.lst_fct:
                    f_loc = getattr(LocalFeature(), f_name, None)
                    feature = section.tokens[i].features
                    if f_loc is None:
                        raise Exception("La fonction n'existe pas dans le code")
                    else:
                        feature[f_name] = f_loc(section, i)

            for reg_lst in self.lst_fct_regex:
                (fct_name_reg, pattern_reg) = (reg_lst[0], reg_lst[1])
                for i in range(len(section.token_str_lst)):
                    ft = self.lst_f_reg[(fct_name_reg, pattern_reg)](section, i)
                    feature = section.tokens[i].features
                    feature[fct_name_reg] = ft
            
            # Features externes

            logger.info('Start to process external features')         
            for tuple_lst in self.lst_fct_ext: 
                (fct_name_ext, lst_name, style_lst) = (tuple_lst[0], tuple_lst[1], tuple_lst[2])
                for i in range(len(section.token_str_lst)):
                    ft = self.lst_f_ext[(fct_name_ext, lst_name, style_lst)](section, i)
                    feature = section.tokens[i].features
                    feature[fct_name_ext] = ft

            document.section = section
        return document
