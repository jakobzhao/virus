from selenium import webdriver
from bs4 import BeautifulSoup
import time
import geocoder
from datetime import datetime
import shutil

fp = open("assets/orig-cases.csv", "r", encoding="utf-8")
lines = fp.readlines()
fp.close()
n = len(lines)


id = 0
outputs = []
for line in lines[1:]:
    no = line.split(",")[0]
    date = line.split(",")[1]
    state =  line.split(",")[2]
    county = line.split(",")[3]
    try:
        note = line.split(",")[4].replace("\n", " ").replace("\r", " ").replace("\t", " ").replace('"', '').replace('"', '').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').strip()
    except:
        note = ""
    try:
        reference = line.split(",")[5].strip()
    except:
        reference = ""

    try:
        g = geocoder.arcgis(county + " county, " + state + ", U.S.A.")
        lat = g.current_result.lat
        lng = g.current_result.lng
    except:
        lat = 0
        lng = 0
    # time.sleep(1)
    id += 1
    print(no, date, county, state, lat, lng, note, reference)
    output = '%d,"%s","%s","%s","%s",%f,%f,"%s","%s"\n' % (id, no, date, county, state, lng, lat, note, reference)
    outputs.append(output)


with open("assets/cases.csv", "w", encoding="utf-8") as fp:
    fp.write("id,no,date,county,state,lng,lat,note,reference\n")
    for output in outputs:
        fp.write(output)


ts = str(datetime.now().timestamp()).split(".")[0]
shutil.copyfile("assets/cases.csv", "assets/cases-" + ts + ".csv")
print("finished!")
