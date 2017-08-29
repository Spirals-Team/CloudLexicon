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
# CloudLex lexicon graph module.
#

from cloudlex import ontology
from cloudlex import lexicon

class Context(object):
	def __init__(self, file, lexicon):
		self.file = file
		self.lexicon = lexicon
		self.alreadyDrawnNodes = []
		self.alreadyDrawnArrows = []

	def drawNode(self, node, color, shape):
		nodeLabel = node.term.term
		if nodeLabel not in self.alreadyDrawnNodes:
			self.file.write('"' + nodeLabel + '" [color=' + color + ', fontcolor=' + color + ', shape=' + shape + ']\n')
			self.alreadyDrawnNodes.append(nodeLabel)

	def drawArrow(self, source, targetLabel, color, arrowhead, otherParameters = ''):
		arrowLabel = '"' + targetLabel + '" -> "' + source.term.term + '"'
		if arrowLabel not in self.alreadyDrawnArrows:
			self.file.write(arrowLabel + ' [color=' + color + ', fontcolor=' + color + ', arrowhead=' + arrowhead + ', arrowtail=none' + otherParameters + ']\n')
			self.alreadyDrawnArrows.append(arrowLabel)

def generateRootNode(context, node, parentResource):
	if type(node) == ontology.Resource and not node.label.startswith('/{'):
		context.drawNode(node, 'blue', 'doublecircle')
		return

	for child in node.paths:
		generateRootNode(context, child, parentResource)

def generateNode(context, node, parentResource):
	if type(node) == ontology.Resource and not node.label.startswith('/{'):
		nodeTerm = node.term.term

# TODO see later if it is pertinent to filter technical REST terms.
#		if not lexicon.isTechnicalRestTerm(nodeTerm):

		if parentResource != None:
			context.drawArrow(parentResource, nodeTerm, 'blue', 'diamond')
		context.drawNode(node, 'blue', 'ellipse')
		for term in lexicon.split_term(nodeTerm):
			for targetTerm in [term, lexicon.singularizeTerm(term), lexicon.pluralizeTerm(term)]:
				if nodeTerm != targetTerm and context.lexicon.get(targetTerm):
					context.drawArrow(node, targetTerm, 'grey', 'none', ', style=dashed')

		parentResource = node


	if type(node) == ontology.Controller:
		nodeTerm = node.term.term

		context.drawNode(node, 'orange', 'box')

		if parentResource != None:
			context.drawArrow(parentResource, nodeTerm, 'orange', 'diamond')

		for term in lexicon.split_term(nodeTerm):
			for targetTerm in [term, lexicon.singularizeTerm(term), lexicon.pluralizeTerm(term)]:
				if nodeTerm != targetTerm and context.lexicon.get(targetTerm):
					context.drawArrow(node, targetTerm, 'grey', 'none', ', style=dashed')
			for antonym in lexicon.antonyms(term):
				for a in [antonym, antonym.title()]:
					antonymNodeTerm = nodeTerm.replace(term, a)
					if context.lexicon.get(antonymNodeTerm):
						context.drawArrow(node, antonymNodeTerm, 'red', 'none')

	for child in node.paths:
		generateNode(context, child, parentResource)

def generateForEachService(folder, cloudComputing):
	for provider in cloudComputing.providers:
		for service in provider.services:
			serviceName = service.name.replace('/', ' ')
			print 'Generating ' + folder + '/' + serviceName + '.dot...'
			with open(folder + '/' + serviceName + '.dot', 'w') as file:
				file.write('digraph LexiconGraph {\n')
				file.write('graph[label="' + provider.name + ' - ' + service.name + '", fontsize=24]\n')
				file.write('splines=true\n')
				context = Context(file, service.lexiconOfNounsVerbs)
				for node in service.paths:
					generateRootNode(context, node, None)
				for node in service.paths:
					generateNode(context, node, None)
				file.write('}\n')
				file.close()

def generateAllInOne(folder, cloudComputing):
	print 'Generating ' + folder + '/AllInOne.dot...'
	with open(folder + '/AllInOne.dot', 'w') as file:
		file.write('digraph AllInOne_LexiconGraph {\n')
		file.write('graph[label="' + cloudComputing.providers[0].name + '", fontsize=24]\n')
		file.write('splines=true\n')
		for provider in cloudComputing.providers:
			for service in provider.services:
				context = Context(file, cloudComputing.lexiconOfNounsVerbs)
				for node in service.paths:
					generateRootNode(context, node, None)
				for node in service.paths:
					generateNode(context, node, None)
		file.write('}\n')
		file.close()

if __name__ == "__main__":
	import sys
	model = ontology.loadDatasets(sys.argv[2:], ontology.DISTINCT_SERVICES, ontology.ONE_LEXICON_BY_SERVICE)
	generateForEachService(sys.argv[1], model)
	model = ontology.loadDatasets(sys.argv[2:], ontology.ALL_IN_ONE_SERVICE)
	generateAllInOne(sys.argv[1], model)


