# python merge4viz.py 

import csv
import os
import numpy as np

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

########################################################
####         TEMPORARY ADD CATEGORIES DATA          ####
####  combine_categories_only.py  has to run first  ####
########################################################
with open("combined_categories_only.csv") as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	array += [row for row in reader if (row[0] != "deptDe" and row[0] != "EDA" and row[0] != "EFD" and row[0] != "UVEK" and row[0] != "EJPD" and row[0] != "EDI" and row[0] != "WBF")] # put the csv into an array but excluding the headers
########################################################
####       END TEMPORARY ADD CATEGORIES DATA        ####
########################################################

arraynp = np.asarray(array)
exportshort = np.delete(arraynp, [1,4,5,7], 1) # delete unnecessary colums
# exportshort = np.delete(arraynp, [1,4,6,7], 1) # delete unnecessary colums

with open("master_export_short.csv", 'wb') as output:
	writer = csv.writer(output, delimiter=',', lineterminator='\n') # , quoting=csv.QUOTE_NONNUMERIC
	writer.writerows(exportshort)
