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

# Iterate over all the cloud providers.
for provider in 'Apache CloudStack' 'Cloud Foundry' 'DigitalOcean' 'Docker Engine' 'Google Cloud Platform' 'Heroku' 'IBM Bluemix' 'Kubernetes' 'Microsoft Azure' 'OCCI' 'OpenStack' 'Oracle Cloud' 'OVH' 'Rackspace' 'VMware' 
do
  cd "$provider"
  sh runAll.sh
  cd ..
done

ALL_DATASETS="*/datasets/DatasetURIs.csv"

wc * ${ALL_DATASETS}

TOOLCHAIN_DIR=../toolchain/cloudlex

export PYTHONPATH=../toolchain:$PYTHONPATH

python ${TOOLCHAIN_DIR}/statistics.py ${ALL_DATASETS} > results/statistics.log

echo Generating the global Lexicon Dataset...
python ${TOOLCHAIN_DIR}/lexicon_csv.py ${ALL_DATASETS} > results/global_lexicon.csv

echo Generating the global Lexicon Tag Cloud...
python ${TOOLCHAIN_DIR}/lexicon_tag_cloud.py results/global_lexicon_tag_cloud.png ${ALL_DATASETS}
