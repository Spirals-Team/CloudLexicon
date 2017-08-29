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
# CloudLex stats module.
#

from cloudlex import ontology

def purcent(x, y):
	return "{:.2%}".format(float(x)/y) 

def formatNumber(x, y):
	return str(x) + ' (' + purcent(x, y) + ')'

class Statistics(object):
	def __init__(self):
		self.numberOfProviders = 0
		self.numberOfServices = 0
		self.numberOfResources = 0
		self.numberOfControllers = 0
		self.numberOfQueries = 0
		self.numberOfMethods = 0
		self.numberByMethod = {}

	def visit(self, cloudComputing):
		self.numberOfProviders = len(cloudComputing.providers)
		for provider in cloudComputing.providers:
			for service in provider.services:
				self.numberOfServices = self.numberOfServices + 1
				for path in service.paths:
					self.visitPath(path)

		print
		print '-'*20 + ' API ' + '-'*20
		print 

		print "Number of providers = " + str(self.numberOfProviders)
		print "Number of services = " + str(self.numberOfServices)
		print "Number of resources = " + str(self.numberOfResources)
		print "Number of controllers = " + str(self.numberOfControllers)
		print "Number of queries = " + str(self.numberOfQueries)
		print "Number of methods = " + str(self.numberOfMethods)
		for method in self.numberByMethod:
			print " - " + str(self.numberByMethod[method]) + " " + method + " (" + purcent(self.numberByMethod[method],self.numberOfMethods) + ")"

		print
		print '-'*20 + ' LEXICON ' + '-'*20
		print 


		lexicon = cloudComputing.lexiconOfNounsVerbs

		commonTerms = []
		for index in range(len(cloudComputing.providers) + 1):
			commonTerms.append([])

		for key in lexicon:
			term = lexicon[key]
			index = len(term.providers)
			commonTerms[index].append(term)

		for index in range(3):
			print '*'*80

		for index in range(len(commonTerms)):
			print '*'*30 + ' '*5 + str(len(commonTerms[index])) + ' terms are common to ' + str(index) + ' of ' + str(len(cloudComputing.providers)) + ' providers ' + ' '*5 + '*'*30
			if index > 2:
				for term in commonTerms[index]:
					print term
		print
	
		numberTerms = len(lexicon)
		print "Number of terms = " + str(numberTerms)
		print "Number of nouns = "  + formatNumber(lexicon.nounsCounter, numberTerms)
		print "Number of verbs = " + formatNumber(lexicon.verbsCounter, numberTerms)
		print "Number of singular terms = " + formatNumber(lexicon.singularCounter, numberTerms)
		print "Number of plural terms = " + formatNumber(lexicon.pluralCounter, numberTerms)
		print "Number of lower case terms = " + formatNumber(lexicon.lowerCaseCounter, numberTerms)
		print "Number of upper case terms = " + formatNumber(lexicon.upperCaseCounter, numberTerms)
		print "Number of camel case terms = " + formatNumber(lexicon.camelCaseCounter, numberTerms)
		print "Number of hyphen terms = " + formatNumber(lexicon.hyphenCounter, numberTerms)
		print "Number of underscore terms = " + formatNumber(lexicon.underscoreCounter, numberTerms)
		print "Number of business terms = " + formatNumber(lexicon.businessTermCounter, numberTerms)
		print "Number of engineering terms = " + formatNumber(lexicon.engineeringTermCounter, numberTerms)
		print 

		assert numberTerms == lexicon.nounsCounter + lexicon.verbsCounter
		assert numberTerms == lexicon.singularCounter + lexicon.pluralCounter
		assert numberTerms == lexicon.lowerCaseCounter + lexicon.upperCaseCounter + lexicon.camelCaseCounter
		assert numberTerms == lexicon.businessTermCounter + lexicon.engineeringTermCounter

		if len(cloudComputing.providers) == 1:
			print
			print '-'*20 + ' QUALITY ' + '-'*20
			print 

			providerName = cloudComputing.providers[0].name

			score = 0.0

			#
			# Scoring API structure quality
			#
			if self.numberOfControllers < 10:
				print providerName + " is CRUD :-) because few controllers (" + str(self.numberOfControllers) + ")"
			else:
				if self.numberOfResources < 5:
					print providerName + " is RPC :-) because few resources (" + str(self.numberOfResources) + ")"
				else:
					print providerName + " is REST ;-)"

			scoreRest = float( self.numberOfMethods - self.numberOfControllers ) / self.numberOfMethods
			print "scoreRest = " + str(scoreRest)

			#
			# Scoring API naming quality
			#
			if ( lexicon.hyphenCounter > 0 and lexicon.underscoreCounter > 0 ) or lexicon.upperCaseCounter > 0:
				print providerName + ": BAD API naming or API Naming Inconsistency Anti-Pattern"
			else:
				print providerName + ": GOOD API naming or API Naming Uniformity Pattern"

			scoreNaming = float( numberTerms - min(lexicon.lowerCaseCounter, lexicon.camelCaseCounter) - lexicon.upperCaseCounter - min(lexicon.hyphenCounter, lexicon.underscoreCounter) ) / numberTerms
			print "scoreNaming = " + str(scoreNaming)

			#
			# Scoring API consumer friendly quality
			#
			if lexicon.engineeringTermCounter > 0:
				print providerName + ": BAD business API design or Engineering-Oriented API Naming Anti-Pattern " + formatNumber(lexicon.engineeringTermCounter, numberTerms)
			else:
				print providerName + ": GOOD business API design or Business-Oriented API Naming Pattern " + formatNumber(lexicon.businessTermCounter, numberTerms)

			scoreBusiness = float(lexicon.businessTermCounter) / numberTerms
			print "scoreBusiness = " + str(scoreBusiness)

			print "Total score = " + str( ( scoreRest + scoreNaming + scoreBusiness ) / 3 )

	def visitPath(self, path):
		if path.__class__ == ontology.Resource:
			self.numberOfResources = self.numberOfResources + 1
		if path.__class__ == ontology.Controller:
			self.numberOfControllers = self.numberOfControllers + 1
		if path.__class__ == ontology.Query:
			self.numberOfQueries = self.numberOfQueries + 1
		for method in path.methods:
			self.numberOfMethods = self.numberOfMethods + 1
			if method.name in self.numberByMethod:
				nb = self.numberByMethod[method.name] + 1
			else:
				nb = 1
			self.numberByMethod[method.name] = nb
		for path in path.paths:
			self.visitPath(path)


if __name__ == "__main__":
	import sys
	print sys.argv[1:]
	model = ontology.loadDatasets(sys.argv[1:], ontology.DISTINCT_SERVICES)
	statistics = Statistics()
	statistics.visit(model)
