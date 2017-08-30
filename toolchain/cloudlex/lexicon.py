#################################################################################
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
# CloudLex lexicon module.
#

import re

# TODO should be reimplemented by using functional programming in Python

def contains(array, value):
	for item in array:
		if item == value:
			return True
	return False

def startswith(value, array):
	for item in array:
		if value.startswith(item):
			return True
	return False

def endswith(value, array):
	for item in array:
		if value.endswith(item):
			return True
	return False

# TODO: CHECK following verbs with Google Translate
# TODO: Use Google Translate and Wordnet to check verbs

# TODO : 'token' is used by Microsoft Azure as a verb but this is not a verb according Google Translate
# TODO : 'importTasks' is used by Microsoft Azure as a noun but this is a verbal form.

# TODO: Following list of verbs is hard-coded!!!
STRICT_VERBS = [
	"abort",			# Used by Oracle Cloud
	"auth",			# Used by Docker
	"backup",			# Used by Microsoft Azure
	"capture",			# Used by Microsoft Azure
	"drop",
	"down",			# Used by OCCI
	"enrich",			# Used by Oracle Cloud
	"exec",			# Used by Docker
	"finish",			# Used by Microsoft Azure
	"generalize",			# Used by Microsoft Azure
	# TODO: perhaps 'issue' could be in VERBS_STARTING_BY
	"issueOutOfBandManagementPowerAction".lower(), # Used by Apache CloudStack
	"ldapConfig".lower(), # Used by Apache CloudStack
	"ldapCreateAccount".lower(), # Used by Apache CloudStack
	"ldapRemove".lower(), # Used by Apache CloudStack
	"login",				# Used by Apache CloudStack
	"logout", 			# Used by Apache CloudStack
	"maproute",			# Used by IBM Bluemix
	"nexthop",			# Used by Microsoft Azure
	"reissue",			# Used by Microsoft Azure
	"reprocess",			# Used by Microsoft Azure
	"reprotect",			# Used by Microsoft Azure
	"offline",			# Used by OCCI
	"online",			# Used by OCCI
	"profile",			# Used by Microsoft Azure
	"push",				# Used by Microsoft Azure
	"unmaproute",			# Used by IBM Bluemix
	"up",				# Used by OCCI
	"tab",				# Used by Microsoft Azure
	"tag",				# Used by Microsoft Azure
	"wipe",				# Used by Microsoft Azure
]

