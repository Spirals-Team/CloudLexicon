# This script extracts request type occurrences from URI datatset files.

import csv
import sys

class Occurrence(dict):
    def __missing__(self, key):
        return 0

requestOccurrences = Occurrence()

# Line command CSV file arguments
with open(sys.argv[1], 'rU') as f:
    freader = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)
    for row in freader:
      httpMethod = row[3]
      requestOccurrences[httpMethod] += 1

for item in requestOccurrences.items():
  print item[0] + ',' + str(item[1])
