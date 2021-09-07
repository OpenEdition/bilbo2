# -*- coding: utf-8 -*-
import argparse
import os
from itertools import starmap
import csv
from collections import defaultdict
from six.moves import reduce

def assign( x,y,t):
    t[x]=y
    return t


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('file_eval', type=str,
                    help='eval file path')
    parser.add_argument('output', type=str,
                    help='eval file path')
    args = parser.parse_args()
    
    file_name = args.file_eval
    output = args.output

    d = defaultdict(list)
    with open(file_name) as csvfile:
        rdr = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in rdr:
            d[row[0]].append(row[1:])
    labels = dict()
    for k,v in d.items():
        tmp  = [(reduce( lambda x,y: x+y, v), len(v)) for v in list(zip(*v))]
        tmp2 = [reduce(lambda a,b : a / b , t) for t in tmp]
        t = dict()
        name = ['precisions', 'recall', 'f-measure', 'occurences']
        for v in list(zip(name, tmp2)):
            labels[k] = reduce( lambda x,y: assign(x,y,t), v)
        
    sep = "-" * (14+5*9)
    print("GLOBAL K-FOLD EVALUATION")
    print(sep)
    print('{:>14}  {:>9}  {:>9}  {:>9}  {:>9}'\
                .format("label", "precision", "rappel",\
                        "f-measure", "occurences"))
    print(sep)
    tmp1 = list()
    for k,v in labels.items():
        if (k not in ['mean','weighted mean']):
            print('{:>14}  {:>9.3f} {:>9.3f} {:>9.3f} {:>9}'.format(k, v.get('precisions'), v.get('recall'),v.get('f-measure'),v.get('occurences')))
        else:
            st = '{:>14}  {:>9.3f} {:>9.3f} {:>9.3f} {:>9}'.format(k, v.get('precisions'), v.get('recall'),v.get('f-measure'),v.get('occurences'))
            tmp1.append(st)
    print(sep)
    for t in tmp1:
        print(t)
    print(sep)

    csv_data = [["GLOBAL K-FOLD EVALUATION"]]
    csv_data.append(["label", "precision", "rappel", "f-measure", "occurences"])
    line=[]
    mean=[]
    for k,v in labels.items():
        if (k not in ['mean','weighted mean']):
            csv_data.append(["'{}'".format(k),'{:.9f}'.format(v.get('precisions')),'{:.9f}'.format(v.get('recall')),'{:.9f}'.format(v.get('f-measure')),'{:0.0f}'.format(v.get('occurences'))])
        else:
            mean.append(["'{}'".format(k),'{:.9f}'.format(v.get('precisions')),'{:.9f}'.format(v.get('recall')),'{:.9f}'.format(v.get('f-measure')),'{:0.0f}'.format(v.get('occurences'))])
    csv_data.append([])
    csv_data.extend(mean)
    with open(output, 'a') as f:
        writer = csv.writer(f)
        for row in csv_data:
            writer.writerow(row)
