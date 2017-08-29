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
# This script generates the URIs Dataset for Apache CloudStack.
#

# from cloudlet import lexicon

import requests

PROVIDER_NAME = 'Apache CloudStack'
DOCUMENTATION_URL = 'http://cloudstack.apache.org/api/apidocs-4.9/apis/'
SERVICE_NAME = 'API 4.9'
PROVIDER_BASE_URL = 'https://cloudstack.provider.com:[port]/client/api'

MARKER1='<tr><td valign="top"><img src="/icons/text.gif" alt="[TXT]"></td><td><a href="'
MARKER1_LEN=len(MARKER1)
MARKER2='<h1>'
MARKER2_LEN=len(MARKER2)
MARKER3='</h1>'
MARKER4='<p>'
MARKER4_LEN=len(MARKER4)
MARKER5='</p>'

# Load Apache CloudStack HTML documentation.
response1 = requests.get(url= DOCUMENTATION_URL)
for line1 in response1.iter_lines():
	if line1.startswith(MARKER1):
		commandFile = line1[MARKER1_LEN: line1.find('">', MARKER1_LEN)]
		documentationUrl = DOCUMENTATION_URL + commandFile
		response2 = requests.get(url= DOCUMENTATION_URL + commandFile)
		commandName = ''
		for line2 in response2.iter_lines():
			if line2.startswith(MARKER2):
				commandName = line2[MARKER2_LEN:line2.find(MARKER3, MARKER2_LEN)]
			if line2.startswith(MARKER4) and commandName != '':
				description = line2[MARKER4_LEN:line2.find(MARKER5, MARKER4_LEN)]

				# Apache CloudStack URI format is described at http://docs.cloudstack.apache.org/en/latest/dev.html
				uri = PROVIDER_BASE_URL + '?command=' + commandName + '&amp;[parameters of this command]'

#				if lexicon.isVerb(commandName):
				method = 'POST'
#				else
#					method = 'GET'

				print '"' + PROVIDER_NAME + '","' + SERVICE_NAME + '","' + uri + '","POST","' + documentationUrl + '","' + description + '"'

				break # Go to next API command.
