# Dhaka Air Quality

This project aims to analyse the air quality data for Dhaka city since 2016.

The data is collected from the US Embassy in Dhaka, which records hourly air quality measurements using a monitor on their roof. Their instrument measures the average concentration of fine particle pollutants (PM2.5) in the air over an hour and converts this into an Air Quality Index (AQI) value. AQI is a numerical scale, between 0 and 500, informing how potentially dangerous the air is to health, where small numbers are good and large numbers are bad.

The recognised acceptable standard for AQI is up to 100, once the quality of air degrades to an AQI above 100, sensitive groups of people may experience adverse health effects. AQI values above 150 are considered "unhealthy", meaning everyone begins to be at risk of adverse health issues, the severity of which increases as the AQI gets larger -- with air deemed "very unhealthy" at AQI in excess of 200 and "extremely unhealthy" above 300.

I have explored daily and seasonal variations in the data and created visualisations.

Seasonal variations in Dhaka:
![image](https://user-images.githubusercontent.com/62939263/120641280-3ac39700-c495-11eb-8462-33d59e877b83.png)

Aggregated hourly varaitions:
![image](https://user-images.githubusercontent.com/62939263/120641548-88d89a80-c495-11eb-8406-e67c309c8e01.png)

For more details see my project page [here](https://tsgreen.github.io/dataproject_airquality.html).

A write up of this data was published in a leading Bangladeshi newspaper: [The Daily Star](https://www.thedailystar.net/opinion/environment/news/breath-not-so-fresh-air-1870759)

<h2> Expansion</h2> 
Currently working on analysis of air quality in several other Bangladeshi cities, scrapped from the Bangladeshi government's [Clean Air and Sustainable Environment (CASE)](http://case.doe.gov.bd/index.php?option=com_content&view=article&id=9&Itemid=31) project. This data is much less complete than the US Embassy data for Dhaka, and only has one daily recording. 

Combing soon! A web-app data dashboard showing all these data.

# Project Structure

*Dhaka data from US Embassy:* Two notebooks,
1) Pre-processing: Imports and cleans the raw dataset and exports cleaned csv file.
2) Analysis and Visualisation: Imports clean dataset and does the analysis of the data and creates the visuals.

And a script to download the csv data files.

*CASE nationwide data:* Two notebooks,
1) Pre-processing: Imports and cleans the raw dataset and exports cleaned csv file.
2) Analysis and Visualisation: Imports clean dataset and does the analysis of the data and creates the visuals.

And a script to scrape the data from the HTML format [data archive](http://case.doe.gov.bd/index.php?option=com_content&view=category&id=8&Itemid=32).
