#! /bin/sh
#
# This script executes all computations on the OpenStack dataset.
#

ROOT_DIR=../..
DATASET_DIR=${ROOT_DIR}/dataset/OpenStack
RESULTS_DIR=${ROOT_DIR}/results/OpenStack

echo Generating the list of URIs where the Swagger JSON documentation for OpenStack is...
python OpenStackExtractJSONURIs.py > ${DATASET_DIR}/OpenStackDocURIs.csv

echo Generating the URI dataset for OpenStack...
python ExtractDatasetURIs.py ${DATASET_DIR}/OpenStackDocURIs.csv > ${DATASET_DIR}/DatasetURIs.csv

echo Generating the Resource dataset for OpenStack...
python OpenStack2Resource.py ${DATASET_DIR}/OpenStackDocURIs.csv > ${DATASET_DIR}/01OpenStackResources.csv

echo Extracting services of the OpenStack URI dataset...
python ../common/ExtractServices.py ${DATASET_DIR}/DatasetURIs.csv | sort --reverse --key=2 --field-separator=, --numeric-sort > ${RESULTS_DIR}/services.csv

echo Extracting request types of the OpenStack URI dataset...
python ../common/ExtractRequestTypes.py ${DATASET_DIR}/DatasetURIs.csv | sort --reverse --key=2 --field-separator=, --numeric-sort > ${RESULTS_DIR}/request_types.csv

echo Extracting all words of the OpenStack URI dataset...
python ../common/ExtractAllWords.py ${DATASET_DIR}/DatasetURIs.csv > ${RESULTS_DIR}/words.csv

echo Counting word occurrences of the OpenStack URI dataset...
python ../common/CountWordOccurrences.py ${RESULTS_DIR}/words.csv | sort --reverse --key=2 --field-separator=, --numeric-sort > ${RESULTS_DIR}/word_occurrences.csv
