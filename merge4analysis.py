# python merge4analysis.py 

import csv
import os

array = []
i = 1

for file in os.listdir("combined/"):
	if file.endswith(".csv"):
		with open("combined/"+file) as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='"')
			if i == 1:
				array += [row for row in reader] # put all the csv into an array
			else:
				array += [row for row in reader if row[0] != "deptDe"] # put the csv into an array but excluding the headers
			i += 1

with open("master_export.csv", 'wb') as output:
	writer = csv.writer(output, delimiter=',', lineterminator='\n') # , quoting=csv.QUOTE_NONNUMERIC
	writer.writerows(array)
