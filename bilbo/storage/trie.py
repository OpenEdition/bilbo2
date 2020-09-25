"""
Trie
"""
NUL = '$'

class Trie:
    """
    The Trie object.
    """
    def __init__(self, filename=None):
        self._data = {}
        if filename:
            for line in open(filename, 'r'):
                seq = line.lower().strip().split()
                self.add(seq)

    def __len__(self):
        return len(self)

    @property
    def data(self):
        """
        data
        """
        return self._data

    def add(self, sequence):
        """
        add element
        """
        iterator = sequence.__iter__()
        dat = self._data

        try:
            while True:
                token = next(iterator).lower()
                if token not in dat:
                    dat[token] = {}

                dat = dat[token]
        except StopIteration:
            pass

        dat[NUL] = {}