# TODO: Following list of verbs is hard-coded!!!
VERBS_STARTING_BY = [
	"abandon",
	"accept",
	"acknowledge",
# TODO remove line 	"action",			# Used by OpenStack BUT must be removed asap
	"activate", 		# Used by Microsoft Azure
	"add",
	"allocate",
	"analyze",
	"annotate",
	"apply",			# Used by Microsoft Azure
	"attach",
	"assign",			# Used by DigitalOcean
	"associate",
	"authorize",		# Used by Microsoft Azure
	"archive",		# Used by Apache CloudStack

	"begin",
	"bind", 			# Used by IBM Bluemix
	"build",			# Used by IBM Bluemix

	"cancel",			# Used by Microsoft Azure
	"change",			# Used by Rackspace
	"clean",			# Used by Apache CloudStack
	"check",
	"claim",			# Used by Microsoft Azure
	"clear",			# Used by Microsoft Azure
	"clone",
	"collect",
	"commit",
	"complete",
	"compose",
	"configure",		# Used by Microsoft Azure
	"convert",		# Used by DigitalOcean
	"copy",			# Used by Apache CloudStack
	"create",

	"deactivate",	# Used by Microsoft Azure
	"deallocate",	# Used by Microsoft Azure
	"decrypt",
	"dedicate",		# Used by Apache CloudStack
	"detect",
	"destroy",
	"deploy",			# Used by Microsoft Azure
	"diagnose",
	"disable",
	"disassociate",	# Correct on Google Translate
	"discover",		# Used by Microsoft Azure
	"dissociate",		# Used by Apache CloudStack and correct on Google Translate

# TODO: disassociate and dissociate are synonyms

	"debug",
	"delete",
	"detach",
	"deprecate",

	"enable",
	"encrypt",
	"end",			# Used by Microsoft Azure
	"evaluate",		# Used by Microsoft Azure
	"execute",
	"expand",
	"export",
	"expunge",		# Used by Apache CloudStack
	"extract",		# Used by Apache CloudStack

	"failover",
	"find",			# Used by Apache CloudStack
	"force",			# Used by Microsoft Azure

	"generate",
	"get",

	"import",
	"insert",
	"inspect",
	"install",			# Used by Microsoft Azure
	"invalidate",
	"invoke",			# Used by Microsoft Azure
	"isenabled",

	"kill",			# Used by Docker

	"launch",
	"lease",
	"link",			# Used by Apache CloudStack
	"list",
	"load",			# Used by Microsoft Azure
	"lock",			# Used by Apache CloudStack
	"lookup",

	"mark",			# Used by Apache CloudStack
	"merge",
	"migrate",			# Used by Rackspace
	"modify",
	"move",

	"notify",			# Used by Microsoft Azure

	"terminate",
	"transfer",		# Used by DigitalOcean
	"trigger",			# Used by Microsoft Azure
	"truncate",

	"read",
	"reassociate",	# Used by Microsoft Azure
	"rebuild",			# Used by DigitalOcean
	"reboot",
	"recognize",
	"reconnect",			# Used by Apache CloudStack
	"recover",			# Used by Apache CloudStack
	"recreate",
	"redact",
	"redeploy",		# Used by Microsoft Azure
	"refresh",			# Used by IBM Bluemix
	"regenerate",	# Used by Microsoft Azure
	"register",
	"reimage",			# Used by Microsoft Azure
	"reject",
	"release",
	"remove",
	"rename",			# Used by IBM Bluemix
	"renew",			# Used by Microsoft Azure
	"repair",
	"replace",			# Used by Apache CloudStack
	"report",
	"resend",			# Used by Microsoft Azure
	"reset",
	"resize",
	"resubmit",		# Used by Microsoft Azure
	"restart",
	"restore",
	"retarget",		# Used by Microsoft Azure
	"retrieve",		# Used by Microsoft Azure
	"resume",
	"request",			# Used by IBM Bluemix
	"revert",			# Used by Apache CloudStack
	"revoke",			# Used by Apache CloudStack
	"rollback",
	"run",

	"save",
	"scale",			# Used by Apache CloudStack
	"scan",				# Used by Microsoft Azure
	"schedule",
	"search",
	"send",
	"set",
	"shutdown",
	"sign",
	"snapshot",		# Used by DigitalOcean
	"submit",
	"subscribe",		# Used by Microsoft Azure
	"suggest",			# Used by Microsoft Azure
	"suspend",
	"start",
	"stop",
	"sync",				# Used by Microsoft Azure
	"switch",

	"test",
	"trigger",
	"troubleshoot",	# Used by Microsoft Azure

	"pause",
	"perform",			# Used by Microsoft Azure
	"predict",
	"prepare",			# Used by Apache CloudStack
	"preview",
	"promote",
	"provision",		# Used by Microsoft Azure
	"publish",
	"pull",
	"purge",			# Used by Microsoft Azure
	"power",			# Used by DigitalOcean

	"unassign",		# Used by DigitalOcean
	"unbind", 			# Used by IBM Bluemix
	"undelete",
	"undo",				# Used by Microsoft Azure
	"unpause",			# Used by IBM Bluemix
	"unregister",	# Used by Microsoft Azure
	"update",
	"upgrade", 		# Used by Microsoft Azure
	"upload",			# Used by Apache CloudStack

	"query",

	"validate",
	"verify",			# Used by Microsoft Azure

	"wait",			# Used by Docker
	"wakeup",			# Used by Rackspace
	"watch",
	"write",
]

# TODO pnsCredentials ??? Which verb is it?

# TODO: Following list of verbs is hard-coded!!!
VERBS_ENDING_BY = [
#	"access", # Removed for 1and1. TODO: 'access' is both a verb and a noun so what to do?
	"check",
	"create",
	"failover", 		# Used by Microsoft Azure
	"read",
	"recognize",
	"reset",			# Used by DigitalOcean
	"update", 			# Used by Microsoft Azure
	"upgrade", 		# Used by Microsoft Azure
	"verify",			# Used by Microsoft Azure
	"write",
]

# NOT_VERBS are verbal forms used as nouns

