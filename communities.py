import shutil
import urllib.request
import json

urllink = "https://oss.mapmiao.com/others/ncov/data.json"
id = 0
with urllib.request.urlopen(urllink) as url:
    content = url.read()
    cities = json.loads(content.decode())
    with open("assets/communities-" + cities[0]['updated_at'].replace(" ", "_").replace("/", "").replace(":", "") + ".json", "w+", encoding="utf-8") as fp:
        fp.write(str(cities))
    with open("assets/communities-" + cities[0]['updated_at'].replace(" ", "_").replace("/", "").replace(":", "") + ".csv", "w+", encoding="utf-8") as fp:
        fp.write("id,name,datetime,updated_date,lat,lng,city,province\n")
        for city in cities:
            name = city['name']
            province = city['province']
            datetime = city['updated_at']
            communities = city['pois']
            for com in communities:
                comName = com['name']
                comDate = com['date']
                comLat = com['point']['coordinates'][1]
                comLng = com['point']['coordinates'][0]
                fp.write("%d,%s,%s,%s,%f,%f,%s,%s\n" % (id, comName, datetime, comDate, comLat, comLng, name, province))
                print(id, name, province, datetime, comName, comDate, comLat, comLng)
                id += 1
    shutil.copyfile("assets/communities-" + cities[0]['updated_at'].replace(" ", "_").replace("/", "").replace(":", "") + ".csv", "assets/communities.csv")
    shutil.copyfile("assets/communities-" + cities[0]['updated_at'].replace(" ", "_").replace("/", "").replace(":", "") + ".json", "assets/communities.json")
print("finished!")
