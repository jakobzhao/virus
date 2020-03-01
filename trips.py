import shutil
import urllib.request
import json
import datetime

ts = str(datetime.datetime.now().timestamp()).split(".")[0]
urllink = "https://hhyfeed.sogoucdn.com/js/common/epidemic-search/main_2020030110.js"
id = 0
with urllib.request.urlopen(urllink) as url:
    content = url.read()
    trips = json.loads(content.decode())
    with open("assets/trips-" + ts + ".json", "w+", encoding="utf-8") as fp:
        fp.write(str(trips))
    with open("assets/trips-" + ts + ".csv", "w+", encoding="utf-8") as fp:
        fp.write("id,from,to,flight,time,flat,flng,tlat,tlng,source\n")
        for trip in trips:
            if trip["trafficType"] == '航班':
                time = trip['trafficTime']
                source = trip['evidenceDocUrl']
                flight = trip['trafficNum']
                fromLoc = json.loads(trip['startEndStation'])[0]
                toLoc = json.loads(trip['startEndStation'])[1]
                fp.write("%d,%s,%s,%s,%s,%s\n" % (id, flight, time, fromLoc, toLoc, source))
                print(id, time, flight, fromLoc, toLoc, source)
                id += 1
    shutil.copyfile("assets/trips-" + ts + ".csv", "assets/trips.csv")
    shutil.copyfile("assets/trips-" + ts + ".json", "assets/trips.json")
print("finished!")