# TODO: Following list of terms which are not verbs is hard-coded!!!
# TODO this list could by compressed by removing <verb>ing<noun> <verb>s <verb>d<nouns> etc.
# TODO renames NOT_VERBS as NOUNS
NOT_VERBS = [
# TODO 'accept' is a verb but 'accepting*' is a noun form
	"acceptingPorts".lower(),		# Used by Microsoft Azure
	"acceptingProcesses".lower(),		# Used by Microsoft Azure
	"actions",				# Used by DigitalOcean
	"actionGroups".lower(), # Used by Microsoft Azure
	"Address".lower(),			# Used by Oracle Cloud
	"AddressPurpose".lower(),			# Used by Oracle Cloud
	"addresses",			# Used by Google Cloud Platform
	"addons",			# Used by Heroku
	"aggregated",			# Used by Google Cloud Platform
	"assignedLocations".lower(),			# Used by Oracle Cloud
	"assignment",			# Used by Oracle Cloud
	"assignmentDFF".lower(),			# Used by Oracle Cloud
	"attachments",			# Used by Oracle Cloud
	"Attachment".lower(),	# Used by Oracle Cloud
	"bindings",			# Used by Kubernetes
	"changes",			# Used by Docker
	"checks",			# Used by Oracle Cloud
	"claimables",			# Used by Oracle Cloud
	"collections",			# Used by Oracle Cloud
	"commitments",			# Used by Google Cloud Platform
	"configuredFields".lower(),			# Used by Oracle Cloud
	"debuggees",			# Used by Google Cloud Platform
	"debugger",			# Used by Google Cloud Platform
	"deletedbackups",			# Used by Oracle Cloud
	"deletedvaults",	# Used by Microsoft Azure
	"deployments",			# Used by Oracle Cloud
	"EncryptionKeys".lower(), # Used by Oracle Cloud
	"endpoints",			# Used by Kubernetes
	"endpointTemplates".lower(), # Used by OpenStack
	"exportTasks".lower(), # Used by Microsoft Azure
	"exports",			# Used by Oracle Cloud
# TODO: Should be removed as 'access' was removed from VERBS_ENDING_WITH
	"flavor-access",	# Used by OpenStack
	"linkedDatabases".lower(), # Used by Microsoft Azure
	"links", # Used by Microsoft Azure
	"linkedActivities".lower(),			# Used by Oracle Cloud
	"linkedServers".lower(), # Used by Microsoft Azure
	"linkedServices".lower(), # Used by Microsoft Azure
	"listExtensions".lower(),			# Used by Oracle Cloud
	"listingConfigurations".lower(),			# Used by Oracle Cloud
	"lists",			# Used by Oracle Cloud
	"listeners",			# Used by Oracle Cloud
	"load_balancers",	# Used by DigitalOcean
	"loadbalancers",	# Used by Microsoft Azure
	"lookups",	# Used by Oracle Cloud
	"imports",			# Used by Oracle Cloud
	"installedInventories".lower(),			# Used by Oracle Cloud
	"inspectionEvents".lower(),			# Used by Oracle Cloud
	"patches",			# Used by Oracle Cloud
	"prediction",		# Used by Google Cloud Platform
	"publisher",			# Used by Oracle Cloud
	"publishingChangeAuthors".lower(),			# Used by Oracle Cloud
	"publishingChanges".lower(),			# Used by Oracle Cloud
# TODO: Should be removed as 'access' was removed from VERBS_ENDING_WITH
	"os-flavor-access",	# Used by OpenStack
	"readonlykeys",		# Used by Microsoft Azure
	"releases",			# Used by Heroku
	"runbooks",			# Used by Microsoft Azure
	"runbookcontent",	# Used by Microsoft Azure
	"rejects",			# Used by Oracle Cloud
	"restoredbackups",			# Used by Oracle Cloud
	"reportingCurrency".lower(),	# Used by Oracle Cloud
	"Reports".lower(),			# Used by Oracle Cloud
	"running",			# Used by Cloud Foundry
	"runs",				# Used by Google Cloud Platform
	"runtime",			# Used by Oracle Cloud
	"scheduledOrders".lower(), # Used by Oracle Cloud
	"schedules",			# Used by Microsoft Azure
	"settings",			# Used by Oracle Cloud
	"SigningCert".lower(), # Used by Oracle Cloud
	"snapshots",					# Used by DigitalOcean
	"syncActions".lower(), # Used by Oracle Cloud
	"syncs".lower(), # Used by Oracle Cloud
	"syncState".lower() # Used by Microsoft Azure
]

def isVerb(term):
	term = term.lower()
	if contains(STRICT_VERBS, term):
		return True
	for verb in VERBS_STARTING_BY:
		if term.startswith(verb):
			return not contains(NOT_VERBS, term)
	for verb in VERBS_ENDING_BY:
		if term.endswith(verb):
			return not contains(NOT_VERBS, term)
	return False

