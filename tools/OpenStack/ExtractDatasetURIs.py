#
# This script generates the URI dataset for OpenStack.
# 

import csv
import sys
import requests
import json

# Line command CSV file argument
file = sys.argv[1]
with open(file, 'rU') as f:
	provider = 'OpenStack'
	jsonURLs = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)
	for jsonURL in jsonURLs:
		reference = jsonURL[0]
		resp = requests.get(url=reference)
		openstack = json.loads(resp.text)
		service = openstack['info']['title'].encode('ascii')
		for uri in openstack['paths']:
			for httpMethod in openstack['paths'][uri]:
				if httpMethod != 'parameters':
					print provider + ',' + service + ',' + uri + ',' + httpMethod.upper() + ',' + reference
