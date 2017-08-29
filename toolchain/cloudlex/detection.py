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
# CloudLex patterns module.
#

from cloudlex import ontology

# Predicates related to CloudLex Ontology classes.

# TODO: Next predicates could be moved to the ontology module.

def isPath(node):
	return type(node) == ontology.Path

def isResource(node):
	return type(node) == ontology.Resource

def isCollection(node):
	return isResource(node) and not isVariablePath(node) and hasSomeVariablePaths(node)

def isSingleton(node):
	hasOnlyParentNotVariablePaths = True
	if isResource(node):
		parentNode = node.parent
		while parentNode != None:
			if not ( ( isPath(parentNode) or isResource(parentNode)) and not isVariablePath(parentNode)):
				hasOnlyParentNotVariablePaths = False
				break
			parentNode = parentNode.parent
	return isResource(node) and not isVariablePath(node) and not hasSomeVariablePaths(node) and hasOnlyParentNotVariablePaths

def isSubResource(node):
	hasParentWithVariablePath = False
	if isResource(node):
		parentNode = node.parent
		while parentNode != None:
			if isVariablePath(parentNode):
				hasParentWithVariablePath = True
				break
			parentNode = parentNode.parent
	return isResource(node) and not isVariablePath(node) and not hasSomeVariablePaths(node) and hasParentWithVariablePath 

def isController(node):
	return type(node) == ontology.Controller

def isMethod(node):
	return type(node) == ontology.Method

def isVariablePath(node):
	return node.label[:2] == '/{' and node.label[-1] == '}'

def isResourceVariablePath(node):
	return isResource(node) and isVariablePath(node)

def hasNoPath(node):
	return len(node.paths) == 0

def hasSomeVariablePaths(node):
	for path in node.paths:
		if isVariablePath(path):
			return True
	return False

def hasNoController(node):
	for path in node.paths:
		if isController(path):
			return False
	return True

def hasOnlyControllers(node):
	if hasNoPath(node):
		return False
	for path in node.paths:
		if not isController(path):
			return False
	return True

def hasNoMethod(node):
	return len(node.methods) == 0

def hasOnlyOneMethod(node, methodName):
	return len(node.methods) == 1 and node.methods[0].name == methodName

import lexicon

class AbstractPattern(object):
	def __init__(self):
		self.nodes = []

	def name(self):
		return "UNKNOWN"

	def kind(self):
		return "UNKNOWN"

	def visitCloudComputing(self, cloudComputing):
		for provider in cloudComputing.providers:
			for service in provider.services:
				for path in service.paths:
					self.visitPath(path)

	def visitPath(self, path):
		self.executeDetection(path)
		for method in path.methods:
			self.executeDetection(method)
		for p in path.paths:
			self.visitPath(p)

	def executeDetection(self, node):
		if self.detection(node):
			self.nodes.append(node)
			self.detected(node)
	
	def detection(self, node):
		return False

	def display(self):
		print '-' * 80
		print self.name() + ' ' + self.kind() + ' - ' + str(len(self.nodes)) + ' detected:'
		for node in self.nodes:
			if type(node) == ontology.Resource:
				print ' * ' + node.getFullUri()
				continue
			if type(node) == ontology.Controller:
				print ' * ' + node.getFullUri()
				continue
			if type(node) == ontology.Method:
				print ' * ' + node.name + ' ' + node.resourceOrController.getFullUri()
				continue
			print ' * ' + str(node)
		print

class Pattern(AbstractPattern):
	def __init__(self):
		AbstractPattern.__init__(self)

	def kind(self):
		return "Pattern"

	def detected(self, node):
		node.patterns.append(self)
		
class AntiPattern(AbstractPattern):
	def __init__(self):
		AbstractPattern.__init__(self)

	def kind(self):
		return "Anti-Pattern"

	def detected(self, node):
		node.antiPatterns.append(self)
		
class ReadOnlyPattern(Pattern):
	def name(self):
		return "Read-Only"

	def detection(self, node):
		return isResource(node) and hasOnlyOneMethod(node, 'GET') and hasNoController(node)

class ResourcePattern(Pattern):
	def name(self):
		return "Resource"

	def detection(self, node):
		return isResourceVariablePath(node) 

class SingletonResourcePattern(Pattern):
	def name(self):
		return "Singleton Resource"

	def detection(self, node):
		return isSingleton(node)

class SubResourcePattern(Pattern):
	def name(self):
		return "SubResource"

	def detection(self, node):
		return isSubResource(node)

class CollectionPattern(Pattern):
	def name(self):
		return "Collection"

	def detection(self, node):
		return isCollection(node)

class ControllerPattern(Pattern):
	def name(self):
		return "Controller"

	def detection(self, node):
		return isController(node) and lexicon.isVerb(node.verb) and hasNoPath(node) and hasOnlyOneMethod(node, 'POST')

class SingularCollectionAntiPattern(AntiPattern):
	def name(self):
		return "Singular Collection"

	def detection(self, node):
		return isCollection(node) and lexicon.isSingular(node.label[1:])

