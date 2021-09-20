#!/bin/bash

dirCorpus=${1}
shift
dirEval=${1}
shift
kfold=${1}
shift
config=${1}
shift

train="$dirEval"train_
test="$dirEval"test_
tmpeval="$dirEval"tmpeval
globalEvalFile=${dirEval}evaluation.csv


function split_data() {
tmp="$dirEval"tmp.txt
shuf="$dirEval"shuf.txt
for entry in "$dirCorpus"*
do
	sed '/<?xml\|<listB\|<\/listB\|<TEI\|<\/TEI/d' $entry >> "$tmp";
done
sort $tmp | uniq -u | shuf -o "$shuf";
python3 -m tools.partition $kfold $shuf
rm "$tmp";
rm "$shuf";
}

function evaluate() { 
for ((i=0; i<$kfold; i++));
do
   echo ""
    python3 -m bilbo.bilbo --action train -c $config -i $train$i -t bibl
    echo 'VALIDATION NUMBER:'$i |& tee -a $globalEvalFile
	output=$(echo "$config$test$i" | sed 's/\//_/g' | sed 's/\.//g')
    python3 -m bilbo.bilbo --action evaluate -c $config -i $test$i -t bibl -o $output
    cat "$output" >> $globalEvalFile
    echo >> $globalEvalFile
done
}


function format_result() {
sed '/\(^\s*$\|^label,precision\|^VALIDATION\|^------\)/d' $globalEvalFile | sed "s/'/\"/g" >> $tmpeval
echo ""
python3 -m tools.format $tmpeval $globalEvalFile
rm $tmpeval
}

split_data
rm -f $globalEvalFile
evaluate
format_result
