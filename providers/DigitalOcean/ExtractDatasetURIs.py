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
# This script generates the URIs Dataset for DigitalOcean.
#

import requests

providerName = 'DigitalOcean'
digitalOceanApiDocumentationUrl = 'https://developers.digitalocean.com/documentation/v2'
serviceTitle = 'API v2'
providerBaseUrl = 'https://api.digitalocean.com'

def changeVariableParts(uri):
	dollarPos = uri.find('$')
	if dollarPos != -1:
		slashPos = uri.find('/',dollarPos)
		if slashPos != -1:
			uri = uri[:dollarPos] + '{' + uri[dollarPos+1:slashPos].lower() + '}' + uri[slashPos:]
			uri = changeVariableParts(uri)
		else:
			uri = uri[:dollarPos] + '{' + uri[dollarPos+1:].lower() + '}'
	return uri


# These DigitalOcean operations are not documented as all other operations !!!
# So we add them manually into the DigitalOcean Dataset URIs :-)
print '"' + providerName + '","' + serviceTitle + '","' + providerBaseUrl + '/v2/account' + '","' + 'GET' + '","' + digitalOceanApiDocumentationUrl + '","' + 'Get User Information' + '"'
for actionName in ['power_cycle', 'power_on', 'power_off', 'shutdown', 'enable_private_networking', 'enable_ipv6', 'enable_backups', 'disable_backups', 'snapshot']:
	print '"' + providerName + '","' + serviceTitle + '","' + providerBaseUrl + '/v2/droplets/actions|type=' + actionName + '","' + 'POST' + '","' + digitalOceanApiDocumentationUrl + '","' + 'Acting ' + actionName +' on Tagged Droplets' + '"'

# Load DigitalOcean HTML documentation.
response = requests.get(url= digitalOceanApiDocumentationUrl)
for line in response.iter_lines():
	if '<h3>' in line and '</h3>' in line:
		lastTitle = line[line.find('<h3>')+4:line.find('</h3>')]

	if ' request ' in line and '<code>' in line and '</code>' in line:
		tmp = line[:line.find(' request ')]
		method = tmp[tmp.rfind(' ')+1:]
		if method != 'your':
			uri = line[line.find('<code>')+6:line.find('</code>')]
			if uri.startswith('/v2/'):
				pos = uri.find('?')
				if pos != -1:
					uri = changeVariableParts(uri[:pos]) + uri[pos:].replace('&amp;', '&')
				else:
					uri = changeVariableParts(uri)
				if uri.endswith('/actions'):
					TYPE = 'the "type" attribute to '
					typePos = line.find(TYPE)
					if typePos != -1:
						uri += '|type='
						tmp = line[typePos+len(TYPE):]
						if tmp.startswith('<code>'):
							uri += tmp[6:tmp.find('</code>')]
						if tmp.startswith('"'):
							uri += tmp[1:tmp.find('"', 1)]
					else:
						if uri == "/v2/volumes/actions":
							uri += '|type=attach'
				uri = uri.replace('/keys/{ssh_key_id}', '/keys/{key_id}')
				uri = uri.replace('/floating_ips/{floating_ip}', '/floating_ips/{floating_ip_addr}')
				print '"' + providerName + '","' + serviceTitle + '","' + providerBaseUrl + uri + '","' + method + '","' + digitalOceanApiDocumentationUrl + '","' + lastTitle + '"'

	if 'query paramter set' in line and '<code>' in line and '</code>.' in line:
		method = "GET"
		uri = line[line.find('<code>/v2/')+6:line.find('</code>.')]
		print '"' + providerName + '","' + serviceTitle + '","' + providerBaseUrl + uri + '","' + method + '","' + digitalOceanApiDocumentationUrl + '","' + lastTitle + '"'


