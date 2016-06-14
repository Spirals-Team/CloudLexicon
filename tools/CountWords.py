# This script counts words.

import csv
import sys

class WordCounter(dict):
    def __missing__(self, key):
        return 0

wordCounter = WordCounter()

# Line command CSV file arguments
for file in sys.argv[1:]:
  with open(file, 'rU') as f:
    freader = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)
    for row in freader:
      word = row[0]
      wordCounter[word] += 1


for item in wordCounter.items():
  print item[0] + ',' + str(item[1])

 