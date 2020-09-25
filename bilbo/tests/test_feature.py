import unittest
from bilbo.components.features.regexfeatures import RegexFeature
from bilbo.components.features.localfeatures import LocalFeature
from bilbo.components.features.externalfeatures import DictionnaryFeature, ListFeature
from bilbo.storage.section import Section
from bilbo.components.features.decorator_feature import WordDecorator, PositionDecorator


def load_section(data):
    return Section(None, None, None,token_str_lst=data)

def load_list_predict(section, function):
    actual = []
    for i in range(len(section.token_str_lst)):
        actual.append(function(section, i))
    return actual


class TestRegexFeature(unittest.TestCase):
    
    def setUp(self):
        pattern =  "^[0-3]?[0-9]/[0-1]?[0-9]/([0-2][0-9])?[0-9][0-9]$"
        self.regex_function = RegexFeature('DATE', pattern)
        data = [['A27/08/1977', 'Nolabel'],
                ['27/08/1977', 'Nolabel']]
        self.section = load_section(data)
    
    def test_match_regex(self):
        actual = self.regex_function(self.section, 1)
        expected = 'DATE'
        self.assertEqual(expected, actual)

    def test_nomatch_regex(self):
        actual = self.regex_function(self.section, 0)
        expected = 'NODATE'
        self.assertEqual(expected, actual)


class TestLocalFeature(unittest.TestCase):
    
    def test_cap(self):
        data = [['WORD', 'Nolabel'],
                ['Word', 'Nolabel'],
                ['word', 'Nolabel'],
                ['woRd', 'Nolabel'],
                [';:.%', 'Nolabel']]
        expected = ['ALLCAP', 'FIRSTCAP', 'ALLSMALL', 'NIMPCAP', 'NONIMPCAP']
        
        cap = getattr(LocalFeature(), 'cap')
        section = load_section(data)
        actual = load_list_predict(section, cap)
        
        self.assertListEqual(expected, actual)

    def test_numbersMixed(self):
        data = [['WOR1D', 'Nolabel'],
                ['WORD', 'Nolabel']]
        expected = ['NUMBERS', 'NONUMBERS']
        
        num = getattr(LocalFeature(), 'numbersMixed')
        section = load_section(data)
        actual = load_list_predict(section, num)
        
        self.assertListEqual(expected, actual)
    
    
    def test_dash(self):
        data = [['(2012-2015', 'Nolabel'],
                ['2012-2015p', 'Nolabel'],
                ['202-20-20', 'Nolabel']]
        expected = ['DASH', 'NODASH', 'DASH']
        
        dash = getattr(LocalFeature(), 'dash')
        section = load_section(data)
        actual = load_list_predict(section, dash)
        
        self.assertListEqual(expected, actual)

    def test_initial(self):
        data = [['M.', 'Nolabel'],
                ['M./', 'Nolabel'],
                ['MR.', 'Nolabel']]
        expected = ['INITIAL', 'NOINITIAL', 'NOINITIAL']
        
        initial = getattr(LocalFeature(), 'initial')
        section = load_section(data)
        actual = load_list_predict(section, initial)
        
        self.assertListEqual(expected, actual)

    def test_biblposition(self):
        data = [['M.', 'Nolabel'],
                ['M./', 'Nolabel'],
                ['M./', 'Nolabel'],
                ['MR.', 'Nolabel'],
                ['MR.', 'Nolabel']]
        expected = ['BIBL_START', 'BIBL_START', 'BIBL_IN', 'BIBL_IN', 'BIBL_END']

        pos = getattr(LocalFeature(), 'biblPosition')
        section = load_section(data)
        actual = load_list_predict(section, pos)

        self.assertListEqual(expected, actual)


class TestDictionnayFeature(unittest.TestCase):

    def setUp(self):
        multiwords = ['façon deu\n', 'façon de\n', ', tester .']
        
        with open('./testdict.txt', 'w') as f:
            f.writelines(multiwords)
        self.dic = DictionnaryFeature('DICT', './testdict.txt')
    
    def test_dict(self):
        data = [['Une', 'Nolabel'],
                ['façon', 'Nolabel'],
                ['de', 'Nolabel'],
                [',', 'Nolabel'],
                ['tester', 'Nolabel']]
        expected = ['NODICT','DICT','DICT','NODICT','NODICT']
        
        section = load_section(data)
        actual = load_list_predict(section, self.dic)
        
        self.assertListEqual(expected, actual)

class TestListFeature(unittest.TestCase):

    def setUp(self):
        simplewords = ['Façon\n', 'de\n', 'teste']
        
        with open('./testlist.txt', 'w') as f:
            f.writelines(simplewords)
        self.list = ListFeature('LIST', './testlist.txt')
    
    def test_dict(self):
        data = [['Une', 'Nolabel'],
                ['façon', 'Nolabel'],
                ['de', 'Nolabel'],
                [',', 'Nolabel'],
                ['tester', 'Nolabel']]
        expected = ['NOLIST','LIST','LIST','NOLIST','NOLIST']
        
        section = load_section(data)
        actual = load_list_predict(section, self.list)
        
        self.assertListEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()


