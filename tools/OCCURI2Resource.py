import csv
import sys

#Line command CSV file argument
file = sys.argv[1]

provider = 'OCCI'

with open(file, 'rU') as f:
     freader = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)
     for row in freader:
	uri = row[0]     	
	httpMethod = row[1]
	service = row[2]
	reference = row[3]

	#Analyse resources and actions in the URI	
	tokens = uri.split('/',100)
		
	for token in tokens:
	  if '?action' not in token:
          #Resource 
	    if token == '{provider_specific_path}' or token == '':
	      continue
	    print provider + ',' + service + ',' + 'RESOURCE' + ',' + token + ',' + httpMethod + ',' + uri + ',' + reference  
 	  else :
	  #Action
	    print provider + ',' + service + ',' + 'ACTION' + ',' + token.split('=',1)[1] + ',' + httpMethod + ',' +  uri + ',' + reference  
	

  #print('Exception: it has subresources!')
  #exit(-1)

	
	
	
	

