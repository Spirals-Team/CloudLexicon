import csv
import sys

from neo4j.v1 import GraphDatabase, basic_auth

#Line command CSV file argument
file = sys.argv[1]

driver = GraphDatabase.driver("bolt://localhost")
session = driver.session()
session.run("MATCH (n) DETACH DELETE n")

with open(file, 'rU') as f:
     freader = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)
     for row in freader:
       	provider = row[0]
	
	providerNode = session.run("MATCH (n:Provider) WHERE n.name = '%s' RETURN n" % provider)
	print providerNode.keys()
	for record in providerNode:
		print record
		
	
	
	#service = row[1]
	#type = row[2]
	#term = row[3]     	
	#httpMethod = row[4]
	#uri = row[5]	
	#reference = row[6]

	#neoCommand = "CREATE (t:Term {term:'%s', type: '%s', provider:'%s', service:'%s', httpMethod: '%s', uri:'%s', reference: '%s' })" % (term, type, provider, service, httpMethod, uri, reference)
	#print neoCommand
  	#session.run(neoCommand)

session.close()
	
	
	
	

