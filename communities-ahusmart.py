import shutil
import urllib.request
import json
import datetime

ts = str(datetime.datetime.now().timestamp()).split(".")[0]
urllink = "https://lab.ahusmart.com/nCoV/api/detail"
id = 0
with urllib.request.urlopen(urllink) as url:
    content = url.read()
    cases = json.loads(content.decode())
    with open("assets/communities-" + ts + ".json", "w+", encoding="utf-8") as fp:
        fp.write(str(cases['results']))
    with open("assets/communities-" + ts + ".csv", "w+", encoding="utf-8") as fp:
        fp.write("id,name,time,lat,lng\n")
        for case in cases['results']:
            name = case['detail']
            # province = case['province']
            city = case['city']
            time = case['updateTime']
            source = case['infoSource']
            url = case['sourceUrl']
            lat = case['position'][1]
            lng = case['position'][0]

            fp.write("%d,%s,%d,%f,%f\n" % (id, name, time, lat, lng))
            print(id, name, time, lat, lng, city, source, url)
            id += 1
    shutil.copyfile("assets/communities-" + ts + ".csv", "assets/communities.csv")
    shutil.copyfile("assets/communities-" + ts + ".json", "assets/communities.json")
print("finished!")
