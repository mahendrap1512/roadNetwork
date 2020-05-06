import csv
import random

import pandas as pd


def gen(x):
    if x < 50:
        return int(random.randint(0, 100) + random.randint(100, 200))
    elif x < 100:
        return int(random.randint(0, 100) + random.randint(110, 220) + random.randint(30, 300))
    elif x < 135:
        return int(random.randint(0, 100) + random.randint(120, 250) + random.randint(50, 600))
    else:
        return int(random.randint(0, 100) + random.randint(130, 300) + random.randint(210, 1000))


dataFrame = pd.read_csv('finalData.csv')
cols = dataFrame.shape[1]
colName = "Safe"
toInsert = [x for x in dataFrame[colName]]
print(toInsert)

allRows = list()
filePtr = open('dataOp1.csv')
file = csv.reader(filePtr)
columns = [1, 6]
header = next(file)
heading = ["Lane 1 Flow (Veh/5 Minutes)", "Time", "Clearance Time in Seconds", "Safe"]
allRows.append(heading)
i = 0

for row in file:
    content = row
    content.append(toInsert[i])
    i += 1
    allRows.append(content)

filePtr.close()

with open('dataOp2.csv', 'w') as opFile:
    fp = csv.writer(opFile)
    fp.writerows(allRows)
