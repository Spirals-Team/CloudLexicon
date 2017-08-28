import sys,requests, csv, re
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

        for i in soup.find_all("div", { "class" : "detail-control section" }):
            name = {'class': re.compile('.*label.*')}
            method = (i.find(**name)).text
            uri = (i.find("div", { "class" : "row col-md-12" })).text
            documentation = (i.find("p", { "class" : "url-subtitle" })).text
            if not (i.find("div", {"class": "row col-md-12"})).contents:
                continue
            token = ((i.find("div", { "class" : "row col-md-12" })).contents[0]).replace('/','')
            print(provider + ',' + service + ',' + "RESOURCE" + ',' + token + ',' + method + ',' + uri + ',' + documentation + ',' + reference)
