from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime
from urllib import request
import sqlite3
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
browser = webdriver.Chrome("/usr/bin/chromedriver", options=options)
#browser = webdriver.Chrome("/Users/FengyuXu/Desktop/web_crawler/twitter_crawler/chromedriver", options=options)


now = str(datetime.now())
sqls = "INSERT OR REPLACE INTO virus ('datetime'"
sqle = ") VALUES ('" + now + "', "

placeName = {}
with open("assets/country_name.csv", "r", encoding="utf-8") as fp:
    lines = fp.readlines()
    for line in lines:
        placeItem = line.replace("\n", "").split(",")
        placeName[placeItem[0]] = placeItem[1]

chineseCity = {}
with open("assets/name.csv", "r", encoding="utf-8") as fp:
    lines = fp.readlines()
    for line in lines:
        placeItem = line.replace("\n", "").split(",")
        chineseCity[placeItem[0]] = placeItem[1]

oldCity = {}
with open("assets/old_name.csv", "r", encoding="utf-8") as fp:
    lines = fp.readlines()
    for line in lines:
        placeItem = line.replace("\n", "").split(",")
        oldCity[placeItem[0]] = placeItem[1]

unitedStates = []
with open("assets/unitedStates.txt", "r", encoding="utf-8") as fp:
    states = fp.readlines()
    for state in states:
        unitedStates.append(state.replace("\n","").lower())

canadacities = []
with open("assets/canada_city.txt", "r", encoding="utf-8") as fp:
    states = fp.readlines()
    for state in states:
        canadacities.append(state.replace("\n","").lower())

"""for city in placeName.values():
    if city not in oldCity.values():
        cursor.execute("ALTER TABLE virus ADD [" + city + "] CHAR(20);")"""


# browser = webdriver.Chrome("/Users/FengyuXu/Desktop/web_crawler/twitter_crawler/chromedriver") #fengyu's chromefrive location
#browser = webdriver.Chrome("C:\Workspace\chromedriver.exe") # zhaobo's chromedrive location'


# # China Provinces
#
url = "https://voice.baidu.com/act/newpneumonia/newpneumonia"
browser.get(url)


unfolds = browser.find_elements_by_xpath("//div[starts-with(@class,'Common')]")
for unfold in unfolds:
    if unfold.text == "展开全部":
        unfold.click()
        time.sleep(2)

unfolds2 = browser.find_elements_by_xpath('//*[@id="foreignTable"]/table/tbody/tr')
for unfold in unfolds2[1:]:
    if "欧洲" in unfold.text or "亚洲" in unfold.text or "北美洲" in unfold.text or "大洋洲" in unfold.text  or "南美洲" in unfold.text or "非洲" in unfold.text:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
        unfold.find_element_by_css_selector("div").click()
        time.sleep(2)



browser.find_element_by_xpath("//table[starts-with(@class,'VirusTable')]").find_elements_by_tag_name("tr")
soup = BeautifulSoup(browser.page_source, 'html.parser')

time.sleep(4)


items = soup.find_all("tr")
for item in items:
    chname = ""
    confirmed, recovered, death = 0, 0, 0,
    try:
        chname = item.find_all("td")[0].text
    except:
        pass

    if (chname in placeName.keys()) and chname != "中国":
        if chname not in chineseCity.keys():
            confirmed = item.find_all("td")[2].text.strip()
            recovered = item.find_all("td")[3].text.strip()
            death = item.find_all("td")[4].text.strip()
        else:
            confirmed = item.find_all("td")[2].text.strip()
            recovered = item.find_all("td")[3].text.strip()
            death = item.find_all("td")[4].text.strip()

        if recovered == "" or recovered == "-":
            recovered = "0"
        if death == "" or death == "-":
            death = "0"
        if confirmed == "" or confirmed == "-" :
            confirmed = "0"
        # if chname in chineseCity.keys():
        #     confirmed = str(int(confirmed) + int(recovered) + int(death))
        print(chname, placeName[chname], confirmed, recovered, death)
        sqls += ", '" + placeName[chname].strip() + "'"
        sqle += "'" + confirmed + "-0-" + recovered + "-" + death + "', "


# other places

conn = sqlite3.connect("assets/virus.db")
cursor = conn.cursor()


