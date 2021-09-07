# -*- coding: utf-8 -*-
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('K', type=int,
                    help='k fold integer')
    parser.add_argument('shuf', type=str,
                    help='shuf file path')
    args = parser.parse_args()
    
    file_shuf = args.shuf
    with open(file_shuf, 'r') as f:
        bibls = list(f)
    
    ratio = args.K
    step = int(len(bibls) * (1 / int(ratio)))
    eval_dir = os.path.dirname(file_shuf)
    for i in range(ratio):
        test = bibls[:step]
        train = bibls[step:]
        train_name = "".join((eval_dir, '/train_', str(i)))
        test_name = "".join((eval_dir, '/test_', str(i)))
        with open(train_name, "w") as file:
            file.write('<TEI xmlns="http://www.tei-c.org/ns/1.0">\n')
            for row in train:
                file.write(row)
            file.write('</TEI>')
        with open(test_name, "w") as file:
            file.write('<TEI xmlns="http://www.tei-c.org/ns/1.0">\n')
            for row in test:
                file.write(row)
            file.write('</TEI>')
        bibls = train + test
