""" SVM """
#-*- coding: utf-8 -*-

import os
import sys
import tempfile
from bilbo.components.component import Component, Estimator, Extractor
from configparser import ConfigParser
from bilbo.utils.timer import Timer
import bilbo.utils.svm_datas as svm_datas
from bilbo.utils.dictionaries import generatePickle
from bilbo.components.features.xmlfeatures import XmlFeature
import collections
import pickle
import pkg_resources

import logging
logger = logging.getLogger(__name__)

try:
    import svmutil
    import svm
except ImportError:
    path = os.path.join(os.getcwd(), 'bilbo/libs/libsvm-3.23/python')
    sys.path.append(path)
    try:
        from libsvm import svmutil, svm
    except ImportError as e:
        print('\n\nYou should run "make" !\n\n', file=sys.stderr)


class Svm(Estimator):
    """
    SVM class
    """
    _parser_name = 'svm'
    _module_name = 'svm'
    _auto_config = False 

    def __init__(self, cfg_file, type_config='ini'):
        super(Svm, self).__init__(cfg_file, type_config)
        self._load_vocab()

    def _get_opts(self):
        self.model_file = self.parser.getArgs(self.cfg_file, "modelFile")
        self.output_file = self.parser.getArgs(self.cfg_file, "output")
        self.vocab_file = self.parser.getArgs(self.cfg_file, "vocab")

    def _load_vocab(self):
        pk_file = self.vocab_file.replace(".txt", ".pkl")
        if Svm._auto_config:
            file_pk = self._auto_load('binary', pk_file)
            self._vocab = pickle.load(file_pk)
            file_pk.close()
        else:
            try:
                file_pk = open(pk_file, 'rb')
                self._vocab = pickle.load(file_pk)
                file_pk.close()
            except(pickle.UnpicklingError, ImportError, OSError, EOFError):
                self._vocab = None

    def transform(self, document, mode):
        super(Svm, self).transform(document, mode)

    def _add_to_doc(self, document, results):
        for i, itm in enumerate(results):
            if results[i] != 1:
                document.sections[i].bibl_status = False
        
    def fit(self, document):
        if isinstance(document, str):
            data_file = str(document)
            y, x = svmutil.svm_read_problem(data_file)
        elif isinstance(document, object):
            y = []
            x =[]
            for y_section,x_section in self.extract_xy(self.get_svm_data(document)):
                y.append(y_section)
                x.append(x_section)
        return y,x
                
    def words_iterator(self, section):
        for token in section.tokens:
            if token.str_value!="None":
                yield token.str_value  
    
    def generate_vocab_dict(self, document):
        i = 0;
        wdict = {}
        for section in document.sections:
            for word in self.words_iterator(section):
                try:
                    wdict[word]
                except KeyError:
                    i+=1
                    wdict[word] = i
        return wdict

    def word_count(self, section):
        word_count = {}
        for word in self.words_iterator(section):
            try:
                id_key = self._vocab[word]
                word_count[id_key] = word_count.get(id_key, 0) + 1
            except KeyError:
                pass
        return word_count
    
    def extract_xy(self, data):
        fmt_feats = lambda f: {int(k):int(v) for k,v in f.items()}
        for d_feats in data:
            y = d_feats['classe']
            del(d_feats['classe'])
            yield y, fmt_feats(d_feats)

    def get_svm_data(self, document):
        """
        shape the svm features data for the svm
        :param document: document object of the document
        :returns: svm shaped data
        """
        data = []
        for section in document.sections:                       
            dict_feat = collections.OrderedDict()
            dict_feat['classe'] = 1 if "</bibl>" in section.str_value else -1
            dict_feat.update(self.word_count(section))
            indice = len(self._vocab)
            d = collections.OrderedDict()
            d = {'initial': 'NOINITIAL', 'numbersMixed': 'NONUMBER'}
            for k, v in d.items(): 
                indice = indice + 1
                if XmlFeature.global_boolean(section, k, v):
                    dict_feat[indice] = 1
            count = XmlFeature.punc_counter(section)
            dict_feat[indice + 1 + count] = 1
            data.append(dict_feat)
        self.write_data_svm(data)
        return data
        
    def write_data_svm(self, data):
        data_svm = open(self.output_file, "w")       
        for d in data:
            str_data = ''
            for k, v in d.items():
                if k=='classe':
                    str_data = str_data + str(v) 
                else:
                    str_data = str_data + ' {}:{}'.format(k, str(v))
            str_data = str_data + '\n'
            data_svm.write(str_data)

    def train(self, document):
        """
        Train the SVM model

        :param document: document object
        """
        targs, tkwargs = svm_datas.svm_opts() # model training arguments
        self._vocab = self.generate_vocab_dict(document)
        y, x  =  self.fit(document)
        m = svmutil.svm_train(y, x, *targs)
        svmutil.svm_save_model(self.model_file, m)
        generatePickle(self._vocab, self.vocab_file)

    def predict(self, document):
        """
        tag the new data basde on a given model

        :param document: document object 

        :returns: list of predictions
        """
        logger.info('Start to predict')         
        y,x =  self.fit(document)

        if Svm._auto_config:
            file_name = self._auto_load('file', self.model_file)
            m = svmutil.svm_load_model(file_name)
            pkg_resources.cleanup_resources()
        else : 
            m = svmutil.svm_load_model(self.model_file)
        y_pred, p_acc, p_val = svmutil.svm_predict(y, x, m, "-q")
        return y_pred

    def evaluate(self, document):
        """
        Evaluate the model for the given data. All the data are split into 
        80/20% for the training / testing process

        :param document: document object
        """
        targs, tkwargs = svm_datas.svm_opts() # model training arguments

        self.fit(document)
        data_fd = open("resources/models/note/data_SVM.txt", "r")
        to_dict = True 
        datas_test, datas_pred = svm_datas.fd2labeled_evaluation(data_fd,to_dict,
                                                                 seed=7)
        y_test = []
        y_pred = []
        mfd, modelfile = tempfile.mkstemp(suffix='evaluate_model_')
        os.close(mfd)

        xseqs = []
        yseq = []
        for y, xs in datas_test:
            yseq.append(y)
            xseqs.append(xs)

        model = svmutil.svm_train(yseq, xseqs, *targs)
        
        yseq = []
        xseq = []
        for y, xi in datas_pred:
            yseq.append(0)
            y_test.append(y)
            xseq.append(xi)
        y_pred, autoeval, _ = svmutil.svm_predict(y_test, xseq, model)
        print(autoeval)
        svm_datas.svmRepport(y_test, y_pred) 
