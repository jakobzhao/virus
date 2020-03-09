from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime
import sqlite3
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
# browser = webdriver.Chrome("/usr/bin/chromedriver", options=options)
# browser = webdriver.Chrome("/Users/FengyuXu/Desktop/web_crawler/twitter_crawler/chromedriver", options=options)
browser = webdriver.Chrome("C:/workspace/chromedriver.exe")



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

unfolds2 = browser.find_elements_by_xpath("//div[starts-with(@class,'VirusTable')]")
for unfold in unfolds2:
    if unfold.text == "欧洲" or unfold.text == "北美洲" or unfold.text == "大洋洲" or unfold.text == "南美洲" or unfold.text == "非洲":
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
        time.sleep(3)
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
latest = {}
for row in cursor.execute("SELECT `arizona`, `illinois`, `washington`, `california`, `wisconsin`, `massachusetts`, `oregon`, `texas`, `quebec`, `ontario`, `british columbia`, `rhode island`, `florida`, `new york`, `new hampshire`, `district of columbia`, `north carolina`, `georgia usa`, `nebraska`, `new jersey`, `tennessee`, `utah`, `nevada`, `maryland`, `colorado`, `pennsylvania`, `indiana`, `minnesota` from virus order by rowid DESC limit 1"):
    latest['arizona'] = row[0]
    latest['illinois'] = row[1]
    latest['washington'] = row[2]
    latest['california'] = row[3]
    latest['wisconsin'] = row[4]
    latest['massachusetts'] = row[5]
    latest['oregon'] = row[6]
    latest['texas'] = row[7]
    latest['quebec'] = row[8]
    latest['ontario'] = row[9]
    latest['british columbia'] = row[10]
    latest['rhode island'] = row[11]
    latest['florida'] = row[12]
    latest['new york'] = row[13]
    latest['new hampshire'] = row[14]
    latest['district of columbia'] = row[15]
    latest['north carolina'] = row[16]
    latest['georgia usa'] = row[17]
    latest['nebraska'] = row[18]
    latest['new jersey'] = row[19]
    latest['tennessee'] = row[20]
    latest['utah'] = row[21]
    latest['nevada'] = row[22]
    latest['maryland'] = row[23]
    latest['colorado'] = row[24]
    latest['pennsylvania'] = row[25]
    latest['indiana'] = row[26]
    latest['minnesota'] = row[27]

# US
# https://nowcorona.com/

url = "https://nowcorona.com/"
browser.get(url)
browser.find_element_by_tag_name("main")
soup = BeautifulSoup(browser.page_source, 'html.parser')
states = soup.find("section", class_="elementor-element-fb5563c").findAll("tr")[3:]
webState = []
for state in states:
    enName = state.find("td", class_="column-1").text.lower()

    confirmed = state.find("td", class_="column-2").text
    recovered = state.find("td", class_="column-4").text
    death = state.find("td", class_="column-3").text
    if enName == 'washiongton' or "washington" in enName:
        enName = 'washington'
    if "georgia" in enName:
        enName = 'georgia usa'
    webState.append(enName)
    if enName in latest.keys():
        print(latest[enName])
        # recovered = latest[enName].split("-")[2]
        # death = latest[enName].split("-")[3]
        try:
            if int(confirmed) < int(latest[enName].split("-")[0]):
                confirmed = latest[enName].split("-")[0]
            if int(recovered) < int(latest[enName].split("-")[2]):
                recovered = latest[enName].split("-")[2]
            if int(death) < int(latest[enName].split("-")[3]):
                death = latest[enName].split("-")[3]
        except:
            confirmed = '0'
            recovered = '0'
            death = '0'
    else:
        confirmed = '0'
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

for latestState in latest:
    if latestState not in webState:
        print(latestState, latest[latestState])
        sqls += ", '" + latestState + "'"
        sqle += "'" + latest[latestState] + "', "

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
