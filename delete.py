fp = open("assets/virus2.csv", "r", encoding="utf-8")
lines = fp.readlines()
fp.close()
n = len(lines)
if lines[n-1][0:10] == lines[n-2][0:10]:
    lines.pop(n-2)
pass
with open("assets/virus2.csv", "w", encoding="utf-8") as fp:
    for line in lines:
        fp.write(line)

print("finished!")