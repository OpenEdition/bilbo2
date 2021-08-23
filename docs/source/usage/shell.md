```python
import configparser
from bilbo.importer import Importer
from bilbo.components.shape_data.shape_data import ShapeSection
from bilbo.components.features.features import FeatureHandler
from bilbo.components.crf.crf import Crf
from bilbo.bilbo import Bilbo

```

## Bilbo in a shell

### Construct Data Structure
First import your xml document. You can import string or a file. For any action (machine learning prediction, features extraction, set a new xml properties), you will handle this document object.



```python
#xml_str = '<xml>Oustide<bibl><pubPlace>Marseille</pubPlace>, <sponsor>OpenEdition is "! inside </sponsor>>a bibl</bibl></xml>'
xml_str = """<TEI xmlns="http://www.tei-c.org/ns/1.0"> Outside 
<bibl>Hillier B., 1996, <hi>Space is the Machine</hi>, Cambridge University Press, <pubPlace>Cambridge.</pubPlace>
</bibl></TEI>"""
imp = Importer(xml_str)
doc = imp.parse_xml('bibl', is_file = False)
```

### Tokenize, extract and wrap xml informations

First, load parameters. 


```python
dic = """                                                      
[shaper]                        
tagsOptions = {                                                                                 
    "pubPlace": "place",
    "sponsor": "publisher"
    } 
verbose = True
"""
#Load the dic.
#There are differnt ways to set parameters (ini file...)see: https://docs.python.org/3/library/configparser.html#quick-start
config = configparser.ConfigParser(allow_no_value=True) 
config.read_string(dic)
```

Use ShapeSection class.
Note at any moment you can call help for parameters function:


```python
help(ShapeSection.__init__)
```

    Help on function __init__ in module bilbo.components.shape_data.shape_data:
    
    __init__(self, cfg_file, type_config='ini', lang='fr')
        Initialize self.  See help(type(self)) for accurate signature.
    



```python
sh = ShapeSection(config, type_config='Dict')
sh.transform(doc)
```




    <bilbo.storage.document.Document at 0x7fc3740d7390>



To see an overview of your document:


```python
for section in doc.sections:
    for token in section.tokens:
        print('Token:{0}\t\t Label:{1}'.format(token.str_value, token.label))
```

    Token:Hillier		 Label:bibl
    Token:B.		 Label:bibl
    Token:,		 Label:c
    Token:1996		 Label:bibl
    Token:,		 Label:c
    Token:Space		 Label:hi
    Token:is		 Label:hi
    Token:the		 Label:hi
    Token:Machine		 Label:hi
    Token:,		 Label:c
    Token:Cambridge		 Label:bibl
    Token:University		 Label:bibl
    Token:Press		 Label:bibl
    Token:,		 Label:c
    Token:Cambridge		 Label:place
    Token:.		 Label:c


### Features

Set features that you are needed. For external features, you need to give the right path to externals lists...


```python
dic = """                                                      
[features]
listFeatures = numbersMixed, cap, dash, biblPosition, initial
listFeaturesRegex = ('UNIVERSITY', '^Uni.*ty$')
listFeaturesExternes = ('surname', 'surname_list.txt', 'simple'),
listFeaturesXML = italic
output = output.txt 
verbose = False 
"""
config = configparser.ConfigParser(allow_no_value=True) 
config.read_string(dic)
```

Features are given for convenience in  Crf++ format.


