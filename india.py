from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime
import sqlite3
from selenium.webdriver.chrome.options import Options
import urllib.request
# import shutil
from selenium.webdriver.common.action_chains import ActionChains

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
# browser = webdriver.Chrome("/usr/bin/chromedriver", options=options)
browser = webdriver.Chrome("/Users/FengyuXu/Desktop/web_crawler/twitter_crawler/chromedriver")
# browser = webdriver.Chrome("C:/workspace/chromedriver.exe")
# browser = webdriver.Chrome("E:\chromedriver_win32\chromedriver.exe")

now = str(datetime.now())
sqls = "INSERT OR REPLACE INTO virus ('datetime'"
sqle = ") VALUES ('" + now + "', "

"""for city in placeName.values():
    if city not in oldCity.values():
        cursor.execute("ALTER TABLE virus ADD [" + city + "] CHAR(20);")"""

citynames = []
# browser = webdriver.Chrome("/Users/FengyuXu/Desktop/web_crawler/twitter_crawler/chromedriver") #fengyu's chromefrive location
#browser = webdriver.Chrome("C:\Workspace\chromedriver.exe") # zhaobo's chromedrive location'


# # China Provinces
#
url = "https://www.mohfw.gov.in"
browser.get(url)

table = browser.find_element_by_tag_name("table")
soup = BeautifulSoup(browser.page_source, 'html.parser')
items = soup.find_all("tr")[1:-1]
for item in items:
    data = item.find_all("td")
    name = data[1].text.lower()
    if name == "union territory of ladakh":
        kconfirmed = int(data[2].text) + int(data[3].text)
        krecovered = int(data[4].text)
        kdeath = int(data[5].text)
    elif name == "union territory of jammu and kashmir":
        kname = "jammu and kashmir"
        kconfirmed += int(data[2].text) + int(data[3].text)
        krecovered += int(data[4].text)
        kdeath += int(data[5].text)
        citynames.append(kname)
        print(kname, str(kconfirmed), str(krecovered), str(kdeath))
        sqls += ", '" + kname + "'"
        sqle += "'" + str(kconfirmed) + "-0-" + str(krecovered) + "-" + str(kdeath) + "', "
    else:
        confirmed = int(data[2].text) + int(data[3].text)
        recovered = data[4].text
        death = data[5].text
        citynames.append(name)
        print(name,confirmed,recovered,death)
        sqls += ", '" + name + "'"
        sqle += "'" + str(confirmed) + "-0-" + recovered + "-" + death + "', "

conn = sqlite3.connect("assets/virus.db")
cursor = conn.cursor()

for name in citynames:
    cursor.execute("ALTER TABLE virus ADD [" + name + "] CHAR(20);")

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
