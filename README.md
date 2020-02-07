# 2019 Coronavirus Map

This repository stores the source code of the Noval Coronavirous Map (https://hgis.uw.edu/virus). This map is made by the [Humanistic GIS Lab](https://hgis.uw.edu) at [University of Washington – Seattle](https://www.uw.edu). The virus trend dataset are collected from multiple official data sources, and we also try to make timely update to display the latest updates. 



interactive map was built upon opensource libraries and collecte

# Data Sources:
a)	National Health Commission (NHC) of the People’s Republic of China;
b)	China’s Provincial & Municipal Health Commission;
c)	China’s Provincial & Municipal government database;
d)	Public data published from Hongkong, Macau and Taiwan official channels;
e)	WHO, CDC, PHA, China NHC and Baidu
a)	China’s data is updated from NHC every day before 3:00 PM EST (providential data is not up to date until later in the day, China’s national data might occur to be greater than the sum of providential data); Global data is updated from World Health Organization (WHO); USA data is updated from CDC
## 	Principals & Data Update:
b)	Data will be updated Every 4 hours; Data is verified daily;
c)	Due to data-calculation verification, live update of national and provincial data will experience a slight delay compared to data from official sites.
d)	China’s data is updated to provincial & municipal scale
e)	Data concerning USA and Canada will be specified to provincial & Municipal level soon
## 	Functions:
a)	Interactive web-based map, clicking on countries will present the respective country’s national epidemic data;
b)	Clicking on provinces in China will present the respective province’s epidemic data;
c)	Dot chart tracks the data changes since January 21st;
4.	Website can be accessed via:  http://hgis.uw.edu/virus/assets/virus.db
5.	Data are manipulated via Sqlite, data is represented by a 4-sequel entry divided by dashes, the first sequel represents number of confirmed cases, the second sequel represents suspected cases, the third sequel represents cured cases, the fourth sequel represents death cases

Made by
Platform is created by Leaflet, D3, C3, bootstrap, and chroma.
The Server is provided by UW’s Center for Studies in Demography and Ecology
Team members: Bo Zhao, Cindy Xu, Lola , Joshua Ji, Steven
