# Dhaka Air Quality

This project aims to explore the air quality data for Bangladesh. It uses two datasets, a higher resolution dataset for Dhaka city, taken every hour at the US Embassy, Dhaka and a once-a-day resolution dataset for several cities published by the Bangladeshi government. 

_Note: This project is still in development._

<h2> Dhaka data </h2>
The data for Dhaka is collected from the US Embassy in Dhaka, which records hourly air quality measurements using a monitor on their roof. Their instrument measures the average concentration of fine particle pollutants (PM2.5) in the air over an hour and converts this into an Air Quality Index (AQI) value. AQI is a numerical scale, between 0 and 500, informing how potentially dangerous the air is to health, where small numbers are good and large numbers are bad.

The recognised acceptable standard for AQI is up to 100, once the quality of air degrades to an AQI above 100, sensitive groups of people may experience adverse health effects. AQI values above 150 are considered "unhealthy", meaning everyone begins to be at risk of adverse health issues, the severity of which increases as the AQI gets larger -- with air deemed "very unhealthy" at AQI in excess of 200 and "extremely unhealthy" above 300.

I have explored daily and seasonal variations in the data and created visualisations.

**Seasonal variations:**

![image](https://user-images.githubusercontent.com/62939263/120923349-e831e700-c6ef-11eb-8a7e-5607d3b7a580.png)

**Aggregated hourly varaitions:**

![image](https://user-images.githubusercontent.com/62939263/120923560-09df9e00-c6f1-11eb-8628-4aeeee03dcfc.png)


**Aggregated monthly varaitions:**

![image](https://user-images.githubusercontent.com/62939263/120923547-fb918200-c6f0-11eb-8304-fb9b9b3e7dca.png)

**Variations across the day throughout the year:**

![image](https://user-images.githubusercontent.com/62939263/120923188-0cd98f00-c6ef-11eb-9f41-98bbc84f942d.png)

For more details see my project page [here](https://tsgreen.github.io/dataproject_airquality.html).

A write up of this data up to February 2020 was published in a leading Bangladeshi newspaper: [The Daily Star](https://www.thedailystar.net/opinion/environment/news/breath-not-so-fresh-air-1870759)
![image](https://user-images.githubusercontent.com/62939263/120923626-6773ea80-c6f1-11eb-96a7-612595e87d7f.png)

# Expansion 

I am currently working on analysis of air quality in several other Bangladeshi cities, scrapped from the Bangladeshi government's [Clean Air and Sustainable Environment (CASE)](http://case.doe.gov.bd/index.php?option=com_content&view=article&id=9&Itemid=31) project. This data is much less complete than the US Embassy data and only has one daily recording. 

**Coming soon!** A web-app data dashboard showing all these data.

# Data Structure
```
├── data 
│   ├── bronze                
│   |    ├── case             <- Nationwide data from CASE project of BD Gov.
│   |    └── us_embassy       <- Dhaka data from US Consulate.
│   └── silver                                          
│        ├── case             <- Nationwide data from CASE project of BD Gov.
│        └── us_embassy       <- Dhaka data from US Consulate.
```
