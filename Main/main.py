from PyQt5 import QtCore, QtGui, QtWidgets
from bieudo import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMenu
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sklearn.metrics import r2_score
import seaborn as sns
import plotly.graph_objects as go
from PyQt5.QtCore import QTimer
import pandas as pd
import numpy as np
import time
from PyQt5.QtCore import QTimer

import sip
colors = ['red', 'green', 'blue', 'yellow', 'orange', 'aqua', 'purple', 'blueviolet']
timer = QTimer()
sheet_id = '1rFqUIqGhauEqoEpio_mCsGkN66fdr_HLJrfmOT-7FlI'
status_thang = 0
status_nam = 0

class ChartLine(FigureCanvas):
    def __init__(self, x1, y1,lables,color):
        self.fig, self.ax = plt.subplots(figsize=(9, 7), sharex=True, sharey=True)
        super().__init__(self.fig)
        self.x1 = x1
        self.y1 = y1
        self.lables = lables

        self.ax.clear()

        #Hồi quy đa thức
        z = np.polyfit(self.x1, self.y1, 1) #đa thức bậc 1
        p = np.poly1d(z) #đường thẳng
        if color == "b":
            
            self.ax.plot(self.x1,p(self.x1),"r--",label =  "Đường xu hướng")
        elif color == "r":
            self.ax.plot(self.x1,p(self.x1),"b--",label = "Đường xu hướng" )
        self.ax.plot(self.x1, self.y1,color = color,label = lables)
        self.ax.set_title(self.lables, fontsize=14)
        self.ax.set_xlabel("Năm")
        self.ax.set_ylabel(self.lables)
        self.ax.legend( loc = 'best')  

          
class ChartLinerealtime(FigureCanvas):
    def __init__(self,x1,y1,y2,lables):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        self.x1 = x1
        self.y1 = y1
        self.y2 = y2
        self.lables = lables
        
        self.ax.clear()
        self.ax.plot(self.x1,self.y1,color = 'b', markersize=5,label = "Nhiệt Độ (°C)" )

        plt.xticks(rotation = 20)
        self.ax.legend(loc = "lower left")     
        self.ax2 = self.ax.twinx()
        self.ax2.plot(self.x1,self.y2,label = "Độ Ẩm (%)", color = 'r',linewidth = 2)
        self.ax2.set_title('Nhiệt Độ Độ Ẩm Thời Gian Thực') 
        self.ax2.legend(loc ="upper left")    
        
 

class Chart2Line(FigureCanvas): 
    def __init__(self,x1,y1,y2,lable):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        self.x1 = x1
        self.y1 = y1
        self.y2 = y2
  
        self.ax.clear()
        self.ax.plot(self.x1,self.y1,color = 'b', markersize=5,label = "Thực Tế" )
        self.ax.plot(self.x1,self.y2,color = 'r', markersize=5 ,label = "Dự Đoán")
        self.ax.set_title(lable)
        self.ax.set_xlabel("Năm")
        self.ax.set_ylabel(lable.strip('Dự Đoán'))
        self.ax.legend()     
        
class ChartBar(FigureCanvas):
    def __init__(self,x1,y1,y2):
        self.fig, self.ax1 = plt.subplots()
        
        super().__init__(self.fig)
        self.x1 = x1
        self.y1 = y1
        self.y2 = y2

        self.ax1 = plt.subplot(1,1,1)
        self.ax1.bar(self.x1,self.y1 , color = '#6090C0',label = "Lượng Mưa (mm)")

        self.ax1.legend(loc ="lower right")  
        self.ax2 = self.ax1.twinx()
        self.ax2.plot(self.x1,self.y2,label = "Nhiệt Độ (°C)", color = '#cf6a63',linewidth = 2)
        self.ax2.set_title('Nhiệt Độ Lượng Mưa Năm 2015')
        self.ax2.legend( loc = 'best')  

class ChartScatter(FigureCanvas):
    def __init__(self,x1,y1):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)       
        self.x1 = x1
        self.y1 = y1
        model = np.polyfit(self.x1, self.y1, 1)

        predict = np.poly1d(model)
        hours_studied = len(self.x1)
        predict(hours_studied)

        r2_score(y1, predict(x1))
        x_lin_reg = range(20,len(self.x1) + 20)
        y_lin_reg = predict(x_lin_reg)
        self.ax.scatter(self.x1, self.y1,label = "Độ Ẩm (%)")
        self.ax.set_title('Mối tương quan giữa nhiệt độ và độ ẩm')
        self.ax.set_xlabel('Nhiệt Độ (°C)')
        self.ax.set_ylabel('Độ Ẩm (%)')
        self.ax.legend( loc = 'best')  
        global status_thang
        if (status_thang == 1):
            self.ax.plot(x_lin_reg, y_lin_reg, c = 'r')
            status_thang = -1
        else:
            pass
class ChartBox(FigureCanvas):
    def __init__(self,y1,y2):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)       
        self.y1 = y1
        self.y2 = y2
        data = [self.y1]   
        
        self.ax.boxplot(data)       
        self.ax = self.fig.add_subplot(111)
 
        self.ax.boxplot(data, patch_artist = True,
                notch ='True', vert = 0)    
class ChartKDE(FigureCanvas):
    def __init__(self,y1,lable,color):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)       
        self.y1 = y1
        sns.kdeplot(self.y1,label = lable, color= color, shade=True)
  
        # Đặt label các cột
        self.ax.set_title('Mật Độ ' + lable)
        self.ax.set_xlabel(lable)
        self.ax.set_ylabel('Xác suất xuất hiện')
        self.ax.legend( loc = 'best')  

