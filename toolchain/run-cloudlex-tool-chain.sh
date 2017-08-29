#! /bin/sh
################################################################################
#
# Copyright (c) 2017 Philippe Merle, Inria
#
# This file is part of CloudLex.
#
# CloudLex is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CloudLex is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CloudLex.  If not, see <http://www.gnu.org/licenses/>.
#
# Contributors:
# - Philippe Merle <philippe.merle@inria.fr>
#
################################################################################

#
# This script executes all the commands of the CloudLex tool chain excepts the cloud provider specific extractor.
#

echo Computing statistics for ${PROVIDER}...
python ${TOOLCHAIN_DIR}/cloudlex/statistics.py "${DATASETS_DIR}/DatasetURIs.csv" > "${RESULTS_DIR}/statistics.log"

#
# Cloud API Ontology
#

echo Load the Cloud API Ontology for ${PROVIDER}...
python ${TOOLCHAIN_DIR}/cloudlex/ontology.py "${DATASETS_DIR}/DatasetURIs.csv"

echo Generating the XML ontology for ${PROVIDER}...
python ${TOOLCHAIN_DIR}/cloudlex/ontology_xml.py "${DATASETS_DIR}/DatasetURIs.csv" > "${RESULTS_DIR}/${PROVIDER} Ontology.xml"

echo Generating .dot files for ${PROVIDER}...
python ${TOOLCHAIN_DIR}/cloudlex/ontology_graph.py "${RESULTS_DIR}/api/dot" "${DATASETS_DIR}/DatasetURIs.csv"

echo Generating .png files for ${PROVIDER}...
for dotFile in "${RESULTS_DIR}/api/dot/"*.dot
do
  dotFilename=`basename "$dotFile"`
  pngFile=${RESULTS_DIR}/api/"${dotFilename%.dot}".png  
  echo Generating ${pngFile}...
  dot "${dotFile}" -Tpng > "${pngFile}"
done

#
# Detection of patterns and anti-patterns in Cloud API.
#

echo Detecting patterns and anti-patterns for ${PROVIDER}...
python ${TOOLCHAIN_DIR}/cloudlex/detection.py "${DATASETS_DIR}/DatasetURIs.csv" > "${RESULTS_DIR}/detection.log"

echo Generating .dot files for ${PROVIDER}...
python ${TOOLCHAIN_DIR}/cloudlex/detection_graph.py "${RESULTS_DIR}/detection/dot" "${DATASETS_DIR}/DatasetURIs.csv"

echo Generating .png files for ${PROVIDER}...
for dotFile in "${RESULTS_DIR}/detection/dot/"*.dot
do
  dotFilename=`basename "$dotFile"`
  pngFile=${RESULTS_DIR}/detection/"${dotFilename%.dot}".png  
  echo Generating ${pngFile}...
  dot "${dotFile}" -Tpng > "${pngFile}"
done

#
# Cloud Lexicon Ontology
#

echo Generating Lexicon CSV for ${PROVIDER}...
python ${TOOLCHAIN_DIR}/cloudlex/lexicon_csv.py "${DATASETS_DIR}/DatasetURIs.csv" > "${RESULTS_DIR}/lexicon.csv" 

echo Generating Lexicon Tag Cloud for ${PROVIDER}...
python ${TOOLCHAIN_DIR}/cloudlex/lexicon_tag_cloud.py "${RESULTS_DIR}/lexicon_tag_cloud.png" "${DATASETS_DIR}/DatasetURIs.csv"

echo Generating Lexicon Graphs for ${PROVIDER}...
python ${TOOLCHAIN_DIR}/cloudlex/lexicon_graph.py "${RESULTS_DIR}/lexicon/dot" "${DATASETS_DIR}/DatasetURIs.csv"

echo Generating .png files for ${PROVIDER}...
for dotFile in "${RESULTS_DIR}/lexicon/dot/"*.dot
do
  dotFilename=`basename "$dotFile"`
  pngFile=${RESULTS_DIR}/lexicon/"${dotFilename%.dot}".png  
  echo Generating ${pngFile}...
  if [[ `wc -c <"${dotFile}"` -le 75000 ]]; then
    fdp "${dotFile}" -Tpng > "${pngFile}"
  else
    echo WARNING: The \'dot\' command is used instead of the \'fdp\' command for generating "${pngFile}" as this graph is too huge for \'fdp\'!
    dot "${dotFile}" -Tpng > "${pngFile}"
  fi
done
