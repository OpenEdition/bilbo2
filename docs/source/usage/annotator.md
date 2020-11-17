## Annotator bilbo usage

<aside class="warning">
   WARNING!
   You can autoload pre-trained models and pipeline with the Bilbo.load('bibl/bibl_lang') method. You have to give all paths in the config file when you want to train or test your own config : just instantiate bilbo as  Bilbo(doc, 'path_to_your_config'). For note is not already implemented with auloader.
</aside>

### For bibliography (Standard tagging)


```python
imp = Importer('resources/corpus/bibl/test_bibl.xml')
doc = imp.parse_xml('bibl')

Bilbo.load('bibl')

bilbo = Bilbo(doc)
bilbo.run_pipeline('tag', '/tmp/output.xml', format_= None)
```

### For bibliography (With Lang Detection tagging)


```python
imp = Importer('resources/corpus/bibl/test_bibl.xml')
doc = imp.parse_xml('bibl')

Bilbo.load('bibl_lang')

bilbo = Bilbo(doc')
bilbo.run_pipeline('tag', '/tmp/output.xml', format_= None)
```


### For note


```python
imp = Importer('resources/corpus/note/test_note.xml')
doc = imp.parse_xml('note')
bilbo = Bilbo(doc, 'pipeline_note.cfg')
bilbo.run_pipeline('tag', '/tmp/output.xml', format_= None)
```

### Train
Just modify tag parameter to train parameter!! Note: output could be some binaries constructed model (They must be specified in pipeline_bibl.cfg not as parameters in run_pipeline() function. 

### Evaluation (end to end)
For evaluate the models just launch bilbo on your datatest annotated as:


```python
imp = Importer('resources/corpus/bibl/data_test.xml')
doc = imp.parse_xml('bibl')
bilbo = Bilbo(doc, 'pipeline_bibl.cfg')
bilbo.run_pipeline('evaluate', None, None)
```

    -----------------------------------------------------------
             label  precision     rappel  f-measure  occurences
    -----------------------------------------------------------
              abbr      0.874      0.765      0.816        452
         biblScope      0.887      0.571      0.695        594
         booktitle      0.903      0.629      0.742         89
              date      0.716      0.915      0.803        614
           edition      0.690      0.460      0.552        126
              emph      1.000      1.000      1.000          2
            extent      1.000      0.979      0.989         48
          forename      0.929      0.956      0.942        942
           genName      1.000      1.000      1.000          1
           journal      0.823      0.732      0.774        514
          nameLink      0.282      1.000      0.440         11
           orgName      0.902      0.836      0.868        110
             place      0.824      0.933      0.875         15
          pubPlace      0.962      0.934      0.948        379
         publisher      0.936      0.732      0.821        920
               ref      1.000      0.071      0.133         14
           surname      0.937      0.934      0.936        823
             title      0.868      0.889      0.879       5740
    -----------------------------------------------------------
              mean      0.863      0.797      0.828      11394
     weighted mean      0.877      0.852      0.864      11394
    -----------------------------------------------------------


### Evaluation by component
You can evaluate each component. In this case we use bilbo as toolkit usage. Load your annotated data : data format annotated is depended of component used. You have to always generate this data first.
And just launch (for svm for instance)  


```python
svm.evaluate(input_svm_data_format)
```
