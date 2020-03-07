import sqlite3

conn = sqlite3.connect("assets/virus.db")
cursor = conn.cursor()

with open("assets/canada_city.txt", "r", encoding="utf-8") as fp:
    states = fp.readlines()
    for state in states:
        try:
            #print(state.replace("\n", "").lower())
            cursor.execute("ALTER TABLE virus ADD [" + state.replace("\n", "").lower() + "] CHAR(20);")
        except:
            continue

with open("unitedStates.txt", "r", encoding="utf-8") as fp:
    states = fp.readlines()
    for state in states:
        print(state.replace("\n","").lower())
        try:
            cursor.execute("ALTER TABLE virus ADD [" + state.replace("\n", "").lower() + "] CHAR(20);")
        except:
            continue