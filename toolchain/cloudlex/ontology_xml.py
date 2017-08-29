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
# CloudLex xml module.
#

from cloudlex import ontology

INDENT = 4

def encode4XML(text):
	text = text.replace('"', '&quot;')
	text = text.replace('&', '&amp;')
	text = text.replace("'", '&apos;')
	text = text.replace('<', '&lt;')
	text = text.replace('>', '&gt;')
	return text

def generateCloudComputing(file, cloudComputing):
	file.write('<CloudComputing>\n')
	for provider in cloudComputing.providers:
		generateProvider(file, provider, INDENT)
	file.write('</CloudComputing>\n')

def generateProvider(file, provider, indent):
	file.write(' '*indent + '<Provider name="' + provider.name + '">\n')
	for service in provider.services:
		generateService(file, service, indent + INDENT)
	file.write(' '*indent + '</Provider>\n')

def generateService(file, service, indent):
	file.write(' '*indent + '<Service name="' + service.name + '">\n')
	for path in service.paths:
		generatePath(file, path, indent + INDENT)
	file.write(' '*indent + '</Service>\n')

def generatePath(file, path, indent):
	if type(path) == ontology.Resource:
		file.write(' '*indent + '<Resource uri="' + path.getFullUri() + '">\n')
		for method in path.methods:
			generateMethod(file, method, indent + INDENT)
		for child in path.paths:
			if type(child) == ontology.Controller:
				generatePath(file, child, indent + INDENT)
		file.write(' '*indent + '</Resource>\n')
		for child in path.paths:
			if type(child) != ontology.Controller:
				generatePath(file, child, indent)	
	if type(path) == ontology.Controller:
		file.write(' '*indent + '<Controller uri="' + path.getFullUri() + '" verb="' + path.verb + '">\n')
		for method in path.methods:
			generateMethod(file, method, indent + INDENT)
		file.write(' '*indent + '</Controller>\n')
	if type(path) == ontology.Query:
		file.write(' '*indent + '<Query uri="' + encode4XML(path.getFullUri()) + '"/>\n')
	if type(path) == ontology.Path:
		for path in path.paths:
			generatePath(file, path, indent)

def generateMethod(file, method, indent):
	description = encode4XML(method.description)
	file.write(' '*indent + '<Method name="' + method.name + '" description="' + description + '"/>\n')

if __name__ == "__main__":
	import sys
	model = ontology.loadDatasets(sys.argv[1:], ontology.DISTINCT_SERVICES)
	generateCloudComputing(sys.stdout, model)
