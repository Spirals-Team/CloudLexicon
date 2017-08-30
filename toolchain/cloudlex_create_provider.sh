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
# This script creates a CloudLex cloud provider folder.
#

CLOUDLEX_PROVIDER=$1

echo Create ${CLOUDLEX_PROVIDER}/
mkdir "${CLOUDLEX_PROVIDER}"

echo Create ${CLOUDLEX_PROVIDER}/datasets/
mkdir "${CLOUDLEX_PROVIDER}/datasets"

echo Create ${CLOUDLEX_PROVIDER}/results/
mkdir "${CLOUDLEX_PROVIDER}/results"

echo Create ${CLOUDLEX_PROVIDER}/results/api/
mkdir "${CLOUDLEX_PROVIDER}/results/api"

echo Create ${CLOUDLEX_PROVIDER}/results/api/dot/
mkdir "${CLOUDLEX_PROVIDER}/results/api/dot"

echo Create ${CLOUDLEX_PROVIDER}/results/lexicon/
mkdir "${CLOUDLEX_PROVIDER}/results/lexicon"

echo Create ${CLOUDLEX_PROVIDER}/results/lexicon/dot/
mkdir "${CLOUDLEX_PROVIDER}/results/lexicon/dot"

echo Create ${CLOUDLEX_PROVIDER}/results/tag_cloud/
mkdir "${CLOUDLEX_PROVIDER}/results/tag_cloud"

echo Create ${CLOUDLEX_PROVIDER}/results/detection/
mkdir "${CLOUDLEX_PROVIDER}/results/detection"

echo Create ${CLOUDLEX_PROVIDER}/results/detection/dot/
mkdir "${CLOUDLEX_PROVIDER}/results/detection/dot"
