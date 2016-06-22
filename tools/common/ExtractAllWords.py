# This script extracts words from URI dataset files.

import csv
import sys

# Line command CSV file arguments
for file in sys.argv[1:]:
	with open(file, 'rU') as f:
		freader = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)
		for row in freader:
			provider = row[0]
			# print provider
			# service = row[1]
			# print service
			uri = row[2]     	
			# httpMethod = row[3]
			# print httpMethod
			# reference = row[4]

			# Analyse resources and actions in the URI	
			tokens = uri.split('/',100)
			for token in tokens:
				if '?action' not in token:
					# For Google Cloud Platform
					if provider == 'Google Cloud Platform':
						if ':' in token:
							token = token.split(':',1)[1]
							if token != '':
								print token
							continue
						if token == "operations}" or token == "www.googleapis.com":
							continue

					# Resource 
					if token == '{provider_specific_path}' or token == '' or token[0] == '{' or token == ',' or token.isdigit() or token[0] == '*':
						continue
					# OpenStack
					if token.find('v1') > -1 or token.find('v2') > -1 or token.find('v3') > -1:
						continue

					print token
				else :
					# OCCI Action
					print 'action'
					print token.split('=',1)[1]  
