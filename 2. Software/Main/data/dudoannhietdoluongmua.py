import pandas as pd
import numpy as np
# đọc dữ liệu từ file lấy dữ liệu từ file weather
Data = pd.read_csv("data/data100nam.csv")

# Nhóm nhiệt độ với lượng mưa với key là year
Data = Data[['Temp','Rain_fall']].groupby(Data['Year']).mean()

# tạo một cột mới bằng giá trị được đưa vô dịch xuống
Data["target_nhietdo"] = Data.shift(-1)["Temp"]
Data["target_luongmua"] = Data.shift(-1)["Rain_fall"]

# xóa hàng cuối
Data = Data.iloc[:-1,:].copy()
from sklearn.linear_model import Ridge

# sử dụng hồi quy ridge đặt hệ số anlpha = 0.1
reg = Ridge(alpha=.1)
# tạo 2 danh sách nhiệt độ và lượng mưa để thử nghiệm
predictors_nhietdo = [ "Temp"]
predictors_luongmua = [ "Rain_fall"]

# tạo dữ liệu để train và dữ liệu thực để kiểm tra
train = Data.loc[:"2000"]
test = Data.loc["2001":]

# đưa 2 dữ liệu vào trong method fit để train theo ridge
# https://www.sharpsightlabs.com/blog/sklearn-fit/
reg.fit(train[predictors_nhietdo], train["target_nhietdo"])
# dự đoán các đầu ra mới
predictions_nhietdo = reg.predict(test[predictors_nhietdo])
reg.fit(train[predictors_luongmua], train["target_luongmua"])
predictions_luongmua = reg.predict(test[predictors_luongmua])
from sklearn.metrics import mean_squared_error
saisonhietdo  = mean_squared_error(test["target_nhietdo"], predictions_nhietdo)
saisoluongmua = mean_squared_error(test["target_luongmua"], predictions_luongmua)
# Sai số so với kết quả 
print("sai so nhiet do",saisonhietdo)
print("sai so luong mua",saisoluongmua)
combined_nhietdo = pd.concat([test["target_nhietdo"], 
pd.Series(predictions_nhietdo, index=test.index)], axis=1)
combined_nhietdo.columns = ["actual_nhietdo", "predictions_nhietdo"]
combined_luongmua = pd.concat([test["target_luongmua"], 
pd.Series(predictions_luongmua, index=test.index)], axis=1)
combined_luongmua.columns = ["actual_luongmua", "predictions_luongmua"]
#Lưu file
combined_nhietdo = combined_nhietdo.reset_index()
combined_nhietdo.to_csv("data/dudoannhietdo.csv", index=False)

combined_luongmua = combined_luongmua.reset_index()
combined_luongmua.to_csv("data/dudoanluongmua.csv", index=False)

print(combined_nhietdo)
print(combined_luongmua)
