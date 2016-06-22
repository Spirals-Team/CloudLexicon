#! /bin/sh
#
# This script executes all computations on the OCCI dataset.
#

ROOT_DIR=../..
DATASET_DIR=${ROOT_DIR}/dataset/OCCI
RESULTS_DIR=${ROOT_DIR}/results/OCCI

echo Merging the URI dataset for OCCI...
cat ${DATASET_DIR}/infrastructure.csv ${DATASET_DIR}/platform.csv ${DATASET_DIR}/sla.csv ${DATASET_DIR}/crtp.csv ${DATASET_DIR}/monitoring.csv  > ${DATASET_DIR}/DatasetURIs.csv
 
echo Generating the Resource dataset for OCCI...
python OCCIURI2Resource.py ${DATASET_DIR}/DatasetURIs.csv > ${DATASET_DIR}/01OCCIResources.csv

echo Extracting services of the OCCI URI dataset...
python ../common/ExtractServices.py ${DATASET_DIR}/DatasetURIs.csv | sort --reverse --key=2 --field-separator=, --numeric-sort > ${RESULTS_DIR}/services.csv

echo Extracting request types of the OCCI URI dataset...
python ../common/ExtractRequestTypes.py ${DATASET_DIR}/DatasetURIs.csv | sort --reverse --key=2 --field-separator=, --numeric-sort > ${RESULTS_DIR}/request_types.csv

echo Extracting all words of the OCCI URI dataset...
python ../common/ExtractAllWords.py ${DATASET_DIR}/DatasetURIs.csv > ${RESULTS_DIR}/words.csv

echo Counting word occurrences of the OCCI URI dataset...
python ../common/CountWordOccurrences.py ${RESULTS_DIR}/words.csv | sort --reverse --key=2 --field-separator=, --numeric-sort > ${RESULTS_DIR}/word_occurrences.csv
