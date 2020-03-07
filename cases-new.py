from selenium import webdriver
from bs4 import BeautifulSoup
import time
import geocoder
from datetime import datetime

now = str(datetime.now())

#browser = webdriver.Chrome("/Users/FengyuXu/Desktop/web_crawler/twitter_crawler/chromedriver") #fengyu's chromefrive location
browser = webdriver.Chrome("C:\Workspace\chromedriver.exe") # zhaobo's chromedrive location'

# US individual cases
# "https://coronavirus.1point3acres.com/en"

url = "https://coronavirus.1point3acres.com/en"
browser.get(url)
i = 0
while i < 20:
    browser.find_element_by_css_selector("html")
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    cases = soup.findAll("table")[0].findAll("tr")[1:]
    preCid = 0
    for case in cases:
        cid = case.findAll("td")[0].text
        if preCid != cid:
            print(cid)
            preCid = cid
        else:
            print("finished!")
            break
    # time.sleep(1)
    #nextpage_button = browser.find_elements_by_css_selector("ul.ant-pagination")[0].find_elements_by_css_selector("a.ant-pagination-item-link")[2]

    #nextpage_button = browser.find_element_by_xpath('// *[ @ id = "map"] / div[3] / div[1] / div[3] / div / div / ul / li[9] / a')

    nextpage_button = browser.find_element_by_xpath('//*[@id="map"]/div[3]/div[1]/div[3]/div/div/ul/li[9]/a')
    time.sleep(2)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight*2/5);")
    time.sleep(2)
    nextpage_button.click()
    i += 1

exit(-1)
browser.find_element_by_tag_name("main")
soup = BeautifulSoup(browser.page_source, 'html.parser')
cases = soup.find("table", class_="tablepress-id-4").findAll("tr")
id = 0
outputs = []
for case in cases:
    iftype = "Confirmed"
    if "recovered" in case.find("td", class_="column-1").text.lower():
        iftype = "Recovered"
    elif "death" in case.find("td", class_="column-1").text.lower():
        iftype = "Death"
    else:
        iftype= "Confirmed"

    date = case.find("td", class_="column-2").text
    info = case.find("td", class_="column-3").text
    loc = case.find("td", class_="column-4").text
    source = case.find("td", class_="column-5").text
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
    output = '%d,"%s",%f,%f,"%s","%s","%s","%s"\n' % (id, iftype, lng, lat, date, info, loc, source)
    outputs.append(output)


with open("assets/cases.csv", "w", encoding="utf-8") as fp:
    fp.write("id,iftype,lng,lat,date,info,loc,source\n")
    for output in outputs:
        fp.write(output)

print("finished!")
