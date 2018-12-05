# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 16:18:49 2018

@author: thomas
"""
import requests
import json
import DBmgt
#from DBmgt import DoSQL


#connection = pymysql.connect(**config)
class ScrapyExInfo():
    def ScrapyExInfo():
        
        json_url = 'https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=6'
        download = requests.get(json_url,verify=False)

        download = download.content.decode("utf-8")
        ExInfo = json.loads(download)
        
        ExInfolist = []
        
        for i in range(0,len(ExInfo)):
            ExInfolist.append({'title': ExInfo[i]['title'],
                     'location':ExInfo[i]['showInfo'][0]['location'],
                     'locationName':ExInfo[i]['showInfo'][0]['locationName'],
                     'endTime':ExInfo[i]['showInfo'][0]['endTime'],
                     'county':ExInfo[i]['showInfo'][0]['location'][:3]})      
        
       # for k in range(0,2):            
       #     print(ExInfolist[k])  
        conn = pymysql.connect(**config)
        conn.autocommit(1)
        cursor = conn.cursor()
        cursor.execute("""TRUNCATE TABLE test.exinfo""")
        cursor.executemany("""INSERT INTO exinfo (title, location,locationName,endTime,county) 
               VALUES (%(title)s, %(location)s, %(locationName)s, %(endTime)s, %(county)s)""",ExInfolist)
        cursor.close()
        
ScrapyExInfo.ScrapyExInfo()  


