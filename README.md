# Swiss Administration Procurements 

## Description
This repo describe the data handling and methodology behind the Swiss federal administration procurements project. The project was published in English, German and French by swiss newspapers *Le Matin Dimanche* and *SonntagsZeitung*.

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

At this stage we have one CSV for each department and each year for the [40 biggest suppliers](csv/biggest) and the same for the [overall by-category](csv/categories) data.

## Python script
- Combine
- CSV master short
- Uniforming the suppliers' name
- CSV analysis

## Last caveat: undisclosed categories
The last department to send us the data was the Department of Defense. And for security reasons, they don't want to disclose in which of the 22 categories their suppliers are active. We added a category with 0 as id. The problem was  that these amounts were not subtracted in the python script and were counted twice in the visualization. We solved that with a tweak in the visualization so that this category is not counted in the "Main category" chart.

## Get in touch
You can contact us here: alexandre.haederli[at]lematindimanche.ch or on [twitter](https://twitter.com/alexhaederli)
