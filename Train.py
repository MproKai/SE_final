#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 讀取PM25
#1. 整個概念是資料庫裡只會有每個縣市近10小時的PM2.5值，下一個的PM25來後，update此資料表，並且刪除原本第一個小時的PM25
#2. 我們可以每九個小時的PM25預測第10小時的PM25，Train model的地方我會寫好


# In[6]:


import pandas as pd
from datetime import datetime
import xgboost as xgb


# while true

time = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + str(datetime.now().hour)
file = time+'PM25.csv'
df = pd.read_csv(file)
max_pm_per_county = df.groupby(['county'])['PM25'].max() # select max(pm25) from table_name group by county 


Nantou = []
Chiayi_4= []
Chiayi= []
Keelung= []= []
Yilan= []
Pingtung= []
Changhua= []
xinbei= []
Hsinchu_4= []
Hsinchu= []
Taoyuan= []
Penghu= []
Taichung= []
Taipei= []
Tainan= []
Taitung= []
Hualien= []
Miaoli= []
Lianjiang= []
Kinmen= []
Yunlin= []
Kaohsiung= []

Nantou.append(max_pm_per_county[0])
Chiayi_4.append(max_pm_per_county[1])
Chiayi.append(max_pm_per_county[2])
Keelung.append(max_pm_per_county[3])
Yilan.append(max_pm_per_county[4])
Pingtung.append(max_pm_per_county[5])
Changhua.append(max_pm_per_county[6])
xinbei.append(max_pm_per_county[7])
Hsinchu_4.append(max_pm_per_county[8])
Hsinchu.append(max_pm_per_county[9])
Taoyuan.append(max_pm_per_county[10])
Penghu.append(max_pm_per_county[11])
Taichung.append(max_pm_per_county[12])
Taipei.append(max_pm_per_county[13])
Tainan.append(max_pm_per_county[14])
Taitung.append(max_pm_per_county[15])
Hualien.append(max_pm_per_county[16])
Miaoli.append(max_pm_per_county[17])
Lianjiang.append(max_pm_per_county[18])
Kinmen.append(max_pm_per_county[19])
Yunlin.append(max_pm_per_county[20])
Kaohsiung.append(max_pm_per_county[21])


# In[52]:


county_name = ['南投縣',
 '嘉義市',
 '嘉義縣',
 '基隆市',
 '宜蘭縣',
 '屏東縣',
 '彰化縣',
 '新北市',
 '新竹市',
 '新竹縣',
 '桃園市',
 '澎湖縣',
 '臺中市',
 '臺北市',
 '臺南市',
 '臺東縣',
 '花蓮縣',
 '苗栗縣',
 '連江縣',
 '金門縣',
 '雲林縣',
 '高雄市']


# In[86]:


import xgboost as xgb


# In[94]:


x = [[23,15,17,24,45,56,66,53,51,43,57,59]]
y = [[55]]


# In[95]:


import numpy as np
train_x = np.array(x)
y = np.array(y)


# In[96]:


from sklearn.linear_model import LinearRegression
reg = LinearRegression().fit(x, y)


# In[97]:


test_x = [[17,24,45,56,66,53,51,43,57,59,45,33]]
test_x = np.array(test_x)


# In[98]:


reg.predict(test_x)


# In[ ]:




