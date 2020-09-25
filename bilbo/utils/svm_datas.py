##  @brief This file contains usefull functions to handle SVM-light input
#   data format.

import os
import os.path
import random

SVM_BIN={'classify': os.path.join('utils', 'svm_classify'),
         'learn': os.path.join('utils', 'svm_learn')}


def fd2features(datas_fd, to_dict=False):
    """
    Process SVM data file
    
    :param to_dict: bool : if true yield values are dict, else strings
    
    :returns: a generator
    """
    
    if not to_dict:
        fmt = lambda s: s.strip('\n')
    else:
        tlab = lambda s: (s[0] if len(s) == 2 else 'label',
                                s[1] if len(s) == 2 else int(s[0]))
        fmt = lambda l: { k:v for k,v in [tlab(l.split(':'))
                                           for l in l.split(' ')
                                           if len(l) > 0]}
    for line in (l.strip('\n') for l in datas_fd):
        yield fmt(line)

def fd2labeled_features(datas_fd, to_dict=False):
    """
    Generator comparable to fd2features but that yield a tuple
     with (label, features)
    
    :param to_dict: bool: if true the features are returned as a dict
                          else a string is yield
    
    :returns: a generator that yield tuples
    """
    if not to_dict:
        fmt_feats = lambda f: ' '.join(('%s:%s' % (k,f[str(k)])
                                        for k in sorted([int(k)
                                                         for k in f])))
    else:
        fmt_feats = lambda f: {int(k):int(v) for k,v in f.items()}

    for feats in fd2features(datas_fd, True):
        y = feats['label']
        del(feats['label'])
        yield y, fmt_feats(feats)
 
def fd2labeled_evaluation(datas_fd, to_dict=False, prop=0.8, seed=None):
    """
    brief Return 2 iterator on training and on evalutation datas (
     same generator than fd2labeled_features
    
    :param to_dict: bool : if true return a dict else a string
    
    :returns: tuple(train_datas, validation_datas)
    """
    if prop <= 0 or prop >= 1:
        raise ValueError('Expected 0 < prop < 1 but got "%s"' % prop)

    if seed is not None:
        random.seed(seed)
    feats = [f for f in fd2labeled_features(datas_fd, to_dict)]
    random.shuffle(feats)
    pivot = int(len(feats) * prop)
    return feats[:pivot], feats[pivot:]

def svm_opts():
    """
    Return kwargs and args for model training given argparse
    parsed arguments

    :param args: NameSpace: as returned by ArgumentParser.parse_argument()
    
    :returns: a tuple(args, kwargs)
    """
    kwargs = {}
    rargs = []
    rargs.append('-t 0')

    return rargs, kwargs

def svmRepport(y_test, y_pred):
    """
    Print the evaluation repport given the test and prediction data

    :param y_test: list of test label (oracle)
    :param y_pred: list of predicted label (same range as test)
    """
    if len(y_test) != len(y_pred):
        print("error, wrong compatibility between test and prediction")

    cpt_class_true = {}
    cpt_class_corr = {}
    cpt_class_find = {}

    for k in range(len(y_test)):
        curr_test = y_test[k]
        curr_pred = y_pred[k]
        if curr_test == curr_pred:
            if curr_test not in cpt_class_corr:
                cpt_class_corr[curr_test] = 1
            else:
                cpt_class_corr[curr_test] += 1

        if curr_test not in cpt_class_true:
            cpt_class_true[curr_test] = 1
        else:
            cpt_class_true[curr_test] += 1

        if curr_pred not in cpt_class_find:
            cpt_class_find[curr_pred] = 1
        else:
            cpt_class_find[curr_pred] += 1

    sep = "-" * (12+5*9)
    print(sep)
    print('{:>12}  {:>9}  {:>9}  {:>9}  {:>9}'\
            .format("label", "precision", "rappel", "f-measure", "occurences"))
    print(sep)
    all_corr = 0
    all_find = 0
    all_true = 0
    all_occu = 0
    for key in cpt_class_true:
        try:
            precision = cpt_class_corr[key] / cpt_class_find[key]
            rappel = cpt_class_corr[key] / cpt_class_true[key]
            fmeasure = 2*(precision*rappel)/(precision + rappel)
            occurences = cpt_class_true[key]

            all_corr += cpt_class_corr[key]
            all_find += cpt_class_find[key]
            all_true += cpt_class_true[key]
            all_occu += cpt_class_true[key]

            print('{:>12}  {:>9.2f}  {:>9.2f}  {:>9.2f}  {:>9}'\
                    .format(key, precision, rappel, fmeasure, occurences))

        except KeyError:
            all_occu += 1
            occurences = 1
            print('{:>12}  {:>9}  {:>9}  {:>9}  {:>9}'\
                    .format(key, "0.00", "0.00", "0.00", occurences))

    all_precision = all_corr/all_find
    all_rappel = all_corr/all_true
    all_fmeasure = 2*(all_precision*all_rappel)/(all_precision + all_rappel)
    print(sep)
    print('{:>12}  {:>9.2f}  {:>9.2f}  {:>9.2f}  {:>9}'\
            .format("avg / total", all_precision, all_rappel, all_fmeasure, all_occu))
    print(sep)
