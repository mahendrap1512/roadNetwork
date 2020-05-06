import pandas as pd
import csv


dataFrame = pd.read_csv('dataOp.csv')
cols = dataFrame.shape[1]
colName = "5 Minutes"
toInsert = [str(x).strip().split(' ')[1] for x in dataFrame[colName]]
print(toInsert)

allRows = list()
filePtr = open('dataOp.csv')
file = csv.reader(filePtr)
header = next(file)
header.append('Time')
allRows.append(header)
print(header)
i = 0
for line in file:
    line.append(toInsert[i])
    allRows.append(line)
    i += 1
filePtr.close()

with open('dataOp1.csv', 'w') as opFile:
    fp = csv.writer(opFile)
    fp.writerows(allRows)
