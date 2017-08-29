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
# This script generates the URIs Dataset for OVH.
# 

import sys
import csv
import requests
import json

PROVIDER_NAME = 'OVH'

with open(sys.argv[1], 'rU') as csvFile:
	jsonURIs = csv.reader(csvFile, delimiter = ',', quoting=csv.QUOTE_NONE)
	for jsonURI in jsonURIs:
		documentationURI = jsonURI[0]
		response = requests.get(url=documentationURI)
		apiJson = json.loads(response.text)
		providerBaseUrl = apiJson['basePath']
		serviceName = apiJson['resourcePath'][1:].replace('/', ' ') + ' ' + apiJson['apiVersion']
		for api in apiJson['apis']:
			uri = api['path']
			for operation in api['operations']:
				httpMethod = operation['httpMethod']
				description = operation['description']
				print '"' + PROVIDER_NAME + '","' + serviceName + '","' + providerBaseUrl + uri + '","' + httpMethod.upper() + '","' + documentationURI + '","' + description +'"'
