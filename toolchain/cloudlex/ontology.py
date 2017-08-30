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
# CloudLex ontology module.
#

class CloudComputing(object):
	def __init__(self):
		self.providers = []

	def addProvider(self, name):
		for provider in self.providers:
			if provider.name == name:
				return provider
		provider = Provider(name)
		self.providers.append(provider)
		return provider

class Provider(object):
	def __init__(self, name):
		self.name = name
		self.services = []

	def addService(self, name):
		for service in self.services:
			if service.name == name:
				return service
		service = Service(name)
		self.services.append(service)
		return service

class Service(object):
	def __init__(self, name):
		self.name = name
		self.paths = []

	def addPath(self, label, term):
		for path in self.paths:
			if path.label == label:
				return path
		path = Path(label, term)
		self.paths.append(path)
		return path

class Object4Detection(object):
	def __init__(self):
		self.patterns = []
		self.antiPatterns = []

class Path(Object4Detection):
	def __init__(self, label, term, parent = None):
		Object4Detection.__init__(self)
		self.label = label
		self.term = term
		self.parent = parent
		self.paths = []
		self.methods = []

	def getFullUri(self):
		if self.parent == None:
			return self.label
		return self.parent.getFullUri() + self.label

	def hasMethod(self, methodName):
		for method in self.methods:
			if method.name == methodName:
				return True
		return False

	def hasPath(self, label):
		for path in self.paths:
			if path.label == label:
				return True
		return False

	def addPath(self, label, term, kind):
		for path in self.paths:
			if path.label == label:
				return path
		
		# If self is a path and the kind is a controller then mutate it to a resource.
		if (self.__class__ == Path or self.__class__ == Controller) and kind == Controller:
			self.__class__ = Resource
		
		path = kind(label, term, self)
		self.paths.append(path)
		return path

	def addMethod(self, name, description):		
		for method in self.methods:
			if method.name == name:
				return method
		
		# If self is a path then mutate it to a resource.
		if self.__class__ == Path:
			self.__class__ = Resource
		
		method = Method(name, description, self)
		self.methods.append(method)
		return method

class Resource(Path):
	def __init__(self, label, term, parent):
		Path.__init__(self, label, term, parent)

class Controller(Path):
	def __init__(self, label, term, parent):
		Path.__init__(self, label, term, parent)

class Query(Path):
	def __init__(self, label, term, parent):
		Path.__init__(self, label, term, parent)

class Method(Object4Detection):
	def __init__(self, name, description, resourceOrController):
		Object4Detection.__init__(self)
		self.name = name
		self.description = description
		self.resourceOrController = resourceOrController

ALL_IN_ONE_SERVICE = "ALL_IN_ONE_SERVICE"
DISTINCT_SERVICES = "DISTINCT_SERVICES"
ONE_GLOBAL_LEXICON = "ONE_GLOBAL_LEXICON"
ONE_LEXICON_BY_SERVICE = "ONE_LEXICON_BY_SERVICE"

#
# Load URIs datasets.
#
def loadDatasets(fileNames, serviceStrategy = DISTINCT_SERVICES, lexiconStrategy = ONE_GLOBAL_LEXICON):
	import csv
	from cloudlex import lexicon

	assert serviceStrategy == ALL_IN_ONE_SERVICE or serviceStrategy == DISTINCT_SERVICES
	assert lexiconStrategy == ONE_GLOBAL_LEXICON or lexiconStrategy == ONE_LEXICON_BY_SERVICE

	model = CloudComputing()

	model.trashLexicon = lexicon.Lexicon()

	if lexiconStrategy == ONE_GLOBAL_LEXICON:
		currentLexicon = lexicon.Lexicon()
		model.lexiconOfNounsVerbs = currentLexicon
	else:
		currentLexicon = None

	def newTerm(term):
		if term[0] == '{' or '}' in term or lexicon.isVersion(term):
			return model.trashLexicon.newTerm(term)
		result = currentLexicon.newTerm(term)
		result.providers.add(currentProviderName)
		return result

	currentProviderName = ''

	for fileName in fileNames:
		with open(fileName, 'rU') as f:
			freader = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_ALL)
			for row in freader:
				currentProviderName = row[0]
				provider = model.addProvider(currentProviderName)

				if serviceStrategy == ALL_IN_ONE_SERVICE:
					serviceName = 'AllInOne'
				else:
					serviceName = row[1]

				service = provider.addService(serviceName)

				if lexiconStrategy == ONE_LEXICON_BY_SERVICE:
					try:
						currentLexicon = service.lexiconOfNounsVerbs
					except AttributeError:
						currentLexicon = lexicon.Lexicon()
						service.lexiconOfNounsVerbs = currentLexicon

				node = service

				uri = row[2]
				# deal with URI starting by http[s]://
				if uri.startswith("http"):
					node = node.addPath(uri[0:uri.index('/',8)], model.trashLexicon.newTerm(currentProviderName))
					uri = uri[uri.index('/',8)+1:]

				tokens = uri.split('/')
				for token in tokens[0:len(tokens)-1]:
					node = node.addPath('/' + token, newTerm(token), Path)
				token = tokens[-1]

