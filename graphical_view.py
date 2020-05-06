import pandas as pd
import matplotlib.pyplot as plt

dataFrame = pd.read_csv('data/train.csv')
slots = 24 * 12
timings = [y for y in range(0, slots * 5, 5)]
print(timings)
traffic_min = "Lane 1 Flow (Veh/5 Minutes)"
traffic = [x for x in dataFrame[: slots][traffic_min]]
for i in range(0, dataFrame.shape[0], slots):
    for j in range(slots):
        traffic[j] = (traffic[j] + dataFrame[traffic_min][i + j]) / 2

# print(traffic)
plt.plot(timings, traffic)
plt.savefig('traffic.png')
