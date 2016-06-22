# This script extracts service occurrences from URI datatset files.

import csv
import sys

class Occurrence(dict):
    def __missing__(self, key):
        return 0

serviceOccurrences = Occurrence()

# Line command CSV file arguments
with open(sys.argv[1], 'rU') as f:
    freader = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)
    for row in freader:
      service = row[1]
      serviceOccurrences[service] += 1

for item in serviceOccurrences.items():
  print item[0] + ',' + str(item[1])
