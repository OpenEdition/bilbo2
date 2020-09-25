""" crf data """
#-*- coding: utf-8 -*-

import re
import itertools
import random

def fd2sections(datas_fd, sep=None):
    """
    brief Generator that yield sections of features from a BIOS formated
    content coming from a line generator

    :param datas_fd: iterable: a line generator (as returned by open())
    :param sep: None|str : if None yield single string containing BIOS
                formated features. Else splits lines and features given sep

    :returns: Depends on bios
    """
    init_section = lambda: str() if sep is None else list()
    if sep is None:
        fmt = str
    else:
        fmt = lambda feats: feats.strip('\n').split(sep)
    cur_section = init_section()
    cur_len = 0

    for str_feats in datas_fd:
        feats_len = len(str_feats.strip())
        cur_len += feats_len
        if sep is None:
            cur_section += fmt(str_feats)
        elif feats_len > 0:
            cur_section.append(fmt(str_feats))
        if feats_len == 0:
            if cur_len > 0:
                yield cur_section
                cur_section = init_section()
                cur_len = 0
    if cur_len > 0:
        yield cur_section


def fd2patterns(patterns_fd):
    """
    brief Read a Wapiti pattern file

    :param patterns_fd: iterable : a line generator

    :returns: An array of tuple(name, row, col)
    """
    # Regex for pattern extraction
    # @author https://github.com/chokkan/crfsuite/blob/
    # dc5b6c7b726de90ca63cbf269e6476e18f1dd0d9/example/template.py
    re_macro = re.compile(r'%x\[(?P<row>[\d-]+),(?P<col>[\d]+)\]')

    patterns = []
    content = [line.strip() for line in patterns_fd]
    for lineno, pattern in enumerate(content):
        if pattern.startswith('#'):
            continue
        if pattern.startswith('U'):
            name, macro = pattern.split(':')
            match = re.match(re_macro, macro)
            try:
                patterns.append((name,
                                 int(match.group('row')),
                                 int(match.group('col'))))
            except (ValueError, TypeError, AttributeError) as err:
                raise ValueError('Given input do not seems to be correct \
formatted Wapiti patterns l.%d : "%s" : %s' % (lineno, pattern, err))
        elif pattern.startswith('B'):
            if len(pattern) == 1:
                continue
            print('Bigram templates not supported but found on line %d\
 : "%s"' % (lineno, pattern))
    return patterns

def sections2evaluate(sections, prop=0.8, seed=None):
    """
    brief Split sections into a training and an evaluation part

    :param sections: iterable: items are sections
    :param prop: float : div proportions
    :param seed: int | None: random seed

    :returns: split section fro train / test purposes
    """
    if prop >= 1 or prop <= 0:
        raise ValueError('Expected 0 < prop < 1 but %f found' % prop)
    random.seed(seed)
    secs = [s for s in sections]
    random.shuffle(secs)
    spl = int(len(secs) * prop)
    return secs[:spl], secs[spl:]


def extract_y(sections, nfeatures=None):
    """
    :param sections: iterable : a sections generator (like returned by
                     fd2sections() )
    :param nfeatures: None|int : if None the first line of the first section
                      is expected to be with a label for last feature. Else nfeatures indicate
                      the number of features, sections[x][nfeatures] is the line's label.

    :returns: a generator that yields one tuple(xseq, yseq) per section
    """
    first = []
    if nfeatures is None:
        try:
            first = sections[0]
            sections = sections[1:]
        except TypeError:
            first = sections.__next__()
        nfeatures = len(first[0])-1
        first = [first]
    for nsec, section in enumerate(itertools.chain(first, sections)):
        xseq = []
        yseq = []
        for nfeat, feats in enumerate(section):
            lfeats = len(feats)
            y = None
            if lfeats == nfeatures+1:
                y = feats.pop()
            elif lfeats != nfeatures:
                msg = 'Section #%d line #%d : ' % (nsec, nfeat)
                if lfeats > nfeatures +1:
                    msg += 'too many features'
                elif lfeats < nfeatures:
                    msg += 'not enough features : %d (+label) expected but \
%d found' % (nfeatures, lfeats)
                raise ValueError(msg)
            xseq.append(feats)
            yseq.append(y)
        yield xseq, yseq

def apply_patterns(sections_xyseq, patterns, empty_features=False):
    """
    brief Transform a list of features given patterns

    :param sections_xseq: iterable : a generator on a list of sections
                          features list and labels

    :returns: a generator that yields a list new list of features given
              patterns
    """
    for xseq, yseq in sections_xyseq:
        cursec = []
        for cur, features in enumerate(xseq):
            feats = list()
            for name, row, col in patterns:
                row = cur + row
                if row < 0 or row >= len(xseq):
                    if empty_features:
                        feats.append(name+'=')
                    continue
                value = xseq[row][col]
                value = value.replace(':', '__COLON__')
                feats.append('%s=%s' % (name, value))
            cursec.append(feats)
        yield cursec, yseq

def trainer_opts(name, options):
    """
    brief Return a dict of options for the trainer

    :param name: str : can be wapiti | crfsuite
    :param options: str (dict) with the option of crfsuite

    :returns: a dict
    """
    opts = eval(options)
    #opts = {
            #'c1': 1.0,   # coefficient for L1 penalty
            #'c2': 1e-3,  # coefficient for L2 penalty
            #'max_iterations': 50,  # stop earlier
            # include transitions that are possible, but not observed
     #       'feature.possible_transitions': True
     #       }

    return opts
