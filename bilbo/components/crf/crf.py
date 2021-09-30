""" crf module """
#!/usr/bin/python3
import os
import tempfile
import logging
import pycrfsuite
import bilbo.utils.crf_datas as crf_datas
from bilbo.components.component import Component, Estimator, Extractor
from bilbo.eval import Evaluation
from bilbo.exceptions import EstimatorError
from bilbo.utils.loader import binary_resource_stream, text_resource_stream

import logging
logger = logging.getLogger(__name__)


class Crf(Estimator):
    """
    CRF class
    """
    _module_name = 'crf' 
    _parser_name = 'crf' 
    _auto_config = False 

    def __init__(self, cfg_file, type_config='ini'):
        super(Crf, self).__init__(cfg_file, type_config)

    def _get_opts(self):
        self.patterns_file = self.parser.getArgs(self.cfg_file, "patternsFile")
        self.model_file = self.parser.getArgs(self.cfg_file, "modelFile")
        self.name = self.parser.getArgs(self.cfg_file, "name")
        self.seed = self.parser.getArgs(self.cfg_file, "seed")
        self.option_crf = self.parser.getArgs(self.cfg_file, "optionCrf")
        self.verbose_crf = self.parser.getArgs(self.cfg_file, "verboseCrf", type_opt='eval')[0]
        self.algo_crf = self.parser.getArgs(self.cfg_file, "algoCrf")
        self.constraint = self.parser.getArgs(self.cfg_file, "constraint", type_opt='dict')

    def fit(self, document, keep_on_doc=False):
        if isinstance(document, list):
            data_fd = document
        else:
            data_fd = self.get_crf_data(document, keep_on_doc)
        if Crf._auto_config:
            pattern_fd = self._auto_load('text', self.patterns_file)
            patterns = crf_datas.fd2patterns(pattern_fd)
            pattern_fd.close()
        else:            
            with open(self.patterns_file, 'r') as pattern_fd:
                patterns = crf_datas.fd2patterns(pattern_fd)
        if not data_fd:
            msg = 'No one section is been processed for this estimator'
            logger.error(msg)
            raise EstimatorError(msg) 
        xyseq = crf_datas.extract_y(crf_datas.fd2sections(data_fd, ' '))
        dats = crf_datas.apply_patterns(xyseq, patterns)
        return dats, data_fd 
    
    def get_crf_data(self, document, keep_on_doc):
        """
        append the features data for the crf

        :param document: document object or file

        :returns: crf data shaped
        """
        logger.info('Start to append features for crf data')         
        data = []
        for sec in document.sections:
            if sec.check_constraint(self.constraint):
                for tok in sec.tokens:
                    if tok.str_value == "None":
                        continue
                    feature = tok.str_value+" "
                    for key in document.keys:
                        feature += tok.features.get(key, key)+" "
                    feature += tok.label
                    data.append(feature)
                data.append('')
        return data

    def _add_to_doc(self, document, results):
        cpt_crf_res = 0
        for sec in document.sections:
            if sec.check_constraint(self.constraint):
                section_result = results[cpt_crf_res]
                for j, tok in enumerate(sec.tokens):
                    _ , tok.predict_label = section_result[j]
                cpt_crf_res += 1

    def transform(self, document, mode):
        logger.info('Start to transform with the transformer: {}'.format(Crf._parser_name))
        super(Crf, self).transform(document, mode)

    def train(self, document):
        """
        train the model given the options

        :param document: document object or file
        """
        t_opts = crf_datas.trainer_opts(self.name, self.option_crf)
        trainer = pycrfsuite.Trainer(self.algo_crf, params=t_opts, verbose=self.verbose_crf)
        (dats, _) = self.fit(document, keep_on_doc=True)
        for xseq, yseq in dats:
            yseq = [y if y != None else "Nolabel" for y in yseq]
            trainer.append(xseq, yseq)
        trainer.train(self.model_file)

    def predict(self, document):
        """
        tag document's tokens given a model

        :param document: document object or file

        :returns: list of token and label tagged
        """
        logger.info('Start to predict')    
        dats, data_fd = self.fit(document)
        result = self.tag_list(dats)
        
        xyseq = crf_datas.extract_y(crf_datas.fd2sections(data_fd, ' '))
        
        result_label = []
        labl = []
        cpt = 0
        for res in xyseq:
            for i in range(len(res[0])):
                labl.append([res[0][i][0], result[cpt][i]])
            result_label.append(labl)
            labl = []
            cpt += 1
        return result_label


    def tag_list(self, dats):
        """
        Instanciate a tagger for each section in order to benchmark
        model loading and eventually detect memory leaks
        In reality not tagger is not loaded every time

        :param dats: BenchMarkDatas child class instance
        """
        all_result = []
        tagger = pycrfsuite.Tagger()
        if Crf._auto_config:
            file_pk = self._auto_load('binary', self.model_file)
            tagger.open_inmemory(file_pk.read())
            file_pk.close()
        else:
            tagger.open(self.model_file)
        for i, (xseq, _) in enumerate(dats):
            result = tagger.tag(xseq)
            all_result.append(result)
        tagger.close()
        return all_result

    def evaluate(self, document):
        """
        Extract y_true and y_pred from reference's file and from tag's file
        And print the evaluation.

        :param document: document object or file
        """
        pattern_fd = open(self.patterns_file, 'r')
        if isinstance(document, list):
            datas_fd = document
        else:
            datas_fd = self.fit(document)

        fd, modelfile = tempfile.mkstemp(prefix='bilbo_evaluation',
                                         suffix='_crfsuite.model')
        os.close(fd)
        sections = crf_datas.fd2sections(datas_fd, ' ')
        tsecs, vsecs = crf_datas.sections2evaluate(sections, seed=int(self.seed))
        t_opts = crf_datas.trainer_opts(self.name, self.option_crf)

        patterns = crf_datas.fd2patterns(pattern_fd)

        # training
        trainer = pycrfsuite.Trainer(self.algo_crf, params=t_opts, verbose=False)
        xyseq = crf_datas.extract_y(tsecs)
        for xseq, yseq in crf_datas.apply_patterns(xyseq, patterns):
            yseq = [y if y != None else "Nolabel" for y in yseq]
            trainer.append(xseq, yseq)

        trainer.train(modelfile)
        # labeling
        tagger = pycrfsuite.Tagger()
        tagger.open(modelfile)

        xyseq = crf_datas.extract_y(vsecs)
        y_test = []
        y_pred = []
        for xseq, yseq in crf_datas.apply_patterns(xyseq, patterns):
            y_test += yseq
            y_pred += tagger.tag(xseq)
        
        cm = Evaluation(y_test, y_pred, "large")
        cm.get_confusion_matrix()

        precisions, recalls, f_measures, counts, macro = cm.evaluate()

        cm.print_std(precisions, recalls, f_measures, counts, macro)
        cm.print_csv(precisions, recalls, f_measures, counts, macro, "eval_to_del.csv")
        os.unlink(modelfile)

