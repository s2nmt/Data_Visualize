import requests
import csv

url = 'https://weather-api-v2.onrender.com/api/weathers'

# đặt tiêu đề
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

reponse = requests.request('GET', url, headers=headers, data={})
#lấy data về dưới dạng json
myjson = reponse.json()
#print(myjson)
# lấy dữ liệu theo các cột
csvheader = ['Country','Year','Month','Temp','Humidity','Rain fall','wind_speed']
ourdata = []

for x in myjson['weathers_flated']:
    listing = [x['country'],x['year'],x['month'],x['temp'],x['humidity'],x['rainfall'],x['wind_speed']]
    ourdata.append(listing)

# ghi file
with open('weather.csv','w',encoding='UTF8',newline='') as f:
    writer = csv.writer(f)

    writer.writerow(csvheader)
    writer.writerows(ourdata)

