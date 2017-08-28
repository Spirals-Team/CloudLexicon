import requests, csv, re
from bs4 import BeautifulSoup

#OpenStack Application Catalog API v1
#Main source -> https://developer.openstack.org/api-ref/application-catalog/v1/index.html
file = sys.argv[1]
provider = 'Open Stack'

with open(file, 'rU') as f:
    freader = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)

    for row in freader:
        service = row[0]
        reference = row[1]

        resp = (requests.get(url=reference)).content
        soup = BeautifulSoup(resp, "html.parser")

        for i in soup.find_all("dl"):
            if '>type <' not in str(i):
                if len(i.find_all('code',{ "class" : "descname" })) < 2:
                    continue
                method = (i.find_all('code',{ "class" : "descname" }))[0].text.strip()
                uri = (i.find_all('code', {"class": "descname"}))[1].text
                documentation = (i.find('p')).text
                token = uri[1:uri.find('/',1)]
                print(provider + ',' + service + ',' + "RESOURCE" + ',' + token + ',' + method + ',' + uri + ',' + documentation + ',' + reference)
