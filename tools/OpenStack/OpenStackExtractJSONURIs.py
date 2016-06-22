#
# This script generates the list of URIs where the Swagger JSON documentation for OpenStack is.
# 

# To install the requests module, execute:
# - pip install requests OR easy_install requests
#
import requests

# Where the OpenStack Swagger Documentation is
urlOpenStackSwaggerDocumentation = 'http://rackerlabs.github.io/wadl2swagger/'

resp = requests.get(url=urlOpenStackSwaggerDocumentation + 'openstack.html')
for line in resp.iter_lines():
  if '.json</a>' in line:
    print urlOpenStackSwaggerDocumentation + line[line.find('">')+2:line.find('</a>')]
