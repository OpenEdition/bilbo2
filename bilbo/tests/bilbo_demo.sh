#!/bin/bash


VERBOSE=$1


function check_test {
if [ $? -eq 0 ]; then
	if [[ -z "$VERBOSE" ]]; then
	    echo -e " \t - TEST : OK \n"
	fi
else
    echo -e "  \t - TEST : FAIL \n"
fi
echo -e "  *************** \n"
}


function run_cmd() {
if [[ -z "$VERBOSE" ]]; then
	tmp_file=$(mktemp)
	tmp_err=$(mktemp)
	eval ${1} > $tmp_file 2> $tmp_err
else
	eval ${1}
fi
}

echo -ne  " - LIST ALL COMPONENTS \n\t - Command : python3 -m bilbo.bilbo -L \n"
run_cmd "python3 -m bilbo.bilbo -L"
check_test


echo -ne  " - HELP COMMAND \n\t - Command : python3 -m bilbo.bilbo -h \n"
run_cmd "python3 -m bilbo.bilbo -h"
check_test



echo -ne  " - TOKENIZATION \n\t - Command : python3 -m bilbo.components.shape_data -cf bilbo/config/pipeline_bibl.cfg -s \"Before <bibl>Inside<hi> hi </hi> outside </bibl> after\" \n"

run_cmd "python3 -m bilbo.components.shape_data -cf bilbo/config/pipeline_bibl.cfg -s 'Before <bibl>Inside<hi> hi </hi> outside </bibl> after'" 
check_test



echo -ne  " - EXTRACT FEATURES from a sentence \n\t - Command : python3 -m bilbo.components.features -cf bilbo/config/pipeline_bibl.cfg -s \"Amblard F. ,  2007\" \n"

run_cmd "python3 -m bilbo.components.features -cf bilbo/config/pipeline_bibl.cfg -s 'Amblard F. , 2007' " 
check_test


echo -ne  " - CRF MODULES on fitted data (features already extracted previously) \n\t Command : python3 -m bilbo.components.crf -cf bilbo/config/pipeline_bibl.cfg -i bilbo/testFiles/features.output.txt --tag -vvv \n"
run_cmd "python3 -m bilbo.components.crf -cf bilbo/config/pipeline_bibl.cfg -i bilbo/testFiles/features.output.txt --tag -vvv" 
check_test


echo -ne  "- SVM MODULES on fitted data (features already extracted) \n\t - Command : python3 -m bilbo.components.svm -cf bilbo/config/pipeline_note.cfg -i bilbo/testFiles/data_SVM.txt --tag -v \n"
run_cmd "python3 -m bilbo.components.svm -cf bilbo/config/pipeline_note.cfg -i bilbo/testFiles/data_SVM.txt --tag -v" 
check_test


echo -ne  " - LABELING (full pipeline) on bibl xml \n\t - Command : python3 -m bilbo.bilbo --action tag -c bilbo/config/pipeline_bibl.cfg -i resources/corpus/bibl/test_bibl.xml -t bibl -o /tmp/doc_bibl_annotated.xml -vvvv \n"
run_cmd "python3 -m bilbo.bilbo --action tag -c bilbo/config/pipeline_bibl.cfg -i resources/corpus/bibl/test_bibl.xml -t bibl -o /tmp/doc_bibl_annotated.xml -vvvv"
check_test


echo -ne  " - LABELING (full pipeline) on note xml \n\t - Command : python3 -m bilbo.bilbo --action tag -c bilbo/config/pipeline_note.cfg -i resources/corpus/note/test_note.xml -t note -o /tmp/doc_note_annotated.xml \n"
run_cmd "python3 -m bilbo.bilbo --action tag -c bilbo/config/pipeline_note.cfg -i resources/corpus/note/test_note.xml -t note -o /tmp/doc_note_annotated.xml"
check_test

 
echo -ne  " - CRF MODULES evaluate on fitted data (features already extracted) \n\t Command : python3 -m bilbo.components.crf -cf bilbo/tests/pipeline.cfg -i bilbo/testFiles/feat_train_output.txt --evaluate -v \n"
run_cmd "python3 -m bilbo.components.crf -cf bilbo/tests/pipeline.cfg -i bilbo/testFiles/feat_train_output.txt --evaluate -v" 
check_test
