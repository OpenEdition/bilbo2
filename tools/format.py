# -*- coding: utf-8 -*-
import argparse
import os
from itertools import starmap
import csv
from collections import defaultdict
from six.moves import reduce

if __name__ == "__main__":

    d = defaultdict(list)
    with open("/tmp/test/tmpeval") as csvfile:
        #next(csvfile)
        rdr = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in rdr:
            d[row[0]].append(row[1:])
        print(d)
    for k,v in d.items():
        print(k)
        print(list(zip(*v)))
        print([(reduce( lambda x,y: x+y, v), len(v)) for v in list(zip(*v))])
        break
    

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
