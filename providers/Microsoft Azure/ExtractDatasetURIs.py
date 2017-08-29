################################################################################
#
# Copyright (c) 2017 Inria
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
# 
# Contributors:
# - Philippe Merle <philippe.merle@inria.fr>
#
################################################################################

#
# This script generates the URIs Dataset for Microsoft Azure.
#

import sys
from cloudlex import extraction

extraction.extractDatasetURIsFromCsvFileOfSwaggerJsonURIs(
	sys.argv[1],
	'Microsoft Azure',

	# TODO: Must be inferred from Swagger descriptor.
	'https://management.azure.com',

	[
	]
)
