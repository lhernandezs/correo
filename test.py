import csv
import os
with open(os.path.join('datos', 'fichas.csv'), newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(', '.join(row))