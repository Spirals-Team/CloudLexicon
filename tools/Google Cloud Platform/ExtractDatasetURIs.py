import csv
import sys
import requests

# Google Cloud Platform Documentation
# Main source -> https://cloud.google.com/docs/

# Line command CSV file argument
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

				code = code.replace('<br/>','/')

				if code.find('/') == -1:
					#It is not a URI
					continue

				httpMethod = code[0:code.find('/')].strip()
				uri = code[code.find('/'):].strip()

				print provider + ',' + service + ',' + uri + ',' + httpMethod + ',' + reference
