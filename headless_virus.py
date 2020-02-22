from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime
import sqlite3
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
browser = webdriver.Chrome("/usr/bin/chromedriver", options=options)


now = str(datetime.now())
sqls = "INSERT OR REPLACE INTO virus ('datetime'"
sqle = ") VALUES ('" + now + "', "

placeName = {}
with open("assets/name.csv", "r", encoding="utf-8") as fp:
    lines = fp.readlines()
    for line in lines:
        placeItem = line.replace("\n", "").split(",")
        placeName[placeItem[0]] = placeItem[1]


# # China Provinces
#
url = "https://voice.baidu.com/act/newpneumonia/newpneumonia"
browser.get(url)


unfolds = browser.find_elements_by_xpath("//div[starts-with(@class,'Common')]")

for unfold in unfolds:
    if unfold.text == "展开全部":
        unfold.click()


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
    if (chname in placeName.keys()):
        if chname in ["美国", "泰国", "新加坡", "日本", "马来西亚", "澳大利亚", "韩国", "法国", "德国", "越南", "加拿大", "尼泊尔", "柬埔寨", "斯里兰卡", "菲律宾", "阿联酋", "英国", "印度", "俄罗斯", "意大利", "比利时", "西班牙", "瑞典", "芬兰", "埃及", "伊朗"]:
            confirmed = item.find_all("td")[1].text.strip()
            recovered = item.find_all("td")[2].text.strip()
            death = item.find_all("td")[3].text.strip()
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
        print(chname, placeName[chname], confirmed, recovered, death)
        sqls += ", '" + placeName[chname].strip() + "'"
        sqle += "'" + confirmed + "-0-" + recovered + "-" + death + "', "


# other places

conn = sqlite3.connect("assets/virus.db")
cursor = conn.cursor()
latest = {}
for row in cursor.execute("SELECT `arizona`, `illinois`, `washington`, `california`, `wisconsin`, `massachusetts`, `ontario`, `british columbia` from virus order by rowid DESC limit 1"):
    latest['arizona'] = row[0]
    latest['illinois'] = row[1]
    latest['washington'] = row[2]
    latest['california'] = row[3]
    latest['wisconsin'] = row[4]
    latest['massachusetts'] = row[5]
    latest['ontario'] = row[6]
    latest['british columbia'] = row[7]


# US
# https://www.worldometers.info/coronavirus/usa-coronavirus/

url = "https://www.worldometers.info/coronavirus/usa-coronavirus/"
browser.get(url)
browser.find_element_by_class_name('content-inner')
soup = BeautifulSoup(browser.page_source, 'html.parser')
states = soup.find_all("ul")[1].find_all("li")[1:]
for state in states:
    enName = state.text.lower().split(" ")[2]
    confirmed = state.text.lower().split(" ")[0]
    if enName in latest.keys():
        recovered = latest[enName].split("-")[2]
        death = latest[enName].split("-")[3]
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

# Canada

url = "https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html"
browser.get(url)
browser.find_element_by_css_selector('main.container')
soup = BeautifulSoup(browser.page_source, 'html.parser')
provinces = soup.find_all("table")[0].find("tbody").find_all("tr")

for province in provinces:
    enName = province.find_all("td")[0].text.lower()
    confirmed = province.find_all("td")[1].text

    if enName in latest.keys():
        recovered = latest[enName].split("-")[2]
        death = latest[enName].split("-")[3]
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

flag, priorFlag, hubei, priorHubei = "", "", "", ""
with open("assets/virus.csv", "w", encoding="utf-8") as fp:
    fp.write(str(col_name_list)[1:len(str(col_name_list))-1].replace("\'", "").replace(", ", ",").replace("(null)", "") + "\n")
    for row in cursor.execute("SELECT * from virus"):
        line = str(row)[1:len(str(row))-1].replace("\'", "").replace("None", "").replace(", ", ",").replace("(null)", "") + "\n"
        flag = line[0:10]
        hubei = line.split(",")[14]
        if flag != priorFlag:
            fp.write(str(row)[1:len(str(row)) - 1].replace("\'", "").replace("None", "").replace(", ", ",").replace("(null)", "") + "\n")
            priorFlag = flag
            priorHubei = hubei
    for row in cursor.execute("SELECT * from virus order by rowid DESC limit 1"):
        line = str(row)[1:len(str(row))-1].replace("\'", "").replace("None", "").replace(", ", ",").replace("(null)", "") + "\n"
        flag = line[0:10]
        hubei = line.split(",")[14]
        if hubei != priorHubei:
            fp.write(str(row)[1:len(str(row)) - 1].replace("\'", "").replace("None", "").replace(", ", ",").replace("(null)", "") + "\n")

conn.close()


fp = open("assets/virus.csv", "r", encoding="utf-8")
lines = fp.readlines()
fp.close()
n = len(lines)
if lines[n-1][0:10] == lines[n-2][0:10]:
    lines.pop(n-2)
pass
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
