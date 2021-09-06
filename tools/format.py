# -*- coding: utf-8 -*-
import argparse
import os
from itertools import starmap
import csv
from collections import defaultdict
from six.moves import reduce

def assign( x,y,t):
    print(x)
    print(y)
    print(t)
    t[x]=y
    print(t)
    return t


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('file_eval', type=str,
                    help='eval file path')
    args = parser.parse_args()
    
    file_name = args.file_eval

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
    print(sep)
    print("GLOBAL K-FOLD EVALUATION")
    print('{:>14}  {:>9}  {:>9}  {:>9}  {:>9}'\
                .format("label", "precision", "rappel",\
                        "f-measure", "occurences"))
    for k,v in labels.items():
        print('{:>14}  {:>9.3f} {:>9.3f} {:>9.3f} {:>9}'. format(k, v.get('precisions'), v.get('recall'),v.get('f-measure'),v.get('occurences')))

    

        #print(v)
        #list (map (lambda x,y: x+y, v))
    

  #  total = sum(int(r[1]) for r in csv.reader(fin))

  #  parser = argparse.ArgumentParser(description='Process some integers.')
  #  parser.add_argument('K', type=int,
  #                  help='k fold integer')
  #  parser.add_argument('shuf', type=str,
  #                  help='shuf file path')
  #  args = parser.parse_args()

  #  file_shuf = args.shuf
  #  with open(file_shuf) as f:
  #      bibls = list(f)

  #  ratio = args.K
  #  step = int(len(bibls) * (1 / int(ratio)))
  #  eval_dir = os.path.dirname(file_shuf)
  #  for i in range(ratio):
  #      test = bibls[:step]
  #      train = bibls[step:]
  #      train_name = "".join((eval_dir, '/train_', str(i)))
  #      test_name = "".join((eval_dir, '/test_', str(i)))
  #      print(len(train), len (test), len(bibls))
  #      with open(train_name, "w") as file:
  #          file.write('<TEI xmlns="http://www.tei-c.org/ns/1.0">\n')
  #          for row in train:
  #              file.write(row)
  #          file.write('</TEI>')
  #      with open(test_name, "w") as file:
  #          file.write('<TEI xmlns="http://www.tei-c.org/ns/1.0">\n')
  #          for row in test:
  #              file.write(row)
  #          file.write('</TEI>')
  #      bibls = train + test
