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
# CloudLex extraction module.
# 

import csv
# To install the requests module, execute:
# - pip install requests OR easy_install requests
import requests
import json
import yaml
import sys

RACKERLABS_URL = 'http://rackerlabs.github.io/wadl2swagger/'

def extractCsvFileOfSwaggerJsonURIsFromRackerlabs(providerName):
	response = requests.get(url=RACKERLABS_URL + providerName + '.html')
	for line in response.iter_lines():
		if '.json</a>' in line:
			print RACKERLABS_URL + line[line.find('">')+2:line.find('</a>')]

def applyMappingRules(text, mappingRules):
	for mappingRule in mappingRules:
		text = text.replace(mappingRule[0], mappingRule[1])
	return text

CSV_MAPPING_RULES = [
	['\n', '\\n'],
	['"', '""']
]

def extractDatasetURIsFromCsvFileOfSwaggerJsonURIs(csvFilename, providerName, defaultProviderBaseUrl, uriMappingRules = []):
	with open(csvFilename, 'rU') as csvFile:
		jsonURIs = csv.reader(csvFile, delimiter = ',', quoting=csv.QUOTE_NONE)
		for jsonURI in jsonURIs:
			if len(jsonURI) == 0: continue # this CVS line is empty.
			documentationURI = jsonURI[0]
			if not documentationURI.startswith('#'):
				extractDatasetURIsFromOneSwaggerJson(documentationURI, providerName, defaultProviderBaseUrl, uriMappingRules)

def extractDatasetURIsFromCsvFileOfSwaggerURIs(csvFilename, providerName, defaultProviderBaseUrl, uriMappingRules = []):
	with open(csvFilename, 'rU') as csvFile:
		jsonURIs = csv.reader(csvFile, delimiter = ',', quoting=csv.QUOTE_NONE)
		for jsonURI in jsonURIs:
			if len(jsonURI) == 0: continue # this CVS line is empty.
			documentationURI = jsonURI[0]
			if not documentationURI.startswith('#'):
				if documentationURI.endswith('.yml'):
					extractDatasetURIsFromOneSwaggerYaml(documentationURI, providerName, defaultProviderBaseUrl, uriMappingRules)
				else:
					extractDatasetURIsFromOneSwaggerJson(documentationURI, providerName, defaultProviderBaseUrl, uriMappingRules)


def extractDatasetURIsFromOneSwaggerJson(jsonURI, providerName, defaultProviderBaseUrl, uriMappingRules = []):
	response = requests.get(url= jsonURI)
	try:
		swaggerJson = json.loads(response.text)
	except:
		sys.stderr.write('Exception in json.loads(): ' + jsonURI + ' may contain an invalid JSON object!\n')
		return

	serviceName = swaggerJson['info']['title'].encode('utf8')
	if 'version' in swaggerJson['info']:
		version = swaggerJson['info']['version']
		if version:
			# Some OpenStack/Rackspace Swagger JSON files have Unknown as version
			if ( providerName == "OpenStack" or providerName == "Rackspace" ) and version == 'Unknown':
				pass # Do nothing
			else:
				serviceName += ' ' + version.encode('utf8')

	try:
		providerBaseUrl = swaggerJson['schemes'][0] + '://' + swaggerJson['host']
	except:
		providerBaseUrl = defaultProviderBaseUrl

	paths = swaggerJson['paths']
	for uri in paths:
		theBaseURI = applyMappingRules(uri, uriMappingRules)
		for httpMethod in paths[uri]:
			theURI = theBaseURI
			theHttpMethod = httpMethod.upper()
			if theHttpMethod != 'PARAMETERS':
				tmp = paths[uri][httpMethod]
				if 'description' in tmp:
					# TODO: encode('utf8') does not correct this exception issue in the next print instruction!!!
					description = tmp['description'].encode('utf8')
					# Do CSV encoding.
					description = applyMappingRules(description, CSV_MAPPING_RULES)
				else:
					description = ''

				# WARNING OpenStack and Rackspace !!!!
				if ( providerName == "OpenStack" or providerName == "Rackspace" ) and uri.endswith('/action'):
					theURI += '|' + paths[uri][httpMethod]['operationId']

				# WARNING Oracle Cloud API documents GET actions which are not supported !!!!
				if description.endswith(" action not supported"):
					continue

				try:
					print '"' + providerName + '","' + serviceName + '","' + providerBaseUrl + theURI + '","' + theHttpMethod + '","' + jsonURI + '","' + description +'"'
				except:
					sys.stderr.write('Exception in print for ' + jsonURI + ' uri=' + theURI + '\n')
					print '"' + providerName + '","' + serviceName + '","' + providerBaseUrl + theURI + '","' + theHttpMethod + '","' + jsonURI + '","' + 'WARNING this description can not be encoded by Python!!!' +'"'
					continue

# TODO: Need to factorize the following code as it is exactly the same than previous code (copy/paste).
def extractDatasetURIsFromOneSwaggerYaml(yamlURI, providerName, defaultProviderBaseUrl, uriMappingRules = []):
	response = requests.get(url= yamlURI)
	swaggerYaml = yaml.load(response.text)

	try:
		serviceName = swaggerYaml['info']['title'].encode('utf8')
	except:
		serviceName = "UNKNOWN"
	if 'version' in swaggerYaml['info']:
		info = swaggerYaml['info']['version']
		if info:
			serviceName += ' ' + info.encode('utf8')

	try:
		providerBaseUrl = swaggerYaml['schemes'][0] + '://' + swaggerYaml['host']
	except:
		providerBaseUrl = defaultProviderBaseUrl

	paths = swaggerYaml['paths']
	for uri in paths:
		theURI = applyMappingRules(uri, uriMappingRules)
		for httpMethod in paths[uri]:
			theHttpMethod = httpMethod.upper()
			if theHttpMethod != 'PARAMETERS':
				tmp = paths[uri][httpMethod]
				if 'description' in tmp:
					# TODO: encode('utf8') does not correct this exception issue in the next print instruction!!!
					description = tmp['description'].encode('utf8')
					# Do CSV encoding.
					description = applyMappingRules(description, CSV_MAPPING_RULES)
				else:
					description = ''

				# WARNING Oracle Cloud API documents GET actions which are not supported !!!!
				if description.endswith(" action not supported"):
					continue

				try:
					print '"' + providerName + '","' + serviceName + '","' + providerBaseUrl + theURI + '","' + theHttpMethod + '","' + yamlURI + '","' + description +'"'
				except:
					sys.stderr.write('Exception in print for ' + documentationURI + ' uri=' + theURI + '\n')
					print '"' + providerName + '","' + serviceName + '","' + providerBaseUrl + theURI + '","' + theHttpMethod + '","' + yamlURI + '","' + 'WARNING this description can not be encoded by Python!!!' +'"'
					continue
