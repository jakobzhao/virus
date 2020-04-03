from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from datetime import datetime
from urllib.request import urlopen
import time
import sqlite3
import urllib
import requests

#browser = webdriver.Chrome("/Users/FengyuXu/Desktop/web_crawler/twitter_crawler/chromedriver")
#browser = webdriver.Chrome("/Users/joshuaji/Desktop/chromedriver") #joshua's chromedrive location
#browser = webdriver.Chrome("C:/workspace/chromedriver.exe")
#browser = webdriver.Chrome("E:/dev/workspaces/chromedriver.exe")
browser = webdriver.Chrome("/Users/stevenbao/dev/chromedriver")

# Variable Preparation
now = str(datetime.now())
sqls = "INSERT OR REPLACE INTO virus ('datetime'"
sqle = ") VALUES ('" + now + "', "

chineseCity = {}
with open("assets/name.csv", "r", encoding="utf-8") as fp:
    lines = fp.readlines()
    for line in lines:
        placeItem = line.replace("\n", "").split(",")
        chineseCity[placeItem[0]] = placeItem[1]

canadacities = []
with open("assets/canada-city.txt", "r", encoding="utf-8") as fp:
    states = fp.readlines()
    for state in states:
        canadacities.append(state.replace("\n","").lower())

# Chinese Provinces
url = "https://voice.baidu.com/act/newpneumonia/newpneumonia"
browser.get(url)

unfolds = browser.find_elements_by_xpath("//div[starts-with(@class,'Common')]")
for unfold in unfolds:
    if unfold.text == "展开全部":
        unfold.click()
        time.sleep(2)
        break

browser.find_element_by_xpath("//table[starts-with(@class,'VirusTable')]").find_elements_by_tag_name("tr")
soup = BeautifulSoup(browser.page_source, 'html.parser')

time.sleep(4)

items = soup.find_all("tr")

for item in items[1:35]:
    chname = ""
    confirmed, recovered, death = 0, 0, 0,
    try:
        chname = item.find_all("td")[0].text
    except:
        pass

    if chname in chineseCity.keys():
        confirmed = item.find_all("td")[3].text.strip()
        recovered = item.find_all("td")[4].text.strip()
        death = item.find_all("td")[5].text.strip()

    if recovered == "" or recovered == "-":
        recovered = "0"
    if death == "" or death == "-":
        death = "0"
    if confirmed == "" or confirmed == "-" :
        confirmed = "0"

    print(chname, chineseCity[chname], confirmed, recovered, death)
    sqls += ", '" + chineseCity[chname].strip() + "'"
    sqle += "'" + confirmed + "-0-" + recovered + "-" + death + "', "

# Countries
url = "https://en.wikipedia.org/wiki/Template:2019%E2%80%9320_coronavirus_pandemic_data"

soup = BeautifulSoup(urlopen(url), "html.parser")
table = soup.find("tbody")
items = table.find_all("tr")
for item in items[2:]:
    name, confirmed, recovered, death = "", "", "", ""
    try:
        name = item.find_all("th")[1].text.split("[")[0].split("\n")[0].lower().strip()
    except IndexError:
        break

    if name == "hong kong":
        continue

    if name == "usa":
        name = 'united states'
        continue

    if name =="swaziland":
        name = 'eswatini'
        continue

    if name =="saint vincent and the grenadines":
        name ='st. vincent and the grenadines'
        continue

    if name == "china (mainland)":
        name = 'china'
        continue

    confirmed = item.find_all("td")[0].text.split("\n")[0].replace(",","")
    death = item.find_all("td")[1].text.split("\n")[0].replace(",", "")
    recovered = item.find_all("td")[2].text.split("\n")[0].replace(",", "")
    if recovered == "–":
        recovered = "0"


    print(name, confirmed, death, recovered)

    sqls += ", '" + name.replace("'", "''") + "'"
    sqle += "'" + confirmed + "-0-" + recovered + "-" + death + "', "

# U.S. States
conn = sqlite3.connect("assets/virus.db")
cursor = conn.cursor()

urllink = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdW9DsR5iffFcJvKAJXyOiNn4IYtavRIGslkcJIslHJC7UfrbChv-L4E89TeDEcWZS6QSzCuHWeMON/pub?gid=1879451031&single=true&output=csv"
with urllib.request.urlopen(urllink) as url:
    content = url.read().decode()
    content.replace("/r/n","")
    states = content.split("\r\n")[1:None]
    for state in states:
        data = state.split(",")
        name = data[0].lower()
        if name == 'georgia':
            name = 'georgia usa'
        cases = data[3] + "-0-" + data[5] + "-" + data[4]
        sqls += ", '" + name + "'"
        sqle += "'" + cases + "', "
        print(name + " " + cases)



# Canadian Provinces
url = "https://health-infobase.canada.ca/covid-19/iframe/table.html"
browser.get(url)
time.sleep(2)
soup = BeautifulSoup(browser.page_source, 'html.parser')
provinces = soup.find("tbody").find_all("tr")

for province in provinces[1:-1]:
    # enName = province.find_all("td")[0].text.lower().replace("british colombia", "british columbia")
    enName = province.find_all("td")[0].text.lower().replace("    ", " ")
    # print (province.text)
    confirmed = province.find_all("td")[1].text.replace(",","")
    death = province.find_all("td")[3].text.replace(",","")

    if enName in canadacities:
        for row in cursor.execute("SELECT `" + enName + "` from virus order by rowid DESC limit 1"):
            latest = row[0]
        # recovered = latest.split("-")[2]
        # death = latest.split("-")[3]
    else:
        recovered = '0'

    if recovered == "" or recovered == "-":
        recovered = "0"
    if death == "" or death == "-":
        death = "0"
    if confirmed == "" or confirmed == "-":
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


flag, confirmed, priorConfirmed = "", 0, 0
prior_row = str(list(cursor.execute("SELECT * FROM virus WHERE rowid = 1")))
prior_row = prior_row[2:(len(prior_row)-5)]
priorFlag = prior_row[1:11]

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
            fp.write(str(prior_row)[1:len(str(prior_row)) - 1].replace("\'", "").replace("None", "").replace(", ", ",").replace("(null)", "") + "\n")
            priorFlag = flag
            priorConfirmed = confirmed
        prior_row = row

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

# exit(-1)
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
