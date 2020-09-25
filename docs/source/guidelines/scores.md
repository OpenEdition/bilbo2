# Resultat

## Bibliography tag


### Crf component 


For evaluate Conditional Random Field on the first step of the bibliography pipeline, you have to train crf component and moreover write a crf input format 

```
python3 -m bilbo.bilbo --action train -i resources/corpus/bibl/oe_bibl_en_fr.xml -c bilbo/config/pipeline_bibl1.cfg
```
(AJouter un write features)


For evaluate, just get your input format and launch the module with evaluate parameter. It is possible because python-crf module offers an option with a random seed for split dataset in two dataset (train and test) 

```
python3 -m bilbo.components.crf -cf bilbo/tests/pipeline.cfg -i bilbo/testFiles/features.output.txt --evaluate -vvvvv
```

| label         | precision | rappel | f-measure | occurences |
|---------------|-----------|--------|-----------|------------|
| abbr          | 0.941     | 0.920  | 0.930     | 138        |
| biblScope     | 0.960     | 0.975  | 0.967     | 122        |
| booktitle     | 0.667     | 1.000  | 0.800     | 14         |
| date          | 0.972     | 1.000  | 0.986     | 175        |
| edition       | 0.438     | 0.500  | 0.467     | 14         |
| extent        | 1.000     | 1.000  | 1.000     | 12         |
| forename      | 0.940     | 0.926  | 0.933     | 269        |
| genName       | 0.000     | 0.000  | 0.000     | 1          |
| journal       | 0.773     | 0.829  | 0.800     | 111        |
| nameLink      | 1.000     | 0.667  | 0.800     | 6          |
| orgName       | 0.897     | 0.867  | 0.881     | 30         |
| place         | 1.000     | 1.000  | 1.000     | 5          |
| pubPlace      | 0.947     | 0.969  | 0.958     | 128        |
| publisher     | 0.912     | 0.921  | 0.917     | 292        |
| ref           | 1.000     | 0.500  | 0.667     | 2          |
| surname       | 0.896     | 0.928  | 0.912     | 250        |
| title         | 0.898     | 0.966  | 0.931     | 1563       |
| title_sub     | 1.000     | 1.000  | 1.000     | 8          |
|               |           |        |           |            |
| mean          | 0.847     | 0.832  | 0.839     | 3140       |
| weighted-mean | 0.906     | 0.947  | 0.926     | 3140       |


### End to End evaluation

In this case you need to split by yourself your dataset in two ways (train.xml and test.xml). Below we randomly assign data in two sets (one data train and one dataset), A simple holdout method for validation (80 % data train, 20 % datatest)


```
python3 -m bilbo.bilbo --action train -i resources/corpus/bibl/train.xml -c bilbo/config/pipeline_bibl1.cfg -vvvvv
```

```
python3 -m bilbo.bilbo --action evaluate -i resources/corpus/bibl/test.xml -c bilbo/config/pipeline_bibl1.cfg -vvvvv
```


| label         | precision | rappel | f-measure | occurences |
|---------------|-----------|--------|-----------|------------|
| abbr          | 0.969     | 0.812  | 0.884     | 117        |
| biblScope     | 0.921     | 0.953  | 0.937     | 86         |
| date          | 0.961     | 0.879  | 0.919     | 141        |
| edition       | 0.750     | 0.375  | 0.500     | 8          |
| emph          | 0.000     | 0.000  | 0.000     | 2          |
| extent        | 1.000     | 1.000  | 1.000     | 9          |
| forename      | 0.954     | 0.959  | 0.956     | 217        |
| genName       | 0.000     | 0.000  | 0.000     | 1          |
| journal       | 0.579     | 0.440  | 0.500     | 100        |
| nameLink      | 1.000     | 1.000  | 1.000     | 2          |
| orgName       | 0.375     | 0.600  | 0.462     | 10         |
| place         | 0.000     | 0.000  | 0.000     | 2          |
| pubPlace      | 1.000     | 0.956  | 0.978     | 91         |
| publisher     | 0.860     | 0.877  | 0.869     | 211        |
| ref           | 0.000     | 0.000  | 0.000     | 5          |
| surname       | 0.948     | 0.926  | 0.937     | 216        |
| title         | 0.855     | 0.907  | 0.880     | 1106       |
|               |           |        |           |            |
| mean          | 0.621     | 0.594  | 0.607     | 2324       |
| weighted-mean | 0.876     | 0.881  | 0.879     | 2324       |



## Note tag


In this case, we have to evaluate the classifier algorithm (SVM) (dedicated to get note which contains bibliography) and the CRF components used to annotated bibliographies.


### Crf component evaluation