#
# TODO: Following code must be factorized and perhaps moved into extractors.
#

				# OCCI controllers are stored in the URI query part.
				if currentProviderName == "OCCI" and '?' in token:
					tmp = token.split('?')
					verb = tmp[1].split('=',1)[1]
					if tmp[0] != "":
						node = node.addPath('/' + tmp[0], newTerm(tmp[0]), Resource)
						node = node.addPath('?' + tmp[1], newTerm(verb), Controller)
					else:
						node = node.addPath('/?' + tmp[1], newTerm(verb), Controller)
					node.verb = verb
				else:
					# GCP controllers are preceded by a ':'
					if currentProviderName == "Google Cloud Platform" and ':' in token:
						tmp = token.split(':')
						if tmp[0] != "":
							node = node.addPath('/' + tmp[0], newTerm(tmp[0]), Resource)
						node = node.addPath(':' + tmp[1], newTerm(tmp[1]), Controller)
						node.verb = tmp[1]
					else:
						if currentProviderName == "DigitalOcean": # TODO: Could be merged with the last general case?
							if token.startswith('actions|type='):
								verb = token[len('actions|type='):]
								node = node.addPath('?' + token, newTerm(verb), Controller)
								node.verb = verb
							else:
								if '?' in token:
									tmp = token.split('?')
									node = node.addPath('/' + tmp[0], newTerm(tmp[0]), Resource)
									node = node.addPath('?' + tmp[1], model.trashLexicon.newTerm(tmp[1]), Query)
								else:
									node = node.addPath('/' + token, newTerm(token), Resource)
									
						else:
							if currentProviderName == "Apache CloudStack":
								if token.startswith('api?command='):
									node = node.addPath('/api', newTerm('api'), Resource)
									verb = token[len('api?command='):token.find('&amp;')]
									node = node.addPath(token, newTerm(verb), Controller)
									node.verb = verb
							else:

								if currentProviderName == "OpenStack": # TODO: Could be merged with the next general case?
									if '|' in token:
										verb = token[token.find('|')+1:]
										node = node.addPath('?' + token, newTerm(verb), Controller)
										node.verb = verb
									else:
										if token != "":
											if lexicon.isVerb(token):
												verb = token.split('?')[0]
												node = node.addPath('/' + token, newTerm(verb), Controller)
												node.verb = token
											else:
												node = node.addPath('/' + token, newTerm(token), Resource)
								else:
									if token != "":
										if '|' in token:
											verb = token[token.find('|')+1:]
											node = node.addPath('?' + token, newTerm(verb), Controller)
											node.verb = verb
										else:
											if lexicon.isVerb(token):
												verb = token.split('?')[0]
												node = node.addPath('/' + token, newTerm(verb), Controller)
												node.verb = token
											else:
												if '?' in token:
													tmp = token.split('?')
													node = node.addPath('/' + tmp[0], newTerm(tmp[0]), Resource)
													node = node.addPath('?' + tmp[1], model.trashLexicon.newTerm(tmp[1]), Query)
												else:
													node = node.addPath('/' + token, newTerm(token), Resource)

				httpMethod = row[3]
				if node.hasMethod(httpMethod):
					import sys
					sys.stderr.write('WARNING - ' + httpMethod + ' ' + row[2] + ' already present in the ontology!!!\n')
				node.addMethod(httpMethod, row[5])
	return model


if __name__ == "__main__":
	import sys
	model = loadDatasets(sys.argv[1:], DISTINCT_SERVICES)
