import csv
import os

array_out = [] # create new array for output
array_out.append(["deptDe", "fullDeptDe", "year", "idSupplier", "supplier", "idCategory", "intCategory", "fullCategoryDe", "officeDe",  "amount"]) # headers for the output array

for file in os.listdir("categories/"):
	if file.endswith(".csv"):
		with open("categories/"+file) as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='"')

			# put the csv into an array
			array_in = [row for row in reader]

			for y in range(1, len(array_in)): # go through the table line by line starting with line 1
				for x in range(7, len(array_in[0])): # go through the line starting with column 7
					if array_in[y][x]: # if cell is not empty
						if not float(array_in[y][5]).is_integer(): # if it's a subcategory -> add to array
							array_out.append([array_in[y][0], array_in[y][1], array_in[y][2], "0", "Unknown", str(array_in[y][5]).replace(".0",""), int(float(array_in[y][5])), array_in[y][6], array_in[0][x], array_in[y][x]]) # write a new line in the output array
						elif y < (len(array_in)-1) and float(array_in[y+1][5]).is_integer(): # if next line is int (=main category) -> no subcategories -> add to array
							array_out.append([array_in[y][0], array_in[y][1], array_in[y][2], "0", "Unknown", str(array_in[y][5]).replace(".0",""), int(float(array_in[y][5])), array_in[y][6], array_in[0][x], array_in[y][x]]) # write a new line in the output array
						elif y == (len(array_in)-1):
							array_out.append([array_in[y][0], array_in[y][1], array_in[y][2], "0", "Unknown", str(array_in[y][5]).replace(".0",""), int(float(array_in[y][5])), array_in[y][6], array_in[0][x], array_in[y][x]]) # write a new line in the output array

# write the output array in a csv file
with open("export_cat.csv", 'wb') as output:
	writer = csv.writer(output, delimiter=',', lineterminator='\n') # , quoting=csv.QUOTE_NONNUMERIC
	writer.writerows(array_out)