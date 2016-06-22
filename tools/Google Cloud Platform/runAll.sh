#! /bin/sh
#
# This script executes all computations on the Google Cloud Platform dataset.
#

ROOT_DIR=../..
DATASET_DIR="${ROOT_DIR}/dataset/Google Cloud Platform"
RESULTS_DIR="${ROOT_DIR}/results/Google Cloud Platform"

echo Generating the URI dataset for Google Cloud Platform...
python ExtractDatasetURIs.py "${DATASET_DIR}/GoogleDocURIs.csv" > ${DATASET_DIR}/DatasetURIs.csv

echo Generating the Resource dataset for Google Cloud Platform...
python Google2Resource.py "${DATASET_DIR}/GoogleDocURIs.csv" > ${DATASET_DIR}/01GoogleResources.csv

echo Extracting services of the Google Cloud Platform URI dataset...
python ../common/ExtractServices.py "${DATASET_DIR}/DatasetURIs.csv" | sort --reverse --key=2 --field-separator=, --numeric-sort > ${RESULTS_DIR}/services.csv

echo Extracting request types of the Google Cloud Platform URI dataset...
python ../common/ExtractRequestTypes.py "${DATASET_DIR}/DatasetURIs.csv" | sort --reverse --key=2 --field-separator=, --numeric-sort > ${RESULTS_DIR}/request_types.csv

echo Extracting all words of the Google Cloud Platform URI dataset...
python ../common/ExtractAllWords.py "${DATASET_DIR}/DatasetURIs.csv" > ${RESULTS_DIR}/words.csv

echo Counting word occurrences of the Google Cloud Platform URI dataset...
python ../common/CountWordOccurrences.py "${RESULTS_DIR}/words.csv" | sort --reverse --key=2 --field-separator=, --numeric-sort > ${RESULTS_DIR}/word_occurrences.csv
