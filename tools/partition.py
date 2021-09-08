# -*- coding: utf-8 -*-
import argparse
import os



def write_in_file(corpus_lst, directory, name):
    corpus_name = "".join((directory, '/', name, '_', str(i)))
    with open(corpus_name, "w") as file:
        file.write('<TEI xmlns="http://www.tei-c.org/ns/1.0">\n')
        for row in corpus_lst:
            file.write(row)
        file.write('</TEI>')
    

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
        write_in_file(test, eval_dir, 'test')
        write_in_file(train, eval_dir, 'train')
        #permutation to reorder corpus for k-fold permutation
        bibls = train + test
