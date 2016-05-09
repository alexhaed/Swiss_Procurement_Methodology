# Swiss Administration Procurements 

## Description
This repo describes the data handling and methodology behind the Swiss federal administration procurements project. The project was published in English, German and French by swiss newspapers *Le Matin Dimanche* and *SonntagsZeitung*.

You can see it live here:
http://enquete.lematindimanche.ch/achats and here: http://dok.sonntagszeitung.ch

Disclosure: I'm a journalist playing code, not a developer. Don't judge me by my code!

## How did we get the data?
FOIA
Three years
Highest court
40 biggest

## Original Data Format
The Federal Administration was kind enough to send us all the data in PDF. There is one file for each of the eight departments and for each year from 2011 to 2014. So [32 files](pdf/biggest) in total.

Each of these file contains one triple-entry table. The columns contains the offices (smaller administrative units) inside the department. The rows contains the 40 biggest suppliers and the amount they received from each office. As a third dimension, the amount for each supplier is subdivided in categories of goods and services.

There is 22 main categories which are themselves sometimes divided into subcategories. For the visualization, we kept only the main categories.

## Crossing the data
Beside the data with the 40 biggest suppliers, we asked the federal administration you much each office spent in total for each of the 22 categories. That would indicate us with part of the global amount the 40 biggest suppliers represent. Once again, the data arrived in PDF format, very similar to the 40 biggest suppliers data: [32 other files](pdf/categories).

## Scraping and cleaning
We used [Tabula](http://tabula.technology/) to scrape the PDF. We found the Lattice method to be more accurate with our data. The cleaning was made in Google Spreadsheet: removing thousand separator, removing unnecessary total columns, etc.

At this stage we have one CSV for each department and each year for the [40 biggest suppliers](csv/biggest) and the same for the [overall categories](csv/categories) data.

## Combine both datasets and mege all departements
We wrote a [python script](combine-and-merge-all.py) to combine the 40 biggest suppliers data with the categories data.

```
python combine-and-merge-all.py
```

This script does three things for each department and each year.

First, it goes through the 40 biggest CSV and create a new array where each line is a procurement (with a department, an office, a supplier, a category and an amount).

It then makes the same thing with the categories data. The categories data has 0 as a supplier id as it is unknown. The original PDFs sometimes give an total amount for one of the main categories and then a detailled repartition between the subcategories. The script then takes only the detailed information since the total for the main categories can easily be rescontructed with a sum. 

Third, the script merges the 40 biggest and the categories data. We subtract, for each category and subcategory, the amount paid to the 40 biggest suppliers. Example: if a company among the 40 biggest supply for 100'000 of food, we subtract that amount from the overall category data (otherwise it would counted twice).

Finally the script merges the combined-data for all the departments and outputs the used CSV for the visualization. To optimize the performance, this file only includes the supplier id, the category id and the name of the office in German. Beside we crated three CSV files with the [suppliers names](import/suppliers-utf8.csv), [categories names](import/categories-utf8.csv), [departments](import/depts-utf8.csv) and [offices](import/offices-utf8.csv) in different languages. We also standardized the name of some suppliers (sometimes the same supplier was writen in French in one department and in German in an other one).

## Last caveat: undisclosed categories
The last department to send us the data was the Department of Defense. And for security reasons, they don't want to disclose in which of the 22 categories their biggest suppliers are active. The problem was that the python script could not substract the 40 biggest amounts from the categories data since we don't know to which category they belong. We solved that by adding a line to the 40 biggest suppliers data with negative amounts attributed to an unknown supplier.

## Get in touch
You can contact us here: alexandre.haederli[at]lematindimanche.ch or on [twitter](https://twitter.com/alexhaederli)
