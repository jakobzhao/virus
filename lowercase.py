unitedStates = []
with open("assets/old_name.csv", "r", encoding="utf-8") as fp:
    states = fp.readlines()
    for state in states:
        unitedStates.append(state.replace("\n","").lower())


with open("assets/old_name.csv", "w", encoding="utf-8") as fp:
    for state in unitedStates:
            fp.write(state + ",")