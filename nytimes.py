unitedStates = []
with open("assets/united-states.txt", "r", encoding="utf-8") as fp:
    states = fp.readlines()
    for state in states:
        unitedStates.append(state.replace("\n","").lower())

raw = []
with open("assets/nytimes-usstate.csv", "r", encoding="utf-8") as fp:
    lines = fp.readlines()[1:]
    for line in lines:
        raw.append(line.replace("\n","").split(','))

day = {}
for r in raw:
    date = r[0]
    state = r[1]
    

print(raw)