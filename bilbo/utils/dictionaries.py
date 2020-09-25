""" dictionaries """
import pickle
from bilbo.storage.trie import Trie
NUL = '$'

def compile_multiword(infile):
    """
    :param infile: str
    """
    trie = Trie()
    for line in open(infile, 'r'):
        seq = line.strip().split()
        trie.add(seq)
    generatePickle(trie, infile)
    return trie

def generatePickle(dic, infile):
    """
    Generate de pickle file

    :param dic: dictionnarie
    :param infile: str

    :returns: pickle file
    """
    pickle_filename = infile.replace("txt", "pkl")
    pfile = open(pickle_filename, 'wb')
    pickle.dump(dic, pfile)
    pfile.close()