class ChartPie(FigureCanvas):
    def __init__(self,x1,y1):
        self.fig, self.ax = plt.subplots(figsize=(9, 9), sharex=True, sharey=True)
        super().__init__(self.fig) 
        self.x1   = x1      
        self.y1   = y1

        myexplode = [0,0.3,0,0,0,0,0,0.5,0,0,0,0]
        lable     = ['Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6','Tháng 7', 'Tháng 8', 'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12']
        self.ax.pie(self.y1, labels=lable, explode = myexplode, shadow = True,autopct= '%2.1f%%')
        self.ax.set_title('Lượng Mưa Năm 2015')
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        self.thang = None
        self.nam   = None
        self.thoigianrealtime    = None
        self.nhietdorealtime     = None
        self.doamrealtime        = None

        self.nhietdotheonam      = None
        self.nhietdotheothang    = None
        self.luongmuatheonam     = None
        self.luongmuatheothang   = None
        self.doamtheothang       = None
        self.tocdogiotheothang   = None

        self.tgdubaonhietdo      = None
        self.tgdubaoluongmua     = None
        self.actual_nhietdo      = None
        self.prediction_nhietdo  = None
        self.actual_luongmua     = None
        self.prediction_luongmua = None


        self.chart1 = None
        self.chart2 = None
        self.chart3 = None
        self.chart4 = None 
        
        self.Xuli()

        self.uic.nam.clicked.connect(self.next)
        self.uic.thang.clicked.connect(self.previous)

    def previous(self):
        global status_nam 
        status_nam= 0

        try:
            self.remove()
        except:
            pass
        self.chart1  = ChartBar(self.thang,self.luongmuatheothang,self.nhietdotheothang)
        self.chart3  = ChartPie(self.thang,self.luongmuatheothang)
        self.chart2  = ChartScatter(self.nhietdotheothang,self.doamtheothang)
        self.add()
        global status_thang
        status_thang = status_thang + 1
        timer.timeout.connect(self.Realtimenhietdo)
        timer.start(2000)
        self.Realtimenhietdo()
    def Realtimenhietdo(self):
        try: 
            sip.delete(self.chart4)
            self.chart4 = None
        except:
            pass

        getdatarealtime = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
        datarealtime    = getdatarealtime.tail(20)
        datarealtime    = datarealtime.fillna(method='ffill')
        

        self.thoigianrealtime = np.array(datarealtime['Time'])
        self.nhietdorealtime  = np.array(datarealtime['Temperature'])
        self.doamrealtime     = np.array(datarealtime['Humidity'])


        self.chart4 = ChartLinerealtime(self.thoigianrealtime,self.nhietdorealtime,self.doamrealtime,"hello")
        self.uic.scr14.addWidget(self.chart4)


    def next(self):
        global status_thang
        global status_nam
        status_thang = 0
        status_nam   = status_nam + 1
        timer.stop()
        try:
            self.remove()
        except:
            pass
        print(status_nam)
        if status_nam == 2:
            self.chart1 = Chart2Line(self.tgdubaonhietdo,self.actual_nhietdo,self.prediction_nhietdo,"Dự Đoán Nhiệt Độ")
            self.chart4 = Chart2Line(self.tgdubaoluongmua ,self.actual_luongmua,self.prediction_luongmua,"Dự Đoán Lượng Mưa")
            
            status_nam  = 0
        else:
            self.chart1 = ChartLine(self.nam,self.nhietdotheonam,"Nhiệt Độ (°C)","r")
            self.chart4 = ChartLine(self.nam,self.luongmuatheonam,"Lượng Mưa (mm)","b")
        self.chart3 = ChartKDE(self.nhietdotheonam,"Nhiệt Độ (°C)","r")
        self.chart2 = ChartKDE(self.luongmuatheonam,"Lượng Mưa (mm)","b")

        self.add()
    def Xuli(self):
        self.data1nam             = pd.read_csv("data/data1nam.csv")    
        self.data100nam           = pd.read_csv("data/data100nam.csv")
        self.datatrainnhietdo     = pd.read_csv("data/dudoannhietdo.csv")
        self.datatrainluongmua    = pd.read_csv("data/dudoanluongmua.csv")
        
        self.nhietdotheonam       = np.array(self.data100nam['Temp'])
        self.luongmuatheonam      = np.array(self.data100nam['Rain_fall'])
        self.nam                  = np.array(self.data100nam['Year'])

        self.nhietdotheothang     = np.array(self.data1nam['Temp'])
        self.luongmuatheothang    = np.array(self.data1nam['Rain_fall'])
        self.doamtheothang        = np.array(self.data1nam['Humidity'])
        self.tocdogiotheothang    = np.array(self.data1nam['wind_speed'])
        self.thang                = np.array(self.data1nam['Month'])

        self.tgdubaonhietdo       = np.array(self.datatrainnhietdo['Year'])
        self.tgdubaoluongmua      = np.array(self.datatrainluongmua['Year'])
        self.actual_nhietdo       = np.array(self.datatrainnhietdo['actual_nhietdo'])
        self.actual_luongmua      = np.array(self.datatrainluongmua['actual_luongmua'])
        self.prediction_nhietdo   = np.array(self.datatrainnhietdo['predictions_nhietdo'])
        self.prediction_luongmua  = np.array(self.datatrainluongmua['predictions_luongmua'])

    def remove(self):
         try:
            sip.delete(self.chart1)
            self.chart1 = None
            sip.delete(self.chart2)
            self.chart2 = None
            sip.delete(self.chart3)
            self.chart3 = None
            sip.delete(self.chart4)
            self.chart4 = None
         except Exception as e:
             print(e)
             pass

    def add(self):
        self.uic.scr11.addWidget(self.chart1)
        self.uic.scr12.addWidget(self.chart2)
        self.uic.scr13.addWidget(self.chart3)
        self.uic.scr14.addWidget(self.chart4)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())   