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
# This script sets all the CloudLex environment variables.
#

CLOUDLEX_TOOLCHAIN_DIR=$TOOLCHAIN_DIR # TODO: `dirname "$0"` 
CLOUDLEX_PROVIDER=$PROVIDER # TODO: `basename `pwd``
CLOUDLEX_TARGET_DIR=.
CLOUDLEX_DATASETS_DIR="${CLOUDLEX_TARGET_DIR}/datasets"
CLOUDLEX_REST_API_DATASET="${CLOUDLEX_DATASETS_DIR}/DatasetURIs.csv"
CLOUDLEX_RESULTS_DIR="${CLOUDLEX_TARGET_DIR}/results"

export PYTHONPATH=${CLOUDLEX_TOOLCHAIN_DIR}:$PYTHONPATH

echo All CloudLex environment variables are set for ${CLOUDLEX_PROVIDER}.

# TODO: Both following lines must be removed when all /providers/*/runAll.sh scripts will used the new CLOUDLEX_ variable names.
DATASETS_DIR="${CLOUDLEX_DATASETS_DIR}"
RESULTS_DIR="${CLOUDLEX_RESULTS_DIR}"
