""" bilbo """
#-*- coding: utf-8 -*-
#!/usr/bin/python3
from configparser import ConfigParser

import bilbo.components
from bilbo.libs.opts import Parser
from bilbo.generateXml import GenerateXml
from bilbo.importer import Importer
from bilbo.eval import Evaluation
from bilbo.utils.bilbo_logger import get_logger

class Bilbo:
    """ Bilbo class """
    def __init__(self, document, cfg_file):
        self.document = document
        self.config = self._get_config_parser(cfg_file)
        self.pipeline = self.get_pipeline(self.config)
        #TODO make a logger by default
        #logger = get_logger(verbosity=4)

    def _get_config_parser(self, cfg_file):
        config =ConfigParser()
        config.read(cfg_file)
        return config

    def get_pipeline(self, cfg):
        """
        Get the pipeline for the rest of the process
        """
        return cfg['PIPELINE']['pipeline'].split(",")

    def annotate(self, output_file, format_):
        """
        annotate the document
        """
        self.run_pipeline("tag", output_file, format_)

    def train(self, output_file=None):
        """
        train the system
        """
        self.run_pipeline("train", output_file)

    def evaluate(self, output_file=None):
        """
        evaluate an annotated document
        """
        self.run_pipeline("evaluate", output_file)

    def run_pipeline(self, mode, output, format_):
        """
        Run the process based on the given pipeline

        :param document: XML document
        """
        for steps in self.pipeline:
            if steps == "shape_data":
                self.shape_data(self.document)
            elif steps == "features":
                self.features(self.document)
            elif steps == "svm":
                self.svm(self.document, mode)
            elif steps == "crf":
                self.crf(self.document, mode)
            elif steps == "generate":
                if mode == 'train' or mode == 'evaluate':
                    break
                self.generate_output(self.document, output, format_)
            else:
                return "Wrong steps in the pipeline"

        if mode == "evaluate":
            self.evaluate_model()

    def shape_data(self, document):
        """
        Shape the data / section of the document

        :param document: XML document

        :returns: document with shaped sections
        """
        from bilbo.components.shape_data.shape_data import ShapeSection
        shaped_data = ShapeSection(self.config, type_config='Dict')
        return shaped_data.transform(document)

    def features(self, document):
        """
        Generate the features based on the config file options

        :param document: Shaped document

        :returns: document with features
        """
        from bilbo.components.features.features import FeatureHandler
        feat = FeatureHandler(self.config, type_config='Dict')
        feat.loadFonctionsFeatures()
        document = feat.transform(document)
        return document

    def crf(self, document, mode):
        """
        Run a crf on a corpus (can train, test or evaluate)

        :param document: Shaped and featured document
        """
        from bilbo.components.crf.crf import Crf
        crf = Crf(self.config, type_config='Dict')
        return crf.transform(document, mode)
            
        #if mode == "evaluate":
        #    crf.evaluate(document)

        #else:
        #    print("Error: Mauvais mode: choisir l'option\
        #            -m [train / tag / evalluate]")

    def generate_output(self, document, output, format_):
        """
        Generate the XML final file

        :param document: document object
        :param res_label: list of predicted label
        :param output_file: output file
        """
        gen = GenerateXml()
        gen.generate_xml(document, output, format_)

    def evaluate_model(self):
        """
        evaluate the model based on the document structure
        """
        pred = []
        gold = []
        for sec in self.document.sections:
            for tok in sec.tokens:
                predict = tok.predict_label if tok.predict_label is not None else 'note'
                pred.append(predict)
                gold.append(tok.label)

        cm = Evaluation(gold, pred, "large")
        cm.get_confusion_matrix()

        precisions, recalls, f_measures, counts, macro = cm.evaluate()

        cm.print_std(precisions, recalls, f_measures, counts, macro)
        cm.print_csv(precisions, recalls, f_measures, counts, macro, "eval_to_del.csv")

    def svm(self, document, mode):
        """
        run a svm on a corpus (can train, test, evaluate)

        :param document: shaped and features document
        """
        from bilbo.components.svm.svm import Svm
        svm = Svm(self.config, type_config='Dict')
        svm.transform(document, mode)

if __name__ == "__main__":
    ## Args parser
    parser = Parser.get_parser(name='python3 -m bilbo.bilbo')
    parser.add_argument('--listcomponents', '-L', action="store_const",\
            default=False, const=True)
    parser.add_argument('--cfgfile', '-c', type=str, default='bilbo/config/pipeline_bibl.cfg',\
            help='Pipeline configuration file (default: %(default)s)')
    parser.add_argument('--action', '-a', type=str, default='tag',\
            choices=['train', 'tag', 'evaluate'])
    parser.add_argument('--output', '-o', type=str,\
            default="bilbo/testFiles/output.xml", help='Tagging output file (default: %(default)s)')
    parser.add_argument('--input', '-i', type=str,\
            help='Path to input file to tag')
    parser.add_argument('--tagname', '-t', type=str, default='bibl',\
            choices=['bibl', 'note'])
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Set level of verbosity')
    parser.add_argument('--format', '-f', type=str,\
            choices=['TEI', 'JATS', 'RESEARCH'], default="TEI", help='XML format of output file (default: %(default)s)')

    args = Parser.parse_arguments()
    if args.listcomponents:
        mode_infos = bilbo.components.load_components()
        for mname in mode_infos:
            print('\t- %s : "%s"' % (mname, mode_infos[mname]['pkg'].__doc__))
        exit(0)
    verbosity = args.verbose
    logger = get_logger(verbosity=args.verbose)

    importer = Importer(args.input)
    tag_separator = args.tagname
    output = args.output
    format_ = args.format
    doc = importer.parse_xml(tag_separator)
    logger.debug('Instantiate Bilbo')

    bilbo = Bilbo(doc, args.cfgfile)
    
    bilbo.run_pipeline(args.action, output, format_)
