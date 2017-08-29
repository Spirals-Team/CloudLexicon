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
# CloudLex lexicon_tag_cloud module.
#

import sys
from cloudlex import ontology
import pytagcloud

# Warning pytagcloud seems to be bugged as it does not accept a large number of elements in the tags.
MAX_TAG_ELEMENTS = 250

# Load Cloud API datasets.
model = ontology.loadDatasets(sys.argv[2:], ontology.DISTINCT_SERVICES)
nbTotalProviders = len(model.providers)

print "# of terms = " + str(len(model.lexiconOfNounsVerbs.values()))

minimalOccurrences = 1

# Compute data for the tag cloud. 
while True:
	data = []
	for term in model.lexiconOfNounsVerbs.values():
		if nbTotalProviders == 1 and term.occurrences >= minimalOccurrences:
			data.append( ( term.term, term.occurrences) )
		else:
			nbTermProviders = len(term.providers)
			if nbTermProviders > 2:
				data.append( ( term.term, 2**nbTermProviders) )

	if len(data) < MAX_TAG_ELEMENTS:
		break
	else:
		minimalOccurrences += 1
	
print "# of tags = " + str(len(data)) + ' with ' + str(minimalOccurrences) + ' occurrences at least'

if nbTotalProviders == 1:
	tagCloudMaxSize = 60
else:
	tagCloudMaxSize = 120

# Create the tag cloud.
tags = pytagcloud.make_tags(data, maxsize=tagCloudMaxSize, minsize=5)

# Save it as a .png file.
pytagcloud.create_tag_image(tags, sys.argv[1], size=(900, 600), layout=pytagcloud.LAYOUT_HORIZONTAL)
