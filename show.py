#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 這是展演活動的info
#1. 已經將要輸出的資訊都傳入show，可以看一下show這個變數
#2. county也放入


# In[ ]:


import requests
json_url = 'https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=6'
download = requests.get(json_url,verify=False)


# In[ ]:


download = download.content.decode("utf-8")


# In[ ]:


import json
j = json.loads(download)


# In[ ]:


# title
# location
# locationName
# endTime
show = []
for i in range(0,len(j)):
    show.append({'title': j[i]['title'],
    'location':j[i]['showInfo'][0]['location'],
    'locationName':j[i]['showInfo'][0]['locationName'],
    'endTime':j[i]['showInfo'][0]['endTime'],
    'county':j[i]['showInfo'][0]['location'][:3]})


# In[ ]:


#show


# In[ ]:




