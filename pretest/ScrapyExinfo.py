# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 16:18:49 2018

@author: thomas
"""
import requests
import json
from DBmgt import DoSQL


#connection = pymysql.connect(**config)
class ScrapyExinfo():
    def ScrapyExinfo():
        
        json_url = 'https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=6'
        download = requests.get(json_url,verify=False)

        download = download.content.decode("utf-8")
        Exinfo = json.loads(download)
        
        Exinfolist = []
        
        for i in range(0,len(Exinfo)):
            Exinfolist.append({'title': Exinfo[i]['title'],
                     'location':Exinfo[i]['showInfo'][0]['location'],
                     'locationName':Exinfo[i]['showInfo'][0]['locationName'],
                     'endTime':Exinfo[i]['showInfo'][0]['endTime'],
                     'county':Exinfo[i]['showInfo'][0]['location'][:3]})      
        sql = 'INSERT INTO exinfo (title, location,locationName,endTime,county) VALUES (%(title)s, %(location)s, %(locationName)s, %(endTime)s, %(county)s)'
        params = Exinfolist
        DoSQL().I_executmany(sql,(params))


