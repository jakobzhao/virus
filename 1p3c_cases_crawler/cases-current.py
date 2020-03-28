import requests
import re
import json
import os
import csv

url = 'https://coronavirus.1point3acres.com'
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
}

html_txt = requests.get(url=url, headers=headers).text
confirmed_data = "{}"
deaths_data = "{}"

js_files = re.findall(r'chunks[^"]+\.js', html_txt)

for js_file in set(js_files):
    curr_html_txt = requests.get(url=url + '/_next/static/' + js_file,
                                 headers=headers).text
    txt_splitted = curr_html_txt.split("JSON.parse('")
    for txt in txt_splitted:
        data = txt.split("')}")[0]
        """if ('people_count' in data and '"confirmed_date":"1/21"' in data):
            confirmed_data = data"""
        if ('"die_count"' in data and '"confirmed_date":"2/28"' in data):
            deaths_data = data

#confirmed_data = confirmed_data.encode().decode('unicode_escape')
#confirmed_data = json.loads(confirmed_data)

deaths_data = deaths_data.encode().decode('unicode_escape')
deaths_data = json.loads(deaths_data)

# check
#test = next((x for x in confirmed_data if x["confirmed_date"] == "1/21"), None)
#if test is None:
    #print('Data crawled from 1P3A are not valid!')
    #exit(1)

"""confirmed_data = json.dumps(
    confirmed_data,
    indent=2,
    ensure_ascii=False,
)"""

deaths_data = json.dumps(
    deaths_data,
    indent=2,
    ensure_ascii=False,
)

o = json.loads(deaths_data)

def loop_data(o, k=''):
    global json_ob, c_line
    if isinstance(o, dict):
        for key, value in o.items():
            if(k==''):
                loop_data(value, key)
            else:
                loop_data(value, k + '.' + key)
    elif isinstance(o, list):
        for ov in o:
            loop_data(ov, k)
    else:
        if not k in json_ob:
            json_ob[k]={}
        json_ob[k][c_line]=o


def get_title_rows(json_ob):
    title = []
    row_num = 0
    rows=[]
    for key in json_ob:
        title.append(key)
        v = json_ob[key]
        if len(v)>row_num:
            row_num = len(v)
        continue
    for i in range(row_num):
        row = {}
        for k in json_ob:
            v = json_ob[k]
            if i in v.keys():
                row[k]=v[i]
            else:
                row[k] = ''
        rows.append(row)
    return title, rows


def write_csv(title, rows, csv_file_name):
    with open(csv_file_name, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=title)
        writer.writeheader()
        writer.writerows(rows)


def json_to_csv(object_list):
    global json_ob, c_line
    json_ob = {}
    c_line = 0
    #for ov in object_list :
    for ov in object_list:
        loop_data(ov)
        c_line += 1
    """with open("assets/1p3c.json", "r") as f:
        for ov in f :
            ov = json.loads(ov.strip())
            loop_data(ov)
            c_line += 1"""
    title, rows = get_title_rows(json_ob)
    write_csv(title, rows, 'cases-current.csv')

json_to_csv(o)

print(o)

"""f = open('assets/1p3c.json', 'w', encoding='utf-8')
f.write(data)
f.close()
print("finished!")

f = open('test3.json', 'w')
f.write(confirmed_data)
f.close()

f = open('test3d.json', 'w')
f.write(deaths_data)
f.close()"""
