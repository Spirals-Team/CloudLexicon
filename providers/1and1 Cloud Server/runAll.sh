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
# This script executes all computations on the 1&1 Cloud Server dataset.
#
# Warning: This file will be deleted in the future in order to be integrated into the CloudLex tool chain.
#

PROVIDER='1and1 Cloud Server'

TOOLCHAIN_DIR=../../toolchain

# Set CloudLex environment variables.
. ${TOOLCHAIN_DIR}/set-cloudlex-environment-variables.sh

echo Generating the CloudLex REST API Dataset for ${PROVIDER}...
python ExtractDatasetURIs.py > "${CLOUDLEX_REST_API_DATASET}"

# Execute CloudLex tool chain.
. ${TOOLCHAIN_DIR}/run-cloudlex-tool-chain.sh
