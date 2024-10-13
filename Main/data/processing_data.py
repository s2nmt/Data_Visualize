import pandas as pd
import numpy as np
# đọc file csv
Data = pd.read_csv("data/weather.csv")

Data = Data.fillna(method="ffill")
print("Du lieu:")
print(Data)
print("Mo ta du lieu:")
print(Data.describe())
print("Thong tin du lieu:")
print(Data.info())
print("Kiem tra phan tu rong:")
print(Data.isnull().sum())

# tách dữ liệu theo nhiệt độ và lượng mưa
Dl100nhietdo = Data[['Temp','Humidity','wind_speed']].groupby([Data['Year']]).mean()
Dl100nhietdo = Dl100nhietdo.reset_index()

Dl100luongmua = Data['Rain_fall'].groupby([Data['Year']]).sum()
Dl100luongmua = Dl100luongmua.reset_index()


Dl100 = pd.concat([Dl100nhietdo["Year"],Dl100luongmua["Rain_fall"], Dl100nhietdo['Temp'],Dl100nhietdo['wind_speed'],Dl100nhietdo['Humidity']], axis=1)


Dl100.to_csv("data/data100nam.csv", index=False)
Dl100.to_excel("data/data100nam.xlsx")
# lấy 12 tháng cuối của dữ  liệu (1 năm)
Ver = Data[1440:]
Dl1 = Ver[['Temp','Rain_fall','Humidity','wind_speed']].groupby([Ver['Year'], Ver['Month']]).mean()

Dl1 = Dl1.reset_index()
Dl1.to_csv("data/data1nam.csv", index=False)