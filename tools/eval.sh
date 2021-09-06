#!/bin/bash

dirCorpus=${1}
shift
dirEval=${1}
shift
kfold=${1}
shift
config=${1}
shift

tmp="$dirEval"tmp.txt
shuf="$dirEval"shuf.txt
train="$dirEval"train_
test="$dirEval"test_
tmpeval="$dirEval"tmpeval

for entry in "$dirCorpus"*
do
	sed '/<?xml\|<listB\|<\/listB\|<TEI\|<\/TEI/d' $entry >> "$tmp";
done

sort $tmp | uniq -u | shuf -o "$shuf";

python3 -m tools.partition $kfold $shuf

rm "$tmp";
rm "$shuf";


globalEvalFile=${dirEval}evaluation.csv


for ((i=0; i<$kfold; i++));
do
    python3 -m bilbo.bilbo --action train -c $config -i $train$i -t bibl
    python3 -m bilbo.bilbo --action evaluate -c $config -i $test$i -t bibl
    cat eval_to_del.csv >> $globalEvalFile
    echo >> $globalEvalFile
done

cat $globalEvalFile

sed '/\(^\s*$\|^label,precision\)/d' $globalEvalFile | sed "s/'/\"/g" >> $tmpeval

python3 -m tools.format $tmpeval >> $globalEvalFile

#rm $tmpeval

#rm $tmpeval;
#for f in "$train" "$test"
#do
#	echo "$f";
#	sed -i '1 s/^/<TEI xmlns="http:\/\/www.tei-c.org\/ns\/1.0">\n/' "$f";
#	echo "</TEI>" >> "$f";
#done
#
#











#sed '/<?xml\|<listB\|<\/listB\|<TEI\|<\/TEI/d' 


# utilisation : ./eval.sh dirCorpus numberOfpartition prefix percentOfTest [percentOfTest…] -- bilbo options
# exemple     : ./eval.sh Corpus 10 huhu 10 20 30 40 50 -- -u
# it will
#  train on Corpus folder
#  do 10 partitions
#  in Corpus-eval-huhu folder
#  doing 10% 20% 30% 40% 50% of test
# with option -u for bilbo

#dirCorpus=${1/\//}
#shift
#numberOfpartition=$1
#shift
#prefix=$1
#shift
#
#args="$@"
#percents=${args%%--*}
#bilboOptions=${args##*--}
#if [ "$percents" == "$bilboOptions" ]; then
#	bilboOptions=
#fi
#
#for percentOfTest in $percents; do
#	echo "Evaluation for ${percentOfTest}% of test data with $numberOfpartition partition"
#	echo "Bilbo options : $bilboOptions"
#	echo "  partitionning…"
#	python src/bilbo/evaluation/partition.py ${dirCorpus} $percentOfTest $numberOfpartition $prefix;
#	echo "  training…"
#	python src/bilbo/evaluation/bilboTrain.py $bilboOptions ${dirCorpus} $percentOfTest $numberOfpartition $prefix;
#	echo "  annotating…"
#	python src/bilbo/evaluation/bilboAnnotate.py $bilboOptions ${dirCorpus} $percentOfTest $numberOfpartition $prefix;
#	echo "  evaluating…"
#	python src/bilbo/evaluation/bilboEval.py ${dirCorpus} $percentOfTest $numberOfpartition $prefix;
#done;
#
## Création du fichier global de l'évaluation
#globalEvalFile=${dirEval}/evaluation.tsv
#head -n 1 ${dirEval}/${percents%% *}%/evaluation.tsv | sed "s/^/% of test data\t/" > $globalEvalFile
## re-get all files, $percents may not be all of them
#allPercents=`find ${dirEval} -iwholename '*%/evaluation.tsv'|sort|sed -e 's/.*\([0-9][0-9]\)%.*/\1/'`
#for percentOfTest in $allPercents; do
# 	tail -n 1 ${dirEval}/${percentOfTest}%/evaluation.tsv | sed "s/^/${percentOfTest}%\t/" >> $globalEvalFile
# 	echo >> $globalEvalFile
#done;