# TODO: Following is hard-coded!!!
def isNoun(term):
	return not isVerb(term)

# TODO: Following list of invariant terms is hard-coded!!!
INVARIANT_NOUNS = [
	"metadata"		# needed for OpenStack/Rackspace
]

# TODO: Following list of invariant terms is hard-coded!!!
NOT_PLURAL_TERMS = [
	"access"		# needed for OpenStack/Rackspace
]
# TODO: Following is hard-coded!!!
def isPlural(term):
# Previous version
#	return len(term) > 0 and isNoun(term) and ( term[-1] == 's' or contains(INVARIANT_NOUNS, term) )
# New version The order is important
	return not endswith(term.lower(), NOT_PLURAL_TERMS) and ( ( len(term) > 0 and term[-1] == 's' ) or contains(INVARIANT_NOUNS, term.lower())) 

def pluralizeTerm(term):
	if isSingular(term):
		return term + 's'
	return term

# TODO: Following is hard-coded!!!
def isSingular(term):
	return len(term) > 0 and isNoun(term) and ( term[-1] != 's' and not contains(INVARIANT_NOUNS, term.lower()) )

def singularizeTerm(term):
	if isPlural(term):
		return term[:-1]
	return term


# TODO: Following is hard-coded!!!
ANTONYMS = {
	'accept' :	[ 'reject' ],
	'add' :		[ 'remove' ],
	'attach' :	[ 'detach' ],
	'associate' :	[ 'disassociate', 'dissociate' ],
	'begin' :	[ 'end' ],
	'create' :	[ 'delete', 'destroy' ],
	'commit' :	[ 'rollback' ],
	'enable' :	[ 'disable' ],
	'encrypt' :	[ 'decrypt' ],
	'import' :	[ 'export' ],
	'insert' : [ 'remove' ],
	'load' : [ 'save' ],
	'login' : [ 'logout' ],

	# TODO : factorize as 'stop' : [ 'start', 'restart']
	'start' :	[ 'stop' ],
	'restart' :	[ 'stop' ],

	'on' : [ 'off' ],
	'up' : [ 'down' ],
	'read' : [ 'write' ]
}

def DE(noun): ANTONYMS[noun] = [ 'de' +  noun ]
DE('activate')
DE('allocate')
DE('register')

def IN(noun): ANTONYMS[noun] = [ 'in' +  noun ]
IN('validate')

def UN(noun): ANTONYMS[noun] = [ 'un' +  noun ]
UN('assign')
UN('bind')
UN('delete')
UN('do')
UN('maproute')
UN('pause')

def antonyms(term):
	return ANTONYMS.get(term.lower(), [])

#
# Source: https://stackoverflow.com/questions/29916065/how-to-do-camelcase-split-in-python
#
RE_WORDS = re.compile(r'''
    # Find words in a string. Order matters!
    [A-Z]+(?=[A-Z][a-z]) |  # All upper case before a capitalized word
    [A-Z]?[a-z]+ |  # Capitalized words / all lower case
    [A-Z]+ |  # All upper case
    \d+  # Numbers
''', re.VERBOSE)

def split_term(term):
	result = []
	for t1 in term.split('_'):
		for t2 in RE_WORDS.findall(t1):
			result.append(t2)
	return result
	

# TODO: Following list of create verbs is hard-coded!!!
CREATE_VERBS = [
	"create",
	"insert",
	"register",
	"request" # specific to IBM Bluemix
	"set",
	"submit",
]

def isCreateVerb(term):
	return contains(CREATE_VERBS, term.lower()) 

# TODO: Following list of retrieve verbs is hard-coded!!!
RETRIEVE_VERBS = [
	"get",
	"inspect",
	"list",
	"retrieve",
	"search",
]

def isRetrieveVerb(term):
	return contains(RETRIEVE_VERBS, term.lower()) 

# TODO: Following list of update verbs is hard-coded!!!
UPDATE_VERBS = [
	"modify",
	"update",
	"write"
]

def isUpdateVerb(term):
	return contains(UPDATE_VERBS, term.lower()) 

# TODO: Following list of delete verbs is hard-coded!!!
DELETE_VERBS = [
	"cancel",
	"delete",
	"destroy",
	"release" # Specific to IBM Bluemix
]

def isDeleteVerb(term):
	return contains(DELETE_VERBS, term) 

DIGITS = '1234567890'

