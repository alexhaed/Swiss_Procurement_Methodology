import os
import csv
import numpy as np

dept_table = ["EDA", "EFD", "UVEK", "EJPD", "VBS", "BK", "WBF", "EDI"] # list all the departments
years_table = ["2011", "2012", "2013", "2014"] # list the avaiable years

# removes previous output files
files = os.listdir("combined/")
for f in files:
    os.remove(f)

for dept in dept_table: # this loop will apply for each department...
	for year in years_table: # ... and for each year
		biggest = "biggest/"+dept+" - "+year+".csv" # path to CSV with the 40 biggest data
		categories = "categories/"+dept+" - "+year+".csv" # path to CSV with the categories data
		outputfile = "combined/"+dept+" - "+year+".csv" # path for output file
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

		#####################################
		#### CONVERT THE CATEGORIES FILE  ###
		#####################################
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

		#########################################
		####  COMBINE BIGGEST AND CATEGORIES  ###
		#########################################
		# fetch the total amount for each category and office
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


###############################
####     MERGE ALL DEPT     ###
###############################
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

arraynp = np.asarray(array)
exportshort = np.delete(arraynp, [1,4,5,7], 1) # delete unnecessary colums

with open("master_export_short.csv", 'wb') as output:
	writer = csv.writer(output, delimiter=',', lineterminator='\n')
	writer.writerows(exportshort)
