# Configuration File options #

Bilbo comes with a `pipeline_config` file (located at the bilbo/config of the bilbo2 directory). Actually, there is two pipeline_config available, one is for annotating bibliographies references(tag `<bibl>` in the TEI/XML format), one other is for annotating footnote (tag `note` in the TEI/XML format). You can modified each of the options presented in this file.Currently, the file is an INI configuration file. In future we expect to handle json or XML file configuration.
As expected, each module of Bilbo can run on his own. A series (not all) of parsing options are available and can be set with arg cli python running.

## PIPELINE ##
In this part, you have to specify the pipeline wanted. Note that for training it does not make sens to add generate pipeline.
Pipeline is one on this [components](../essential/pipelines.html) before going any further.
This section is marked by:
* `[PIPELINE]`

### verbose ###
Set at False by default

### pipeline ###
You have to chained the desired chained algorithm as instance: 
```ini
PIPELINE=shape_data,features,svm,crf,generate
```

Example:
```ini
[PIPELINE]
PIPELINE=shape_data,features,svm,crf,generate
outputFile=None
verbose=True
```



## SHAPER ##

This section is marked by:
* `[shaper]`

### tokenizerOption ###
This option is currently unnecessary. The next developments regarding tokenization will make it active soon.

### tagOptions ###
This is a wrapper for reduce or rename tag to an other

```ini
tagsOptions = {
	"title_a": "title",
	"distributor": "publisher",
	"country": "place",
	"sponsor": "publisher"
} 
```


Example:
```ini
[PIPELINE]
PIPELINE=shape_data,features,svm,crf,generate
outputFile=None
verbose=True
```



## FEATURES ##

This section is marked by:
* `[features]`

### listFeatures ###
Default Value is set to:
numbersMixed, cap, dash, biblPosition, initial

You can removed some of them or add a new one (see ../developer/modules.html)
This is a wrapper for reduce or rename tag to an other

### listFeaturesRegex ###
You can add a list of regex as :
(name_of_regex, python_regex), (name_of_regex1, python_regex1)


### listFeaturesExternes ###
(unic_named_list, path_to_external_list, List_type), ...

Note type_list is simple (simple word list) or multi (multi word list as journals names for instance)

### listFeaturesXML ###

This is set to italic by default.

### output ###
Path output, it is handling when you use feature component. Output is fitted to CRF++ format data.


Example:
```ini
[features]
listFeatures = numbersMixed, cap, dash, biblPosition, initial
listFeaturesRegex = ('WEBLINK', '^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$')
listFeaturesExternes = ('place', 'resources/external/place_list.txt', 'multi'), 
		     ('possmonth', 'resources/external/month_list.txt', 'simple'), 
		     ('posseditor', 'resources/external/editor_abbr_list.txt', 'simple'), 
		     ('posspage', 'resources/external/page_abbr_list.txt', 'simple'),
		     ('journal', 'resources/external/journals_list.txt', 'multi'),
		     ('surname', 'resources/external/surname_list.txt', 'simple'),
		     ('forename', 'resources/external/forename_list.txt', 'simple')
		     listFeaturesXML = italic
		     output = bilbo/testFiles/features.output.txt 
		     verbose = False 
```


## CRF ##

This section is marked by:
* `[crf]`

### name ###
Name of libraries used, in some cases you can change the crf libraries (for wapiti for instance)


### algoCrf ###

Default value is set to [lbfgs](for https://en.wikipedia.org/wiki/Limited-memory_BFGS)
algorithm : {‘lbfgs’, ‘l2sgd’, ‘ap’, ‘pa’, ‘arow’}

### optionCrf ###

Many option are avalaible . see [crfsuite manual](http://www.chokkan.org/software/crfsuite/manual.html#idp8853531472)

Most important are c1 for a L1 regularisation (in this case algoritm is switch to orthant method), c2 regression ridge and and max_iterations

epsilon : The epsilon parameter that determines the condition of convergence. value set by default at  1e-5


```ini
optionCrf = {
	'c2': 0.00001,
	}
```
### patternsFile ###

path to wapiti pattern. By default pattern used is located in resources/models/bibl/wapiti_pattern_ref


### modelFile ###
Path to the model generated in train action or used in tag action.

### seed ###

This is used to generate a pseudo-random number. This random number is used when you evaluate the crf algorithn only (not the fulle pipeline)


Example:
```ini
[crf]
name = crfsuite
algoCrf = lbfgs
#    lbfgs for Gradient descent using the L-BFGS method,
#    l2sgd for Stochastic Gradient Descent with L2 regularization term
#    ap for Averaged Perceptron
#    pa for Passive Aggressive
#    arow for Adaptive Regularization Of Weight Vector
optionCrf = {
	'c2': 0.00001,
	'max_iterations': 2000,
}
seed = 3
patternsFile = resources/models/note/wapiti_pattern_ref
modelFile = resources/models/note/crf_OE_fr.txt
```




## SVM ###

This section is marked by:
* `[svm]`

### name ###
Name of libraries used, in some cases you can change the svm libraries for an other.

### modelFile ###
Path to the vocab model generated in train action or used in tag action.

### vocab ###
Path to the vocab model generated by svm train. Vocab attribute at each word a integer.

### output ###

Not already implemented 


Example:
```ini
bsvm
modelFile = resources/models/note/svm_OE_fr.txt
vocab = resources/models/note/inputID.txt
output = /tmp/data_SVM.txt
```
