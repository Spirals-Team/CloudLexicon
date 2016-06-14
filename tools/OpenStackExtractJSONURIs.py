import csv
import sys

import requests

#OpenStack Swagger Documentation
url = 'http://rackerlabs.github.io/wadl2swagger/'
urlDocs = url + 'openstack.html'

resp = requests.get(url=urlDocs)

for line in resp.iter_lines():
  if '.json</a>' in line:


    print url + line[line.find('">')+2:line.find('</a>')]



