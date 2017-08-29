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
# This script generates the URIs Dataset for Google Cloud Platform.
#

import csv
import sys
import requests
import json
import string

cloudProvider = 'Google Cloud Platform'
gcpServiceTitle = ''
gcpServiceApiUrl = ''
gcpServiceBaseUrl = ''

def traverseResources(resources):
		for resource in resources:
			resource = resources[resource]
			if 'methods' in resource:
				methods = resource['methods']
				for method in methods:
					method = methods[method]
					if 'flatPath' in method:
						path = method['flatPath']
					else:
						path = method['path']

					# Correct GCP ???? paths.
					path = path.replace('/{projectsId}', '/{projectId}')
					path = path.replace('/{regionsId}', '/{region}')
					# Correct GCP Genomics paths.
					path = path.replace('/{datasetsId}', '/{datasetId}')
					# Correct GCP Service Management paths.
					path = path.replace('/{servicesId}', '/{serviceName}')

					uri = gcpServiceBaseUrl + path
					httpMethod = method['httpMethod']
					description = method['description']
					# Remove line returns.
					description = string.replace(description, '\n', '\\n')
					# Encode quote as double quote for CVS
					description = string.replace(description, '"', '""')
					print '"' + cloudProvider + '","' + gcpServiceTitle + '","' + uri + '","' + httpMethod + '","' + gcpServiceApiUrl + '","' + description  + '"'
			if 'resources' in resource:
				traverseResources(resource['resources'])


# Line command CSV file argument
file = sys.argv[1]
with open(file, 'rU') as f:
	jsonURLs = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)
	for jsonURL in jsonURLs:
		gcpServiceApiUrl = jsonURL[0]

		# Load the Google Discovery JSON description for a GCP Service API.
		response = requests.get(url= gcpServiceApiUrl)
		gcpApi = json.loads(response.text)

		gcpServiceTitle = gcpApi['title'] + ' ' + gcpApi['version']
 		gcpServiceBaseUrl = gcpApi['baseUrl']

		resources = gcpApi['resources']
		traverseResources(resources)
