import requests
import re
import json
import csv
import sys
import time

url = 'https://instant.1point3acres.com/v1/coronavirus/cases/'
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
}
rows = []
"""data = requests.get(url=url + '10?country=US&lang=en', headers=headers).text
data = json.loads(data)
comment = data['comments']
links = data['links']"""


with open("test.csv", "r", encoding="utf-8") as fp:
    lines = fp.readlines()
    for line in lines[2000:4000]:
        id = line.split(',')[0]
        data = requests.get(url=url + str(id) + '?country=US&lang=en', headers=headers).text
        try:
            data = json.loads(data)
            comment = data['comments'].replace('\n','')
            links = data['links']
        except:
            comment = ""
            links = ""
        result = line.replace('\n','') + '"' + comment + '",' + str(links) + "\n"
        rows.append(result)
        print(id)
        time.sleep(2)


with open("test2.csv", "a", encoding="utf-8") as fp:
    #fp.write('id,confirmed_date,gender,people_count,die_count,state_name,county,num,age_range\n')
    for row in rows:
        fp.write(row)
        #print(row)
    print('finished!')


