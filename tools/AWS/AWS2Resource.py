import csv
import sys
import requests

#Amazon Web Services Documentation
#Main source -> http://docs.aws.amazon.com/apigateway/api-reference/resource/

#Line command CSV file argument
file = sys.argv[1]
#file = "C:/users/admin/desktop/amazon.csv"

with open(file, 'rU') as f:
    provider = 'Amazon Web Services'
    freader = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)

    for row in freader:
        service = row[0]
        reference = row[1]

        resp = requests.get(url=reference)

        for line in resp.iter_lines():
            code = line.strip()
            if '<p><p>' in code:
                description = code[6:code.find('</p>')]
                if '<a' in description:
                    crop = description[description.find('<a'):description.find('>') + 1]
                    description = description.replace(crop,'')
                description = description.replace('</a>', '')
                description = description.replace('<code>', '')
                description = description.replace('</code>', '')
                description = description.replace('&#39;', "'")
                if '<a' in description:
                    crop = description[description.find('<a'):description.find('>') + 1]
                    description = description.replace(crop, '')

            if '<code>' in code and code[0:5] == '<pre>' and 'HTTP' not in code:
                code = code[11:code.find('</code>')]
                code = code.replace('&nbsp;','')
                code = code.replace('<var class="apiparam">','{')
                code = code.replace('</var>','}')
                code = code.replace('<br/>','/')

                if code.find('/') == -1:
                    #It is not a URI
                    continue

                httpMethod = code[0:code.find('/')].strip()
                uri = code[code.find('/'):].strip()
                uri = uri.replace('&lt;','<')
                uri = uri.replace('&gt;', '>')
                print provider + ',' + service[0:service.find(':')] + ',' + 'RESOURCE' + ',' + service[service.find(':') + 1:] + ',' + httpMethod + ',' + uri + ',' + description + ',' + reference