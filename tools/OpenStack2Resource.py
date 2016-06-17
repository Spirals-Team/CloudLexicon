import csv
import sys
import requests
import json

#Line command CSV file argument
file = sys.argv[1]

with open(file, 'rU') as f:
	provider = 'OpenStack'
	jsonURLs = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)

	for jsonURL in jsonURLs:
		resp = requests.get(url=jsonURL[0])
		openstack = json.loads(resp.text)

		for element in openstack:
			service = openstack['info']['title'].encode('ascii')

			for uri in openstack['paths']:
				reference = jsonURL[0]
				tokens = uri.split('/',100)

				for token in tokens:
					if token == '' or token == ',' or token[0] == '{' or token.isdigit():
						continue
					if token.find('v1') > -1 or token.find('v2') > -1 or token.find('v1') > -1:
						continue
					if token != 'action':
						#Resource
						for httpMethod in openstack['paths'][uri]:
							if httpMethod != 'parameters':
								print provider + ',' + service + ',' + 'RESOURCE' + ',' + token + ',' + httpMethod.upper() +  ',' + uri + ',' + reference
					else:
						#Action
						for httpMethod in openstack['paths'][uri]:
							if httpMethod != 'parameters':
								print provider + ',' + service + ',' + 'ACTION' + ',' + openstack['paths'][uri][httpMethod]['operationId'] + ',' + httpMethod.upper() + ',' +  uri + ',' + reference
