from selenium import webdriver
from bs4 import BeautifulSoup
import time
import geocoder
from datetime import datetime

now = str(datetime.now())

#browser = webdriver.Chrome("/Users/FengyuXu/Desktop/web_crawler/twitter_crawler/chromedriver") #fengyu's chromefrive location
#browser = webdriver.Chrome("C:\Workspace\chromedriver.exe") # zhaobo's chromedrive location'
browser = webdriver.Chrome("E:\chromedriver_win32\chromedriver.exe")

# US individual cases
# "https://nowcorona.com/coronavirus-us-situation-summary/"
id = 0
outputs = []
toEnd = False
url = "https://coronavirus.1point3acres.com/en?fbclid=IwAR1wDNOOEnTqMh5SbX2zXWH2n8hBcEMiDOCaXA_VaFWulMzMB18gwn9z_AQ"
browser.get(url)

while toEnd != True:

button = browser.find_element_by_xpath('//*[@id="map"]/div[3]/div[1]/div[3]/div/div/ul/li[9]/a')
time.sleep(2)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight*2/5);")
time.sleep(2)
button.click()



def content():
    browser.find_element_by_name("body")
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    cases = soup.find("table").find_all("tr")[1:]
    for case in cases:
        iftype = "Confirmed"
        data = case.find_all("td")
        date = data[1].text
        loc = data[2].text
        info = data[3].text
        source = "<a target ='_blank' href='" + str(data[7].find('a').get('href')) + "'>" + str(data[7].text) + "</a>"
        print(id, iftype, date, info, loc, source)
        if "recovered" in data[6].text.lower():
            iftype = "Recovered"

        try:
            g = geocoder.arcgis(loc)
            lat = g.current_result.lat
            lng = g.current_result.lng
        except:
            lat = 0
            lng = 0
        time.sleep(1)
        id += 1
        print(id, iftype, date, info, loc, source)
        #output = '%d,"%s",%f,%f,"%s","%s","%s","%s"\n' % (id, iftype, lng, lat, date, info, loc, source)
        #outputs.append(output)


with open("assets/cases-20200309.csv", "w", encoding="utf-8") as fp:
    fp.write("id,iftype,lng,lat,date,info,loc,source\n")
    for output in outputs:
        fp.write(output)

print("finished!")
