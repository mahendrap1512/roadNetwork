# import pandas as pd
# from sklearn.preprocessing import LabelEncoder, OneHotEncoder
# from keras.models import Sequential
# from keras.layers import Dense
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import confusion_matrix
# from sklearn.preprocessing import PolynomialFeatures
# import matplotlib.pyplot as plt
#
#
# def ann():
#     model = Sequential()
#     model.add(Dense(80, input_dim=289, activation='relu'))
#     model.add(Dense(20, activation='relu', ))
#     model.add(Dense(10, activation='relu', ))
#     model.add(Dense(1, activation='relu'))
#     model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
#     return model
#
#

#
# # myModel = ann()
# # myModel.fit(x_train, y_train, epochs=100, batch_size=10)
# #
# # _, accuracy = myModel.evaluate(x_test, y_test)
# # print('Accuracy: %.2f' % (accuracy * 100))
#
# regressor = LinearRegression()
# regressor.fit(x_train, y_train)
# y_predict = regressor.predict(x_test)
#
#
# poly = PolynomialFeatures(2)
# x_poly = poly.fit_transform(x_train)
# poly.fit(x_poly, y_train)
# lin2 = LinearRegression()
# lin2.fit(x_poly, y_train)
#
# plt.scatter(x_train, y_train, color='blue')
#
# plt.plot(x_train, lin2.predict(poly.fit_transform(x_train)), color='red')
# plt.title('Polynomial Regression')
# plt.xlabel('Temperature')
# plt.ylabel('Pressure')
#
# plt.show()

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from datetime import datetime

dataFrame = pd.read_csv('../data/dataOp1.csv')
x_init = dataFrame.iloc[:, :-1].values
y_init = dataFrame.iloc[:, -1:].values
labelEncoder = LabelEncoder()
x_init[:, -1] = labelEncoder.fit_transform(x_init[:, -1])
oneHotEncoder = OneHotEncoder(handle_unknown='ignore')
enc_df = pd.DataFrame(oneHotEncoder.fit_transform(x_init[:, -1:]).toarray())
# dataFrame = dataFrame.join(enc_df)
x = dataFrame.loc[:, ["Lane 1 Flow (Veh/5 Minutes)"]].join(enc_df)
trainingSet = x.join(dataFrame.loc[:, "Clearance Time in Seconds"])
# print(trainingSet.head())
X = trainingSet.iloc[:, :-1].values
y = trainingSet.iloc[:, -1:].values
scalar_X = MinMaxScaler(feature_range=(0, 1))
scaledInput = scalar_X.fit_transform(X)
scalar_y = MinMaxScaler(feature_range=(0, 1))
scaledOutput = scalar_y.fit_transform(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
# X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))
#
# regressor = Sequential()
# regressor.add(LSTM(units=200, return_sequences=True, input_shape=(1, X_train.shape[2])))
# regressor.add(Dropout(0.2))
#
# regressor.add(LSTM(units=200, return_sequences=True, activation='relu'))
# regressor.add(Dropout(0.2))
#
# regressor.add(LSTM(units=100, return_sequences=True, activation='relu'))
# regressor.add(Dropout(0.1))
#
# regressor.add(LSTM(units=50, activation='relu'))
# regressor.add(Dropout(0.1))
#
# regressor.add(Dense(units=1, activation='relu'))
#
# regressor.compile(optimizer='adam', loss='mean_squared_error')
#
# regressor.fit(X_train, y_train, epochs=100, batch_size=32)
#
# # making prediction
# predictedClearanceTime = regressor.predict(X_test)
# X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[2]))
# predictedClearanceTime = scalar_y.inverse_transform(predictedClearanceTime)

# plot
# plt.plot(y_test, color='black', label='Actual clearance Time')
# plt.plot(predictedClearanceTime, color='green', label='Predicted clearance Time')
# plt.title('Clearance Time Prediction')
# plt.xlabel('Time')
# plt.ylabel('Traffic')
# plt.legend()
# plt.show()
# print(predictedClearanceTime)
# print(y_test)


regressor = LinearRegression()
regressor.fit(X_train, y_train)
y_predict = regressor.predict(X_test)

fig, ax = plt.subplots()
ax.plot(X_test[:, :1], y_test, color="blue")
ax.plot(X_test[:, :1], y_predict, color="green")
plt.xlabel('Vehicle Density')
plt.ylabel('Clearance time in second')
plt.text(  # position text relative to Axes
    1.0, 1.0, 'blue-> Actual time\n green->Predicted time',
    ha='right', va='top',
    transform=ax.transAxes
)
plt.show()


def predict_clearance_time(vehicles):
    global regressor

    curr_time = datetime.now()
    timestamp = curr_time.hour * 12 + curr_time.minute//5
    ip = [vehicles]
    l = [1 if x == timestamp else 0 for x in range(24*12)]
    ip.extend(l)
    ip_array = np.array(ip)
    ip_array = ip_array.reshape(1, len(ip))
    op = regressor.predict(ip_array)
    return op[0]
