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
# CloudLex dot module.
#

from cloudlex import ontology

NODE_COLORS = {
	ontology.CloudComputing: "black",
	ontology.Provider: "black",
	ontology.Service: "violet",
	ontology.Path: "black",
	ontology.Resource: "blue",
	ontology.Controller: "orange",
	ontology.Query: "blue",
	ontology.Method: "green"
}

ARROW_COLORS = {
	ontology.CloudComputing: "black",
	ontology.Provider: "black",
	ontology.Service: "violet",
	ontology.Path: "black",
	ontology.Resource: "blue",
	ontology.Controller: "orange",
	ontology.Query: "blue",
	ontology.Method: "green"
}

NODE_SHAPES = {
	ontology.CloudComputing: "none",
	ontology.Provider: "none",
	ontology.Service: "none",
	ontology.Path: "ellipse",
	ontology.Resource: "ellipse",
	ontology.Controller: "octagon",
	ontology.Query: "ellipse",
	ontology.Method: "box"
}

def getPatterns(node):
	result = ''
	if len(node.patterns) > 0:
		result = '\\n'
		for pattern in node.patterns:
			result = result + ' ' + pattern.name()
	if len(node.antiPatterns) > 0:
		result = result + '\\nbut'
		for antiPattern in node.antiPatterns:
			result = result + '\\n' + antiPattern.name()
	return result

def generateCloudComputing(file, cloudComputing):
	file.write('digraph Cloud_Computing_REST_APIs {\n')
	file.write('rankdir="LR";\n')
	number = 0
	for provider in cloudComputing.providers:
		number = generateProvider(file, provider, number)
	file.write('}\n')

def generateProvider(file, provider, number):
	file.write('subgraph cluster_' + str(number) + ' {\n')
	file.write('label="' + provider.name + '"\n')
	color = NODE_COLORS[type(provider)]
	file.write('color=' + color + '\n')
	file.write('fontcolor=' + color + '\n')
	for service in provider.services:
		number = generateService(file, service, number + 1)
	file.write('}\n')
	return number

def generateService(file, service, number, labelPrefix = ''):
	file.write('subgraph cluster_' + str(number) + ' {\n')
	file.write('label="' + labelPrefix + service.name + '"\n')
	color = NODE_COLORS[type(service)]
	file.write('color=' + color + '\n')
	file.write('fontcolor=' + color + '\n')
	for path in service.paths:
		number = generatePath(file, path, number + 1)
	file.write('}\n')
	return number

def generatePath(file, path, number):
	file.write('subgraph cluster_' + str(number) + ' {\n')
	file.write('label=""\n')
	file.write('color=white\n')
	file.write('fontcolor=white\n')
	if len(path.antiPatterns) > 0:
		color = 'red'
	else:
		color = NODE_COLORS[type(path)]
	file.write('node' + str(number) + ' [label="' + path.label + getPatterns(path) + '", shape="' + NODE_SHAPES[type(path)] + '", color="' + color + '", fontcolor="' + color + '"]\n')
	parentNumber = number
	for method in path.methods:
		color = ARROW_COLORS[type(method)]
		file.write("node" + str(parentNumber) + " -> node" + str(number + 1) + " [color=\"" + color + "\", fontcolor=\"" + color + '\"]\n')
		number = generateMethod(file, method, number + 1)
	for child in path.paths:
		color = ARROW_COLORS[type(child)]
		file.write("node" + str(parentNumber) + " -> node" + str(number + 1) + " [color=\"" + color + "\", fontcolor=\"" + color + '\"]\n')
		number = generatePath(file, child, number + 1)
	file.write('}\n')
	return number

def generateMethod(file, method, number):
	file.write('subgraph cluster_' + str(number) + ' {\n')
	file.write('label=\"\"\n')
	file.write('color=white\n')
	file.write('fontcolor=white\n')
	if len(method.antiPatterns) > 0:
		color = 'red'
	else:
		color = NODE_COLORS[type(method)]
	file.write('node' + str(number) + ' [label="' + method.name + getPatterns(method) + '", shape="' + NODE_SHAPES[type(method)] + '", color="' + color + '", fontcolor="' + color + '"]\n')
	file.write('}\n')
	return number

def generateForEachService(folder, cloudComputing):
	for provider in cloudComputing.providers:
		for service in provider.services:
			serviceName = service.name.replace('/', ' ')
			print 'Generating ' + folder + '/' + serviceName + '.dot...'
			with open(folder + '/' + serviceName + '.dot', 'w') as file:
				file.write('digraph Cloud_Computing_REST_API {\n')
				file.write('rankdir="LR";\n')
				generateService(file, service, 0, provider.name + ' - ')
				file.write('}\n')
				file.close()

def generateAllInOne(folder, cloudComputing):
	print 'Generating ' + folder + '/AllInOne.dot...'
	with open(folder + '/AllInOne.dot', 'w') as file:
		generateCloudComputing(file, cloudComputing)
		file.close()

if __name__ == "__main__":
	import sys
	model = ontology.loadDatasets(sys.argv[2:], ontology.DISTINCT_SERVICES)
	generateForEachService(sys.argv[1], model)
	model = ontology.loadDatasets(sys.argv[2:], ontology.ALL_IN_ONE_SERVICE)
	generateAllInOne(sys.argv[1], model)
