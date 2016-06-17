import csv
import sys
import requests

#Google Cloud Platform Documentation
#Main source -> https://cloud.google.com/docs/

#Line command CSV file argument
file = sys.argv[1]

with open(file, 'rU') as f:
	provider = 'Google Cloud Platform'
	freader = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)

	for row in freader:
		service = row[0]
		reference = row[1]

		resp = requests.get(url=reference)

		for line in resp.iter_lines():
			code = line.strip()
			if '<code>' in code and code[0:6] == '<code>' and '</td>' not in code:
				code = code[6:code.find('</code>')]
				code = code.replace('&nbsp;','')
				code = code.replace('<var class="apiparam">','{')
				code = code.replace('</var>','}')

				if code.find('/') == -1:
					#It is not a URI
					continue

				httpMethod = code[0:code.find('/')].strip()
				uri = code[code.find('/'):].strip()

				#Analyse resources and actions in the URI
				tokens = uri.split('/',100)

				for token in tokens:
					if token == '' or token == 'v1' or token == 'v2' or token == 'v3':
						continue
					if token[0] == '*' or token[0] == '{':
						continue
					if ':' not in token:
						#Resource
						print provider + ',' + service + ',' + 'RESOURCE' + ',' + token + ',' + httpMethod + ',' + uri + ',' + reference
					else:
						#Action
						print provider + ',' + service + ',' + 'ACTION' + ',' + token.split(':',1)[1] + ',' + httpMethod + ',' +  uri + ',' + reference
