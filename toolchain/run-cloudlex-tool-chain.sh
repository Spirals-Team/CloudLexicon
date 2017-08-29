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
# This script executes all the CloudLex tool chain commands excepts the cloud provider specific CloudLex REST API Dataset Extractor.
#

# TODO: Add the execution of the cloud provider specific CloudLex REST API Dataset Extractor, e.g.,
# ./CloudLex_REST_API_Dataset_Extractor <arguments common to all the CloudLex REST API Dataset extractors such as ${CLOUDLEX_REST_API_DATASET}>

echo Computing CloudLex statistics for ${CLOUDLEX_PROVIDER}...
python ${CLOUDLEX_TOOLCHAIN_DIR}/cloudlex/statistics.py ${CLOUDLEX_REST_API_DATASET} > "${CLOUDLEX_RESULTS_DIR}/statistics.log"

#
# CloudLex REST API Ontology
#

echo Loading the CloudLex REST API Dataset for ${CLOUDLEX_PROVIDER}...
python ${CLOUDLEX_TOOLCHAIN_DIR}/cloudlex/ontology.py ${CLOUDLEX_REST_API_DATASET}

echo Generating the CloudLex REST API Ontology for ${CLOUDLEX_PROVIDER}...
python ${CLOUDLEX_TOOLCHAIN_DIR}/cloudlex/ontology_xml.py ${CLOUDLEX_REST_API_DATASET} > "${CLOUDLEX_RESULTS_DIR}/${CLOUDLEX_PROVIDER} Ontology.xml"

echo Generating all the CloudLex REST API .dot graphs for ${CLOUDLEX_PROVIDER}...
python ${CLOUDLEX_TOOLCHAIN_DIR}/cloudlex/ontology_graph.py "${CLOUDLEX_RESULTS_DIR}/api/dot" ${CLOUDLEX_REST_API_DATASET}

echo Generating all the CloudLex REST API .png graphs for ${CLOUDLEX_PROVIDER}...
for dotFile in "${CLOUDLEX_RESULTS_DIR}/api/dot/"*.dot
do
  dotFilename=`basename "$dotFile"`
  pngFile=${CLOUDLEX_RESULTS_DIR}/api/"${dotFilename%.dot}".png  
  echo Generating ${pngFile}...
  dot "${dotFile}" -Tpng > "${pngFile}"
done

#
# CloudLex REST API Patterns and Anti-Patterns Detection.
#

echo Detecting all the CloudLex REST API Patterns and Anti-Patterns for ${CLOUDLEX_PROVIDER}...
python ${CLOUDLEX_TOOLCHAIN_DIR}/cloudlex/detection.py ${CLOUDLEX_REST_API_DATASET} > "${CLOUDLEX_RESULTS_DIR}/detection.log"

echo Generating all the CloudLex REST API Patterns and Anti-Patterns .dot graphs for ${CLOUDLEX_PROVIDER}...
python ${CLOUDLEX_TOOLCHAIN_DIR}/cloudlex/detection_graph.py "${RESULTS_DIR}/detection/dot" ${CLOUDLEX_REST_API_DATASET}

echo Generating all the CloudLex REST API Patterns and Anti-Patterns .png graphs for ${CLOUDLEX_PROVIDER}...
for dotFile in "${CLOUDLEX_RESULTS_DIR}/detection/dot/"*.dot
do
  dotFilename=`basename "$dotFile"`
  pngFile=${CLOUDLEX_RESULTS_DIR}/detection/"${dotFilename%.dot}".png  
  echo Generating ${pngFile}...
  dot "${dotFile}" -Tpng > "${pngFile}"
done

#
# CloudLex Lexicon Ontology
#

echo Generating the CloudLex Lexicon CSV for ${CLOUDLEX_PROVIDER}...
python ${CLOUDLEX_TOOLCHAIN_DIR}/cloudlex/lexicon_csv.py ${CLOUDLEX_REST_API_DATASET} > "${CLOUDLEX_RESULTS_DIR}/lexicon.csv" 

echo Generating all the CloudLex Lexicon Tag Clouds for ${CLOUDLEX_PROVIDER}...
python ${CLOUDLEX_TOOLCHAIN_DIR}/cloudlex/lexicon_tag_cloud.py "${CLOUDLEX_RESULTS_DIR}/lexicon_tag_cloud.png" ${CLOUDLEX_REST_API_DATASET}

echo Generating all the CloudLex Lexicon .dot graphs for ${CLOUDLEX_PROVIDER}...
python ${CLOUDLEX_TOOLCHAIN_DIR}/cloudlex/lexicon_graph.py "${CLOUDLEX_RESULTS_DIR}/lexicon/dot" ${CLOUDLEX_REST_API_DATASET}

echo Generating all the CloudLex Lexicon ..png graphs for ${CLOUDLEX_PROVIDER}...
for dotFile in "${CLOUDLEX_RESULTS_DIR}/lexicon/dot/"*.dot
do
  dotFilename=`basename "$dotFile"`
  pngFile=${CLOUDLEX_RESULTS_DIR}/lexicon/"${dotFilename%.dot}".png  
  echo Generating ${pngFile}...
  if [[ `wc -c <"${dotFile}"` -le 75000 ]]; then
    fdp "${dotFile}" -Tpng > "${pngFile}"
  else
    echo WARNING: The \'dot\' command is used instead of the \'fdp\' command for generating "${pngFile}" as this graph is too huge for \'fdp\'!
    dot "${dotFile}" -Tpng > "${pngFile}"
  fi
done

echo 
echo Done.
echo
