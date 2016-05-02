# python combine.py "biggest/EDA - 2014.csv" "categories/EDA - 2014" combined/EDA-2014.csv
# python combine.py "biggest/EFD - 2014.csv" "categories/EFD - 2014.csv" combined/EFD-2014.csv
# python combine.py "biggest/UVEK - 2014.csv" "categories/UVEK - 2014.csv" combined/UVEK-2014.csv
# python combine.py "biggest/EJPD - 2014.csv" "categories/EJPD - 2014.csv" combined/EJPD-2014.csv
# python combine.py "biggest/EDI - 2014.csv" "categories/EDI - 2014.csv" combined/EDI-2014.csv
# python combine.py "biggest/WBF - 2014.csv" "categories/WBF - 2014.csv" combined/WBF-2014.csv

import sys
import csv

# check arguments
if not len(sys.argv) is 4:
	print("Three arguments required: biggest, categories and outputfile")
	sys.quit()

biggest = sys.argv[1]
categories = sys.argv[2]
outputfile = sys.argv[3]
array_biggest = []
array_categories = []
array_unknown = []
table_unknown = {} # dictionnary

####################################
#### CONVERT THE 40 BIGGEST FILE ###
####################################
with open(biggest, 'rt') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')

	# put the csv into an array
	array_in = [row for row in reader]

	# headers for the output array
	array_biggest.append(["deptDe", "fullDeptDe", "year", "idSupplier", "supplier", "idCategory", "intCategory", "fullCategoryDe", "officeDe", "amount"])

	for y in range(1, len(array_in)): # go through the table line by line starting with line 1
		for x in range(7, len(array_in[0])): # go through the line starting with column 7
			if array_in[y][x]: # if cell is not empty
				array_biggest.append([array_in[y][0], array_in[y][1], array_in[y][2], array_in[y][3], array_in[y][4], str(array_in[y][5]).replace(".0",""), int(float(array_in[y][5])), array_in[y][6], array_in[0][x], array_in[y][x]]) # write a new line in the output array

####################################
#### CONVERT THE CATEGORIE FILE  ###
####################################
with open(categories, 'rt') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')

	# put the csv into an array
	array_in = [row for row in reader]

	# headers for the output array
	array_categories.append(["deptDe", "fullDeptDe", "year", "idSupplier", "supplier", "idCategory", "fullCategoryDe", "officeDe", "amount"])

	for y in range(1, len(array_in)): # go through the table line by line starting with line 1
		for x in range(7, len(array_in[0])): # go through the line starting with column 7
			if array_in[y][x]: # if cell is not empty
				if float(array_in[y][5]).is_integer(): # only if it's a main category (filter out the subcategories)
					array_categories.append([array_in[y][0], array_in[y][1], array_in[y][2], "0", "Unknown", array_in[y][5], array_in[y][6], array_in[0][x], array_in[y][x]]) # write a new line in the output array

with open(outputfile, 'wb') as output:
	writer = csv.writer(output, delimiter=',', lineterminator='\n') # , quoting=csv.QUOTE_NONNUMERIC
	writer.writerows(array_categories)

####################################
####        COMBINE DATA         ###
####################################
# fetch the total amount for each categories and offices
for y in range(1, len(array_categories)): # go through the table line by line
	catoffice = str(array_categories[y][5]) + "|" + str(array_categories[y][7]) # create a unique key combinining the category number and the office (category_nb|offce)
	table_unknown[catoffice] = array_categories[y][8] # put the key in the dictionnary and add the total amount for this category and office as value

# fetch the 40biggest data
for x in range(1, len(array_biggest)): # go through the table
	z = str(array_biggest[x][5]) + "|" + array_biggest[x][8] # generate unique key for this line with subcategories (decimal)

	if not z in table_unknown: # if subcategory not in the categories data
		z = str(array_biggest[x][6]) + "|" + array_biggest[x][8] # unique key with main categorie

	res = round(round(float(table_unknown[z]),2) - round(float(array_biggest[x][9]),2),2) # make the substraction
	if float(res) == 0.0: # if amount after substraction equals 0
		table_unknown.pop(z, None) # delete the key from the dictionnary
	else:
		table_unknown[z] = res # if not, the new amount is set

# convert the table_unknown results into the same format as the 40biggest data (same columns)
# dept,fullDept,year,idSupplier,supplier,idCategory,intCategory,fullCategory,office,amount
for k,v in table_unknown.items():
	categorie = k.split("|")
	array_unknown.append([array_biggest[1][0], array_biggest[1][1], array_biggest[1][2], "0", "Unknown", categorie[0], categorie[0], "", categorie[1], v])

# combine the 40 biggest data and the unknown data in a new csv file
with open(outputfile, 'wb') as output:
	writer = csv.writer(output, delimiter=',', lineterminator='\n') # , quoting=csv.QUOTE_NONNUMERIC
	writer.writerows(array_biggest)
	writer.writerows(array_unknown)
