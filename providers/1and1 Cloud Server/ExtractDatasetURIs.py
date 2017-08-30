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
# - Fabio Petrillo
# - Philippe Merle <philippe.merle@inria.fr>
#
################################################################################

#
# This script generates the CloudLex REST API Dataset for 1&1 Cloud Server.
#

import requests
import re
# This script uses BeautifulSoup library.
# To download: >Path\Python36-32\Scripts\easy_install.exe beautifulsoup4
# TODO: document this requirements in README.md
from bs4 import BeautifulSoup


# 1&1 Cloud Server API v1 - Documentation
# Main source: https://cloudpanel-api.1and1.com/documentation/v1/en/documentation.html#

PROVIDER = '1&1 Cloud Server'
SERVICE = 'API v1'
REFERENCE = 'https://cloudpanel-api.1and1.com/documentation/v1/en/documentation.html'
BASE_URL = 'https://cloudpanel-api.1and1.com/v1'

response = requests.get(url=REFERENCE).content
soup = BeautifulSoup(response, "html.parser")
for i in soup.find_all("div", { "class" : "panel panel-default" }):
	for j in i.find_all("div",{"class":"panel panel-white"}):
		uri = str(j.find("a",{"class":"collapsed"}))
		uri = uri[uri.find('<span class="parent">')+21:uri.find('</a>')]
		uri = uri.replace('</span>','')
		for k in j.find_all("div", { "class" : "list-group-item" }):
			name = {'class': re.compile('.*badge.*')}

			method = str(k.find_all(**name))
			method = method.replace('[<span class="badge badge_get">','')
			method = method.replace('[<span class="badge badge_post">', '')
			method = method.replace('[<span class="badge badge_delete">', '')
			method = method.replace('[<span class="badge badge_put">', '')
			method = method.replace('</span>]', '')
			method = method.upper()
            
			description = str(k.find_all("div", { "class" : "method_description" }))
			description = description.replace('[<div class="method_description"><p>','')
			description = description.replace('</p></div>]', '')

			# There is a special case for the uri '.../status/action'
			# TODO: Could be implemented by introspecting more the documentation page.
			if uri.endswith('/status/action'):
				for action in [ 'POWER_ON', 'POWER_OFF' ]:
					print '"' + PROVIDER + '","' + SERVICE + '","' + BASE_URL + uri + '|' + action + '","' + method + '","' + REFERENCE + '","' + description + '"'
			else:
				print '"' + PROVIDER + '","' + SERVICE + '","' + BASE_URL + uri + '","' + method + '","' + REFERENCE + '","' + description + '"'
