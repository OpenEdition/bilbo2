# Evaluation


It is not easy in a pipelines to evaluate the revelance of each algorithm and the relevance of a series of algorithms. As bilbo is constructed as a toolkit for researcher, we can evaluate each pipeline and doing a end to end evaluation. In some cases, a component library can handle its own evaluation. In all cases we rebuilt a confusion matrix.

## End to End Evaluation

For a end to end evaluation, split your dataset in train and test then you need to train first:
```
python3 -m bilbo.bilbo --action train -c MY_PIPELINE.cfg -i DATA_TRAIN.xml -t tag
```

Then, evaluate:
```
python3 -m bilbo.bilbo --action evaluate -c MY_PIPELINE.cfg -i DATA_TEST.xml -t tag
```

## Evaluation by component

For evaluate one component, you need to create the input standart format of your library (the features matrice fitted to your library):

```
python3 -m bilbo.bilbo --action train -c MY_PIPELINE.cfg -i DATA_SET.xml -t tag
```

Check in MY_PIPELINE.cfg the path to your input standart standart format of your component.


Then evaluate:

```
python3 -m bilbo.components.MY_COMPONENT -cf MY_PIPELINE.cfg -i INPUT_STANDART_COMPONENT --evaluate
```

## K-Fold Croos Validation

For easier use, a bash and python scripts are avalaible for doing K-Fold Cross Validation.

Utilisation : bash tools/eval.sh DIR_TO_CORPUS/  DIR_TO_OUTPUT/ K_FOLD_INTEGER PATH_CONFIG_FILE
Keep in mind to give directories with the slash  '/'.

OUTPUT are std_out, train and test file splitting and a summary file (evaluation.csv) of the different evaluations.


```
cd bilbo2
bash tools/eval.sh ../bibl/ ../test/ 5 bilbo/config/pipeline_bibl.cfg
```

## Examples

For resultat and evaluation of bilbo: [Resultat](scores.html) 