urllink = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdW9DsR5iffFcJvKAJXyOiNn4IYtavRIGslkcJIslHJC7UfrbChv-L4E89TeDEcWZS6QSzCuHWeMON/pub?gid=1879451031&single=true&output=csv"
with urllib.request.urlopen(urllink) as url:
    content = url.read().decode()
    content.replace("/r/n","")
    states = content.split("\r\n")[1:]
    for state in states:
        data = state.split(",")
        name = data[0].lower()
        if name == 'georgia':
            name = 'georgia usa'
        cases = data[3] + "-0-" + data[5] + "-" + data[4]
        sqls += ", '" + name + "'"
        sqle += "'" + cases + "', "
        print(name + " " + cases)

# Canada

url = "https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html"
browser.get(url)
browser.find_element_by_css_selector('main.container')
soup = BeautifulSoup(browser.page_source, 'html.parser')
provinces = soup.find_all("table")[0].find("tbody").find_all("tr")

for province in provinces[:-1]:
    enName = province.find_all("td")[0].text.lower().replace("british colombia", "british columbia")
    confirmed = province.find_all("td")[1].text

    if enName in canadacities:
        for row in cursor.execute("SELECT `" + enName + "` from virus order by rowid DESC limit 1"):
            latest = row[0]
        recovered = latest.split("-")[2]
        death = latest.split("-")[3]
    else:
        recovered = '0'
        death = '0'

    if recovered == "" or recovered == "-":
        recovered = "0"
    if death == "" or death == "-":
        death = "0"
    if confirmed == "" or confirmed == "-" :
        confirmed = "0"
    print(enName, confirmed, recovered, death)
    sqls += ", '" + enName.strip() + "'"
    sqle += "'" + confirmed + "-0-" + recovered + "-" + death + "', "


browser.close()



insert_record_sql = sqls + sqle[0: len(sqle) -2] + ")"

cursor.execute(insert_record_sql)
conn.commit()
cursor.execute("SELECT * from virus")
col_name_list = [tuple[0] for tuple in cursor.description]


flag, priorFlag, confirmed, priorConfirmed = "", "", 0, 0
with open("assets/virus.csv", "w", encoding="utf-8") as fp:
    fp.write(str(col_name_list)[1:len(str(col_name_list))-1].replace("\'", "").replace(", ", ",").replace("(null)", "") + "\n")
    for row in cursor.execute("SELECT * from virus"):
        line = str(row)[1:len(str(row))-1].replace("\'", "").replace("None", "").replace(", ", ",").replace("(null)", "") + "\n"
        flag = line[0:10]
        for area in line.split(",")[1:]:
            if area == "" or area == "(null)" or area == "None" or area == "\n":
                area = 0
            else:
                area = int(area.split("-")[0])
            confirmed += area

        if flag != priorFlag:
            fp.write(str(row)[1:len(str(row)) - 1].replace("\'", "").replace("None", "").replace(", ", ",").replace("(null)", "") + "\n")
            priorFlag = flag
            priorConfirmed = confirmed
    for row in cursor.execute("SELECT * from virus order by rowid DESC limit 1"):
        line = str(row)[1:len(str(row))-1].replace("\'", "").replace("None", "").replace(", ", ",").replace("(null)", "") + "\n"
        flag = line[0:10]
        for area in line.split(",")[1:]:
            if area == "" or area == "(null)" or area == "None" or area == "\n":
                area = 0
            else:
                area = int(area.split("-")[0])
            confirmed += area
        if confirmed != priorConfirmed:
            fp.write(str(row)[1:len(str(row)) - 1].replace("\'", "").replace("None", "").replace(", ", ",").replace("(null)", "") + "\n")

conn.close()

exit(-1)
fp = open("assets/virus.csv", "r", encoding="utf-8")
lines = fp.readlines()
fp.close()
n = len(lines)
if lines[n-1][0:10] == lines[n-2][0:10]:
    lines.pop(n-2)

with open("assets/virus.csv", "w", encoding="utf-8") as fp:
    start = 10
    stop = 26
    id = 0
    for line in lines:
        if id !=0:
            fp.write(line[0: 10:] + line[26::])
        else:
            fp.write(line)
        id += 1


with open("assets/timestamp.txt", "w", encoding="utf-8") as fp:
    fp.write("timestamp\n")
    fp.write(now)

print("finished!")