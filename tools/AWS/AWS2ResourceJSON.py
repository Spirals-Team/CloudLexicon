import json, requests, csv, re

#Amazon Web Services Documentation
#Main source -> http://docs.aws.amazon.com/apigateway/api-reference/resource/

#Line command CSV file argument
#file = sys.argv[1]
file = "C:/users/admin/desktop/aws.csv"

provider = 'Amazon Web Services'

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

with open(file, 'rU') as f:
    provider = 'Amazon Web Services'
    freader = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)

    for row in freader:
        service = row[0]
        reference = row[1]

        resp = json.loads(requests.get(url=reference).text)["operations"]
        for i in resp:
            token = resp[i]["name"]
            method = resp[i]["http"]["method"]
            uri = resp[i]["http"]["requestUri"]
            if uri == '/':
                uri = uri + token.lower()
            if 'documentation' in resp[i]:
                documentation = resp[i]["documentation"]
            else:
                documentation = 'No description'
            documentation = cleanhtml(documentation)
            print(provider + ',' + service + ',' + "RESOURCE" + ',' + token + ',' + method + ',' + uri + ',' + documentation + ',' + reference)
