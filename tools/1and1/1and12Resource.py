import requests, re
from bs4 import BeautifulSoup

#This script uses BeautifulSoup library. To download : >Path\Python36-32\Scripts\easy_install.exe beautifulsoup4

#1&1 Cloud Server API v1 - Documentation
#Main source -> https://cloudpanel-api.1and1.com/documentation/v1/en/documentation.html#

provider = '1&1 Cloud Server'
reference = 'https://cloudpanel-api.1and1.com/documentation/v1/en/documentation.html'
resp = (requests.get(url=reference)).content
soup = BeautifulSoup(resp, "html.parser")

for i in soup.find_all("div", { "class" : "panel panel-default" }):
    service = str(i.find('h3'))
    service = service[service.find('>')+1:service.find('</h3>')]
    token = service.lower()

    for j in i.find_all("div",{"class":"panel panel-white"}):
        uri = str(j.find("a",{"class":"collapsed"}))
        uri = uri[uri.find('<span class="parent">')+21:uri.find('</a>')]
        uri = uri.replace('</span>','')

        for k in j.find_all("div", { "class" : "list-group-item" }):
            name = {'class': re.compile('.*badge.*')}
            method = str(k.find_all(**name))
            method = method.replace('[<span class="badge badge_get">','')
            method = method.replace('[<span class="badge badge_post">', '')
            method = method.replace('[<span class="badge badge_delete">', '')
            method = method.replace('[<span class="badge badge_put">', '')
            method = method.replace('</span>]', '')
            
            description = str(k.find_all("div", { "class" : "method_description" }))
            description = description.replace('[<div class="method_description"><p>','')
            description = description.replace('</p></div>]', '')

            print(provider + ',' + service + ',' + 'RESOURCE' + ',' + token + ',' + method + ',' + uri + ',' + description + ',' + reference)