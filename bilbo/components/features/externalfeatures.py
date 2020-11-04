""" External feature Class """
import os
from bilbo.utils.dictionaries import compile_multiword
from bilbo.utils.loader import binary_resource_stream, text_resource_stream
try:
    import cPickle as pickle
except ImportError:
    import pickle

NUL = '$'

class ExternalFeature:
    """
    ExternalFeature CLass
    generate the feature from external ressources
    """
    _auto_config = False 
    @classmethod
    def factory(cls, typeft, name, list_name):
        """
        Chose between single or multiple tokens feature

        :param typeft: simple or multiple
        :param name: the name of the feature
        :param list_name: list file

        :returns: the right function to call
        """
        if cls is ExternalFeature:
            if typeft == 'simple':
                return ListFeature(name, list_name)
            if typeft == 'multi':
                return DictionnaryFeature(name, list_name)
        return 'WRONG TYPE'

    def _auto_load(self, mode, path):
        fname = os.path.basename(path)
        resources = 'resources.external'
        if mode == 'binary':
            return binary_resource_stream(fname, resources)
        else:
            return text_resource_stream(fname, resources)



class DictionnaryFeature(ExternalFeature):
    """
    Get features from dictionnaries
    """
    def __init__(self, name, filename):
        self._name = name
        self._path = filename
        self._appendice = '$'
        self._list = None
        pk_file = self._path.replace(".txt", ".pkl")
        if DictionnaryFeature._auto_config:
            file_pk = self._auto_load('binary', pk_file)
            self._value = pickle.load(file_pk)
            file_pk.close()
        else:
            try:
                file_pk = open(pk_file, 'rb')
                self._value = pickle.load(file_pk)
                file_pk.close()
            except(pickle.UnpicklingError, ImportError, OSError, EOFError):
                self._value = compile_multiword(self._path)

    def __call__(self, section, token_id):
        self.create_list(section)
        if self._list:
            if self._list[token_id] != 'O':
                return self._name.upper()
            return "NO" + self._name.upper()
        self.create_list(section)
        self.__call__(section, token_id)
        return self._list

    def create_list(self, sequence):
        """
        Create a liste of token from a sequence

        :param sequence: list of token and label associated
                         i.e: [["token", "label"], ["token", "label"]]
        """
        seq = [sequence.token_str_lst[i][0].lower().strip() for i \
                in range(len(sequence.token_str_lst))]
        lis = ["O"]*len(seq)
        tmp = self._value._data
        length = len(seq)
        fst = 0
        lst = -1 # last match found
        cur = 0
        ckey = None  # Current KEY
        appendice = '$'
        while fst < length - 1:
            cont = True
            while cont and (cur < length):
                ckey = seq[cur]
                if NUL in tmp:
                    lst = cur

                tmp = tmp.get(ckey, {})
                cont = len(tmp) != 0
                cur += int(cont)

            if NUL in tmp:
                lst = cur

            if lst != -1:
                lis[fst] = 'B' + appendice
                for i in range(fst + 1, lst):
                    lis[i] = 'I' + appendice
                fst = lst
                cur = fst
            else:
                fst += 1
                cur = fst

            tmp = self._value._data
            lst = -1

        if NUL in self._value._data.get(seq[-1], []):
            lis[-1] = 'B' + appendice
        self._list = lis


class ListFeature(ExternalFeature):
    """
    ListFeature Class
    """
    def __init__(self, name, list_name):
        self._name = name
        self._extern_token = set()
        if ListFeature._auto_config: 
            for line in self._auto_load('text', list_name):
                self._extern_token.add(line.strip().lower())
        else:    
            with open(list_name, 'r') as fds:
                for line in fds:
                    self._extern_token.add(line.strip().lower())

    def __call__(self, section, token_id):
        if section.token_str_lst[token_id][0].lower() in self._extern_token:
            return self._name.upper()
        return ''.join(('NO', self._name.upper()))