| label         | precision | rappel | f-measure | occurences |
|---------------|-----------|--------|-----------|------------|
| abbr          | 0.943     | 0.909  | 0.926     | 308        |
| biblScope     | 0.910     | 0.836  | 0.871     | 365        |
| booktitle     | 0.800     | 0.364  | 0.500     | 33         |
| date          | 0.811     | 0.853  | 0.831     | 286        |
| edition       | 0.000     | 0.000  | 0.000     | 27         |
| editor        | 0.000     | 0.000  | 0.000     | 2          |
| extent        | 0.438     | 0.389  | 0.412     | 18         |
| forename      | 0.907     | 0.913  | 0.910     | 332        |
| genName       | 0.000     | 0.000  | 0.000     | 2          |
| journal       | 0.822     | 0.550  | 0.659     | 260        |
| name          | 0.000     | 0.000  | 0.000     | 2          |
| nameLink      | 1.000     | 0.250  | 0.400     | 4          |
| note          | 0.896     | 0.943  | 0.919     | 4986       |
| num           | 0.000     | 0.000  | 0.000     | 3          |
| orgName       | 1.000     | 0.364  | 0.533     | 44         |
| place         | 0.000     | 0.000  | 0.000     | 1          |
| pubPlace      | 0.885     | 0.911  | 0.898     | 135        |
| publisher     | 0.812     | 0.803  | 0.807     | 279        |
| ref           | 1.000     | 0.250  | 0.400     | 4          |
| roleName      | 0.000     | 0.000  | 0.000     | 23         |
| surname       | 0.892     | 0.863  | 0.877     | 344        |
| title         | 0.753     | 0.775  | 0.764     | 2284       |
| w             | 0.885     | 0.966  | 0.924     | 88         |
| mean          | 0.598     | 0.476  | 0.530     | 9830       |
| weighted-mean | 0.852     | 0.866  | 0.859     | 9830       |


### Svm component evaluation
```
python3 -m bilbo.components.svm --evaluate -c bilbo/config/pipeline_note1.cfg -i resources/models/note/data_SVM.txt 
```

Accuracy = 93.3993% (283/303) (classification)
(93.3993399339934, 0.264026402640264, 0.6858941220502061)

|label      | precision | rappel | f-measure | occurences |
|-----------|-----------|--------|-----------|------------|
| 1         | 0.93      | 0.99   | 0.96      | 222        |
| -1        | 0.96      | 0.79   | 0.86      | 81         |
| avg-total | 0.93      | 0.93   | 0.93      | 303        |


### End to End evaluation

In this case you need to split by yourself your dataset in two ways (train.xml and test.xml). Below we randomly assign data in two sets (one data train and one dataset), A simple holdout method for validation (70 % data train, 30 % data test)

Pour les notes:

```
python3 -m bilbo.bilbo --action train -c bilbo/config/pipeline_note1.cfg -i resources/corpus/note/train.xml -t note -vvvv
python3 -m bilbo.bilbo --action evaluate -c bilbo/config/pipeline_note1.cfg -i resources/corpus/note/test.xml -t note -vvvv
```

| label         | precision | rappel | f-measure | occurences |
|---------------|-----------|--------|-----------|------------|
| abbr          | 0.928     | 0.921  | 0.924     | 445        |
| biblScope     | 0.903     | 0.833  | 0.867     | 492        |
| booktitle     | 0.250     | 0.214  | 0.231     | 14         |
| date          | 0.880     | 0.839  | 0.859     | 446        |
| edition       | 0.200     | 0.060  | 0.092     | 67         |
| editor        | 0.000     | 0.000  | 0.000     | 2          |
| extent        | 0.667     | 0.444  | 0.533     | 36         |
| forename      | 0.918     | 0.861  | 0.888     | 495        |
| genName       | 0.000     | 0.000  | 0.000     | 4          |
| journal       | 0.839     | 0.709  | 0.768     | 381        |
| nameLink      | 0.333     | 0.200  | 0.250     | 5          |
| note          | 0.784     | 0.965  | 0.865     | 7393       |
| num           | 0.000     | 0.000  | 0.000     | 1          |
| orgName       | 1.000     | 0.242  | 0.390     | 66         |
| place         | 0.000     | 0.000  | 0.000     | 2          |
| pubPlace      | 0.923     | 0.919  | 0.921     | 248        |
| publisher     | 0.816     | 0.752  | 0.783     | 573        |
| ref           | 0.000     | 0.000  | 0.000     | 4          |
| roleName      | 1.000     | 0.111  | 0.200     | 9          |
| surname       | 0.922     | 0.840  | 0.879     | 524        |
| title         | 0.842     | 0.797  | 0.819     | 3775       |
| w             | 0.945     | 0.902  | 0.923     | 133        |
| mean          | 0.598     | 0.482  | 0.534     | 15115      |
| weighted-mean | 0.822     | 0.879  | 0.850     | 15115      |
