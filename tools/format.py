# -*- coding: utf-8 -*-
import argparse
import os
from itertools import starmap
import csv
from collections import defaultdict
from six.moves import reduce

def assign(x,y,t):
    t[x]=y
    return t

def csv_to_dic(f):
    d = defaultdict(list)
    with open(file_name) as csvfile:
        rdr = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in rdr:
            d[row[0]].append(row[1:])
    return d
    
def reduce_to_mean(dic):
    labels = dict()
    for label,v in d.items():
        #from [[1,2,3],[4,5,6], [7,8,9],[10,11,12]] to [(1+4+7+10, 4),(2+5+8+11, 4),(3+6+9+12, 4))]
        tmp  = [(reduce( lambda x,y: x+y, t), len(t)) for t in list(zip(*v))]
        #from  [(1+4+7+10, 4),(2+5+8+11, 4),(3+6+9+12, 4))] to [(22/4),(26/4),(30/4)]
        means_list = [reduce(lambda a,b : a / b , t) for t in tmp]
        labels =mean_to_dic(labels,label,means_list)
    return labels
    
def mean_to_dic(labels, label, means):
    t = dict()
    name = ['precisions', 'recall', 'f-measure', 'occurences']
    for v in list(zip(name, means)):
        labels[label] = reduce( lambda x,y: assign(x,y,t), v)
    return labels

def print_std(labels):
    sep = "-" * (14+5*9)
    print("GLOBAL K-FOLD EVALUATION")
    print(sep)
    print('{:>14}  {:>9}  {:>9}  {:>9}  {:>9}'\
                .format("label", "precision", "rappel",\
                        "f-measure", "occurences"))
    print(sep)
    global_mean = list()
    for label,v in labels.items():
        if (label not in ['mean','weighted mean']):
            print('{:>14}  {:>9.3f} {:>9.3f} {:>9.3f} {:>9}'.format(label, v.get('precisions'), v.get('recall'),v.get('f-measure'),v.get('occurences')))
        else:
            st = '{:>14}  {:>9.3f} {:>9.3f} {:>9.3f} {:>9}'.format(label, v.get('precisions'), v.get('recall'),v.get('f-measure'),v.get('occurences'))
            global_mean.append(st)
    print(sep)
    for line in global_mean:
        print(line)
    print(sep)
    
def print_csv(labels, output):
    csv_data = [["GLOBAL K-FOLD EVALUATION"]]
    csv_data.append(["label", "precision", "rappel", "f-measure", "occurences"])
    line=[]
    mean=[]
    for label,v in labels.items():
        if (label not in ['mean','weighted mean']):
            csv_data.append(["'{}'".format(label),'{:.9f}'.format(v.get('precisions')),'{:.9f}'.format(v.get('recall')),'{:.9f}'.format(v.get('f-measure')),'{:0.0f}'.format(v.get('occurences'))])
        else:
            mean.append(["'{}'".format(label),'{:.9f}'.format(v.get('precisions')),'{:.9f}'.format(v.get('recall')),'{:.9f}'.format(v.get('f-measure')),'{:0.0f}'.format(v.get('occurences'))])
    csv_data.append([])
    csv_data.extend(mean)
    with open(output, 'a') as f:
        writer = csv.writer(f)
        for row in csv_data:
            writer.writerow(row)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('file_eval', type=str,
                    help='eval file path')
    parser.add_argument('output', type=str,
                    help='eval file path')
    args = parser.parse_args()

    file_name = args.file_eval
    output = args.output

    d = csv_to_dic(file_name)
    labels = reduce_to_mean(d)
    print_std(labels)
    print_csv(labels,output)