def isVersion(term):
	return len(term) > 1 and term[0] == 'v' and term[1] in DIGITS

ENGINEERING_TERMS_STARTING_WITH = [
	'os-' # Used by OpenStack
]

ENGINEERING_TERMS = [
	'rest', # Used by Oracle Cloud
	'api',  # Used by Apache CloudStack, Kubernetes, OVH, Oracle Cloud and VMware
	'json',  # Used by Docker
	':*'  # Used by Oracle Cloud
]

def isEngineeringTerm(term):
	# A term with just one character is an engineering term, not a business term.
	if len(term) < 2:
		return True

	# A term starting by a digit is an engineering term, not a business term.
	if term[0] in DIGITS:
		return True

	# A term starting by a special character is an engineering term, not a business term.
	if term[0] in ':*_':
		return True

	if isVersion(term):
		return True

	term = term.lower()

	# A term starting by an engineering term is an engineering term, not a business term.
	if startswith(term.lower(), ENGINEERING_TERMS_STARTING_WITH):
		return True

	# Is it an engineering term or not?
	return contains(ENGINEERING_TERMS, term)

def isBusinessTerm(term):
	return not isEngineeringTerm(term)

class Term(object):
	def __init__(self, term):
		self.term = term
		self.occurrences = 1
		self.providers = set()

	def increase_occurrences(self):
		self.occurrences += 1

	def kind(self):
		pass

	def isNoun(self):
		pass

	def isVerb(self):
		pass

	def isSingular(self):
		return isSingular(self.term)

	def isPlural(self):
		return isPlural(self.term)

	def quantity(self):
		if isPlural(self.term):
			return 'Plural'
		return 'Singular'

	def case(self):
		if self.term.islower():
			return 'Lower'
		if self.term.isupper():
			return 'Upper'
		return 'Camel'

	def contains_hyphens(self):
		return '_' in self.term

	def contains_underscores(self):
		return '-' in self.term

	def is_business(self):
		return isBusinessTerm(self.term)

	def is_engineeing(self):
		return isEngineeringTerm(self.term)

	def __repr__(self):
		return self.kind() + '("' + self.term + '",' + self.quantity() + ',' + self.case() + ',' + str(self.occurrences) + ',' + str(self.providers) + ')'

class Noun(Term):
	def kind(self):
		return 'Noun'

	def isNoun(self):
		return True

	def isVerb(self):
		return False

class Verb(Term):
	def kind(self):
		return 'Verb'

	def isNoun(self):
		return False

	def isVerb(self):
		return True

class Lexicon(dict):
	def __init__(self):
		dict.__init__(self)
		# TODO: Following counters must be moved in statistics
		self.nounsCounter = 0
		self.verbsCounter = 0
		self.singularCounter = 0
		self.pluralCounter = 0
		self.lowerCaseCounter = 0
		self.upperCaseCounter = 0
		self.camelCaseCounter = 0
		self.hyphenCounter = 0
		self.underscoreCounter = 0
		self.businessTermCounter = 0
		self.engineeringTermCounter = 0

	def newTerm(self, term):
		result = self.get(term)
		if result == None:
			if isVerb(term):
				result = Verb(term)
			else:
				result = Noun(term)
			self[term] = result
			# TODO: Following tests and counting must be moved in statistics
			if result.isNoun():
				self.nounsCounter += 1
			if result.isVerb():
				self.verbsCounter += 1
			if result.isSingular():
				self.singularCounter += 1
			else: # if result.isPlural():
				self.pluralCounter += 1
			if result.term.islower():
				self.lowerCaseCounter += 1
			else:
				if result.term.isupper():
					self.upperCaseCounter += 1
				else:
					self.camelCaseCounter += 1
			if result.contains_hyphens():
				self.hyphenCounter += 1
			if result.contains_underscores():
				self.underscoreCounter += 1
			if result.is_business():
				self.businessTermCounter += 1
			else:
				self.engineeringTermCounter += 1
		else:
			result.increase_occurrences()
		return result

	def __repr__(self):
		return 'Lexicon(' + dict.__repr__(self) + ',' + str(self.nounsCounter) + ' nouns,' + str(self.verbsCounter) + ' verbs,' + str(self.singularCounter) + ' singular,' + str(self.pluralCounter) + ' plural,' + str(self.lowerCaseCounter) + ' lower,' + str(self.upperCaseCounter) + ' upper,' + str(self.camelCaseCounter) + ' camel' + ')'

