# Swiss Administration Procurements 

## Description
This repo describes the data handling and methodology behind the Swiss federal administration procurements project. The project was published in English, German and French by swiss newspapers *Le Matin Dimanche* and *SonntagsZeitung*.

See it live here:
http://enquete.lematindimanche.ch/achats  
and here: http://dok.sonntagszeitung.ch/2016/beschaffungen

The interactive data visualization was created with the help of *Datastory*. Its source code is available separately on [Florian Evéquoz's repository](https://github.com/evequozf/Swiss_Procurement-LeMatinDimanche).

## How did we get the data?
We made a FOIA request to obtain the data. The administration refused and we had to go to the swiss highest court which ruled in our favor on December 2, 2015. That's more than three years after our initial request. Each federal department was compelled to give us their 40 main suppliers in terms of turnover.

## Original data format
The federal administration was kind enough to send us all the data in PDF. One file for each of the eight departments and for each year from 2011 to 2014. That's [32 files](pdf/biggest) in total.

Each of these files contains one triple-entry table. The columns contain the offices (smaller administrative units) inside the department. The rows contain the 40 biggest suppliers and the amount they received from each office. As a third dimension, the amount for each supplier is subdivided in categories of goods and services.

There is 22 main categories which are themselves sometimes divided into subcategories. For the sake of simplicity, the visualization shows only the main categories.

## Crossing the data
Beside the data with the 40 biggest suppliers, we asked the federal administration how much each office spent in total for each of the 22 categories from 2011 to 2014. That would indicate us which percentage of this global amount the 40 biggest suppliers represent. Once again, the data was delivered in PDF format, very similar to the 40 biggest suppliers data: [32 other files](pdf/categories).

## Scraping and cleaning
We used [Tabula](http://tabula.technology/) to scrape the PDF. We found the Lattice method to be more accurate with our data. The cleaning was made in Google Spreadsheet: removing thousand separator, removing unnecessary total columns, etc.

At this stage we have one CSV for each department and each year for the [40 biggest suppliers](csv/biggest) and the same for the [overall categories](csv/categories) data.

## Combine both datasets and merge all departments
We wrote a [python script](combine-and-merge-all.py) to combine the 40 biggest suppliers data with the categories data.

```
python combine-and-merge-all.py
```

This script does three things for each department and each year.

First, it goes through the 40 biggest suppliers CSV file and creates a new array where each line is a procurement (with a department, an office, a supplier, a category and an amount).

It then makes the same thing with the categories data (with 0 as supplier id as it is unknown). The original PDFs sometimes give an total amount for one of the main categories and then a detailed repartition between the subcategories. The script takes only the detailed information (even if we won't use it in the visualization, it could be useful for the analysis) since the total for the main categories can easily be reconstructed with a sum. 

Third, the script merges the 40 biggest suppliers and the categories data. We subtract, for each category and subcategory, the amount paid to the 40 biggest suppliers.

Finally the script merges the combined-data for all the departments and outputs the CSV that will be used by the visualization. To optimize performance, this file only includes the supplier id, the category id and the name of the office in German. Beside we created three CSV files with the [suppliers names](import/suppliers-utf8.csv), [categories names](import/categories-utf8.csv), [departments](import/depts-utf8.csv) and [offices](import/offices-utf8.csv) in different languages. We also standardized the name of some suppliers (for example sometimes the same supplier was written in French in one department and in German in an other one).

## Last caveat: undisclosed categories
The last department that sends us the data was the Department of Defense. And for security reasons, they don't want to disclose in which of the 22 categories their biggest suppliers are active. The problem was that the python script could not subtract the amounts of the 40 biggest suppliers from the categories data since we don't know to which category they belong. We solved that by adding a line to the 40 biggest suppliers data with negative amounts attributed to an unknown supplier.

## Get in touch
alexandre.haederli[at]lematindimanche.ch or on [twitter](https://twitter.com/alexhaederli)

## Licence
[BSD](https://opensource.org/licenses/BSD-3-Clause) 
