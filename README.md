# Swiss Administration Procurements 

## Description
This repo describes the data handling and methodology behind the Swiss federal administration procurements project. The project was published in English, German and French by swiss newspapers *Le Matin Dimanche* and *SonntagsZeitung*.

You can see it live here:
http://enquete.lematindimanche.ch and here: http://dok.sonntagszeitung.ch

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

## Combine both datasets
We wrote a first [python script](combine.py) to combine the 40 biggest suppliers data with the categories data. This script first put the original data into an array where each line is a procurement (with a department, an office, a supplier, a category and an amount).

The categories data has 0 as a supplier as it is unknown. We subtract, for each category and subcategory, the amount paid to the 40 biggest suppliers. Example: if a company among the 40 biggest supply for 100'000 of food, we subtract that amount from the overall category data (otherwise it would counted twice).

We ran the script for each department and each year (we didn't receive all the data together at the same time). The script returns a CSV given as fourth argument:

```
python combine.py "biggest/EDA - 2014.csv" "categories/EDA - 2014.csv" combined/EDA-2014.csv
```

## Merge the data
A [second python script](merge4viz.py) just merge all the files created in the "combined" directory. The output is a CSV that we used for the visualization.

```
python merge4viz.py
```

To optimize the performance, this file only includes the supplier id, the category id and the name of the office in German. Beside we crated three CSV files with the suppliers names, category names and offices in different languages. We also standardized the name of some suppliers (sometimes the same supplier was writen in French in one department and in German in an other one).

A [third python script](merge4analysis.py) merge the same data but output a CSV with more information (like the supplier name). This spreadsheet was shared with colleagues working on the analysis with software like Excel or Tableau.

```
python merge4viz.py
```

## Last caveat: undisclosed categories
The last department to send us the data was the Department of Defense. And for security reasons, they don't want to disclose in which of the 22 categories their suppliers are active. We added a category with 0 as id. The problem was  that these amounts were not subtracted in the python script and were counted twice in the visualization. We solved that with a small modification in the [python script](combine_vbs.py) and a tweak in the visualization so that this category is not counted in the "By category" chart.

## Get in touch
You can contact us here: alexandre.haederli[at]lematindimanche.ch or on [twitter](https://twitter.com/alexhaederli)
