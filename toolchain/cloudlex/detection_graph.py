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
# This script generates a dot graph for URIs datasets with pattern annotations.
#

import sys
from cloudlex import ontology
from cloudlex import detection
from cloudlex import ontology_graph

model = ontology.loadDatasets(sys.argv[2:], ontology.DISTINCT_SERVICES)
detection.applyOn(model)
ontology_graph.generateForEachService(sys.argv[1], model)

model = ontology.loadDatasets(sys.argv[2:], ontology.ALL_IN_ONE_SERVICE)
detection.applyOn(model)
ontology_graph.generateAllInOne(sys.argv[1], model)
