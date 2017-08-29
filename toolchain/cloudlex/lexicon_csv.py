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
# CloudLex lexicon_csv module.
#

from cloudlex import ontology

def yes_no(bool):
	if bool:
		return 'Yes'
	else:
		return 'No'

def generate_lexicon_csv_for_one_provider(model):
	lexicon = model.lexiconOfNounsVerbs
	terms = sorted(lexicon.values(), key=lambda term: ( term.occurrences, term.term ), reverse=True)
	print '"Term","Kind","Quantity","Case","Hyphens","Underscores","Business","Occurrences"'
	for term in terms:
		print '"' + term.term + '","' + term.kind() + '","' + term.quantity() + '","' + term.case() + '","' + yes_no(term.contains_hyphens()) + '","' + yes_no(term.contains_underscores()) + '","' + yes_no(term.is_business()) + '","' + str(term.occurrences) + '"'

def generate_lexicon_csv_for_all_providers(model):
	# Generate the first line of the CSV file.
	providerColunmNames = ''
	for provider in model.providers:
		providerColunmNames += ',"' + provider.name + '"'
	print '"Term","Kind","Quantity","Case","Hyphens","Underscores","Business","Occurrences","# of Providers",' + providerColunmNames

	# Create an array for storing terms according their provider occurrence.
	occurrenceOfTerms = []
	for index in range(len(model.providers)):
		occurrenceOfTerms.append([])

	# Classify each term according to its number of providers.
	for term in model.lexiconOfNounsVerbs.values():
		nbProviders = len(term.providers)
		occurrenceOfTerms[nbProviders].append(term)

	for terms in reversed(occurrenceOfTerms):
		for term in sorted(terms, key=lambda term: term.term):
			providersText = ''
			for provider in model.providers:
				if provider.name in term.providers:
					providersText += ',"Yes"'
				else:
					providersText += ',""'
			print '"' + term.term + '","' + term.kind() + '","' + term.quantity() + '","' + term.case() + '","' + yes_no(term.contains_hyphens()) + '","' + yes_no(term.contains_underscores()) + '","' + yes_no(term.is_business()) + '","' + str(term.occurrences) + '"' + '","' + str(len(term.providers)) + '"' + providersText

#
# Main program
#

if __name__ == "__main__":
	import sys
	model = ontology.loadDatasets(sys.argv[1:])
	if len(model.providers) == 1:
		generate_lexicon_csv_for_one_provider(model)
	else:
		generate_lexicon_csv_for_all_providers(model)
