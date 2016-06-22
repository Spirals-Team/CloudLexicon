import csv
import sys

from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost")
session = driver.session()

result = session.run("MATCH (n) RETURN n")

for record in result:
  print record

session.close()

	

	
	
	
	

