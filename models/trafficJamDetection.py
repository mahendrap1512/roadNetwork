import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from datetime import datetime
import numpy as np


data = pd.read_csv("../data/dataOp2.csv")
X_init = data.iloc[:, :-1].values
y = data.iloc[:, -1:].values
labelEncoder = LabelEncoder()
X_init[:, 1] = labelEncoder.fit_transform(X_init[:, 1])
oneHotEncoder = OneHotEncoder(handle_unknown='ignore')
enc_df = pd.DataFrame(oneHotEncoder.fit_transform(X_init[:, 1:2]).toarray())
X = data[["Lane 1 Flow (Veh/5 Minutes)", "Clearance Time in Seconds"]]
X = X.join(enc_df)

model = LogisticRegression(solver="liblinear", random_state=13).fit(X, y)
cm = confusion_matrix(y, model.predict(X))

fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(cm)
ax.grid(False)
ax.xaxis.set(ticks=(0, 1), ticklabels=('Predicted 0->Traffic Jam', 'Predicted 1->Clear'))
ax.yaxis.set(ticks=(0, 1), ticklabels=('Actual 0->Traffic Jam', 'Actual 1->Clear'))
ax.set_ylim(1.5, -0.5)
for i in range(2):
    for j in range(2):
        ax.text(j, i, cm[i, j], ha='center', va='center', color='brown')

plt.title("Traffic Jam prediction")
plt.show()


def detect_jam(vehicle_intensity, clearance_time):
    global model
    curr_time = datetime.now()
    timestamp = curr_time.hour * 12 + curr_time.minute//5
    ip = [vehicle_intensity, clearance_time]
    l = [1 if x == timestamp else 0 for x in range(24*12)]
    ip.extend(l)
    ip_array = np.array(ip)
    ip_array = ip_array.reshape(1, len(ip))
    op = model.predict(ip_array)
    return op[0]