class MissingPostMethodAntiPattern(AntiPattern):
	def name(self):
		return "Missing POST Method"

	def detection(self, node):
		hasChildWithDeleteMethod = False
		if isResource(node):
			for path in node.paths:
				if path.hasMethod('DELETE'):
					hasChildWithDeleteMethod = True
					break
		return isResource(node) and not isVariablePath(node) and hasSomeVariablePaths(node) and not node.hasMethod('POST') and hasChildWithDeleteMethod

class MissingGetMethodAntiPattern(AntiPattern):
	def name(self):
		return "Missing GET Method"

	def detection(self, node):
		return isResource(node) and not node.hasMethod('GET')

class MissingDeleteMethodAntiPattern(AntiPattern):
	def name(self):
		return "Missing DELETE Method"

	def detection(self, node):
		return isResource(node) and isVariablePath(node) and not node.hasMethod('DELETE') and node.parent.hasMethod('POST') 

class UnexpectedDeleteMethodAntiPattern(AntiPattern):
	def name(self):
		return "Unexpected DELETE Method"

	def detection(self, node):
		return ( isSingleton(node) or isCollection(node) or isSubResource(node) ) and node.hasMethod('DELETE')

class OnlyControllersAntiPattern(AntiPattern):
	def name(self):
		return "Only Controllers"

	def detection(self, node):
		return isResource(node) and hasNoMethod(node) and hasOnlyControllers(node)

class NotVerbControllerAntiPattern(AntiPattern):
	def name(self):
		return "Not Verb Controller"

	def detection(self, node):
		return isController(node) and not lexicon.isVerb(node.verb)

class CreateVerbControllerAntiPattern(AntiPattern):
	def name(self):
		return "Create Verb Controller"

	def detection(self, node):
		return isController(node) and lexicon.isCreateVerb(node.verb) and not node.parent.hasMethod('POST')

class RetrieveVerbControllerAntiPattern(AntiPattern):
	def name(self):
		return "Retrieve Verb Controller"

	def detection(self, node):
		return isController(node) and lexicon.isRetrieveVerb(node.verb) and not node.parent.hasMethod('GET')

class UpdateVerbControllerAntiPattern(AntiPattern):
	def name(self):
		return "Update Verb Controller"

	def detection(self, node):
		return isController(node) and lexicon.isUpdateVerb(node.verb) and not node.parent.hasMethod('POST') and not node.parent.hasMethod('PUT') and not node.parent.hasMethod('PATCH')

class DeleteVerbControllerAntiPattern(AntiPattern):
	def name(self):
		return "Delete Verb Controller"

	def detection(self, node):
		return isController(node) and lexicon.isDeleteVerb(node.verb) and not node.parent.hasMethod('DELETE')

class NotPostMethodControllerAntiPattern(AntiPattern):
	def name(self):
		return "Not POST Method Controller"

	def detection(self, node):
		return isController(node) and not hasOnlyOneMethod(node, 'POST')

class ControllerWithMoreThanOneMethodAntiPattern(AntiPattern):
	def name(self):
		return "More Than One Method"

	def detection(self, node):
		return isController(node) and len(node.methods) > 1

class NotPostControllerMethodAntiPattern(AntiPattern):
	def name(self):
		return "Not POST Controller Method"

	def detection(self, node):
		return isMethod(node) and isController(node.resourceOrController) and node.name != "POST"

class UntaggedResourcesAndControllers(AntiPattern):
	def name(self):
		return "Untagged Resources and Controllers"

	def kind(self):
		return ''

	def detection(self, node):
		return (isResource(node) or isController(node)) and len(node.patterns) == 0 and len(node.antiPatterns) == 0

PATTERNS = [
	ReadOnlyPattern(),
	ResourcePattern(),
	SingletonResourcePattern(),
	SubResourcePattern(),
	CollectionPattern(),
	ControllerPattern()
]

ANTI_PATTERNS = [
	SingularCollectionAntiPattern(),
	MissingPostMethodAntiPattern(),
	MissingGetMethodAntiPattern(),
	MissingDeleteMethodAntiPattern(),
	# TODO: Is it really an anti-pattern?
	UnexpectedDeleteMethodAntiPattern(),
	OnlyControllersAntiPattern(),
	NotVerbControllerAntiPattern(),
	CreateVerbControllerAntiPattern(),
	RetrieveVerbControllerAntiPattern(),
	UpdateVerbControllerAntiPattern(),
	DeleteVerbControllerAntiPattern(),
	NotPostMethodControllerAntiPattern(),
	ControllerWithMoreThanOneMethodAntiPattern(),
	NotPostControllerMethodAntiPattern(),
	UntaggedResourcesAndControllers()
]

def applyOn(model):
	for pattern in PATTERNS:
		pattern.visitCloudComputing(model)
	for antiPattern in ANTI_PATTERNS:
		antiPattern.visitCloudComputing(model)

if __name__ == "__main__":
	import sys
	model = ontology.loadDatasets(sys.argv[1:], ontology.DISTINCT_SERVICES)
	applyOn(model)
	for pattern in PATTERNS:
		pattern.display()
	for antiPattern in ANTI_PATTERNS:
		antiPattern.display()