```python
feat = FeatureHandler(config, type_config='Dict')
feat.loadFonctionsFeatures()
doc = feat.transform(doc)
feat.print_features(doc)
```

    Hillier NONUMBERS FIRSTCAP NODASH BIBL_START NOINITIAL NOUNIVERSITY SURNAME NOITALIC bibl
    
    B. NONUMBERS ALLCAP NODASH BIBL_START INITIAL NOUNIVERSITY NOSURNAME NOITALIC bibl
    
    , NONUMBERS NONIMPCAP NODASH BIBL_START NOINITIAL NOUNIVERSITY NOSURNAME NOITALIC c
    
    1996 NUMBERS NONIMPCAP NODASH BIBL_START NOINITIAL NOUNIVERSITY NOSURNAME NOITALIC bibl
    
    , NONUMBERS NONIMPCAP NODASH BIBL_START NOINITIAL NOUNIVERSITY NOSURNAME NOITALIC c
    
    Space NONUMBERS FIRSTCAP NODASH BIBL_START NOINITIAL NOUNIVERSITY NOSURNAME ITALIC hi
    
    is NONUMBERS ALLSMALL NODASH BIBL_IN NOINITIAL NOUNIVERSITY NOSURNAME ITALIC hi
    
    the NONUMBERS ALLSMALL NODASH BIBL_IN NOINITIAL NOUNIVERSITY NOSURNAME ITALIC hi
    
    Machine NONUMBERS FIRSTCAP NODASH BIBL_IN NOINITIAL NOUNIVERSITY NOSURNAME ITALIC hi
    
    , NONUMBERS NONIMPCAP NODASH BIBL_IN NOINITIAL NOUNIVERSITY NOSURNAME NOITALIC c
    
    Cambridge NONUMBERS FIRSTCAP NODASH BIBL_IN NOINITIAL NOUNIVERSITY NOSURNAME NOITALIC bibl
    
    University NONUMBERS FIRSTCAP NODASH BIBL_END NOINITIAL UNIVERSITY NOSURNAME NOITALIC bibl
    
    Press NONUMBERS FIRSTCAP NODASH BIBL_END NOINITIAL NOUNIVERSITY NOSURNAME NOITALIC bibl
    
    , NONUMBERS NONIMPCAP NODASH BIBL_END NOINITIAL NOUNIVERSITY NOSURNAME NOITALIC c
    
    Cambridge NONUMBERS FIRSTCAP NODASH BIBL_END NOINITIAL NOUNIVERSITY NOSURNAME NOITALIC place
    
    . NONUMBERS NONIMPCAP NODASH BIBL_END NOINITIAL NOUNIVERSITY NOSURNAME NOITALIC c
    


### Make predictions 
First, to get an Document storage object which make sense (not as above, just for demonstration usage). We load right parameters with path_pipeline_bibl:


```python
# This part is a fast resume of TOKENIZER AND FEATURE explain above.
# There are runned again with the appropriate parameter (path to pipeline_bibl.cfg).
imp = Importer(xml_str)
doc = imp.parse_xml('bibl', is_file = False)
bbo = Bilbo(doc, 'pipeline_bibl.cfg')
bbo.shape_data(doc)
bbo.features(doc)
```




    <bilbo.storage.document.Document at 0x7fc3740ac828>



We have now a Document storage object which contains all needed information


```python
# Start to make predictions
tagger = Crf(bbo.config, type_config='Dict')
labels = tagger.predict(doc)

for label in labels:
    for l in label:
        print(l[0], l[1])
```

    Hillier surname
    B. forename
    , c
    1996 date
    , c
    Space title
    is title
    the title
    Machine title
    , c
    Cambridge publisher
    University publisher
    Press publisher
    , c
    Cambridge pubPlace
    . c


### Add prediction at the data structure
Always use transform() function for added prediction to Document storage object. Note for estimator component, three option are availables :'tag', 'train', 'evaluate'  


```python
tagger.transform(doc, 'tag')
```


```python
for section in doc.sections:
    for token in section.tokens:
        print('Token:{0}\t\t Label:{1}'.format(token.str_value, token.predict_label))
```

    Token:Hillier		 Label:surname
    Token:B.		 Label:forename
    Token:,		 Label:c
    Token:1996		 Label:date
    Token:,		 Label:c
    Token:Space		 Label:title
    Token:is		 Label:title
    Token:the		 Label:title
    Token:Machine		 Label:title
    Token:,		 Label:c
    Token:Cambridge		 Label:publisher
    Token:University		 Label:publisher
    Token:Press		 Label:publisher
    Token:,		 Label:c
    Token:Cambridge		 Label:pubPlace
    Token:.		 Label:c

