#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 自動擷取每小時PM2.5的值
#開啟 While true 便可以自動開爬


# In[3]:


import requests
import csv


def downloadPMCSV(time):
    CSV_URL = 'https://opendata.epa.gov.tw/ws/Data/ATM00625/?$format=csv'
    download = requests.get(CSV_URL,verify=False)
    download = download.content.decode("utf-8")
    reader = csv.reader(download.split('\n'), delimiter=',')

    name = time + 'PM25.CSV'
    with open(name,'a',encoding = 'utf8') as f:
        w = csv.writer(f)
        for row in reader:
            w.writerow(row)


# In[53]:


import time
from datetime import datetime
#while True:
time = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + str(datetime.now().hour)
downloadPMCSV(time)
#time.sleep(3600) # s


# In[ ]:




