# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 02:48:21 2018

@author: willy
"""
from DBmgt import DoSQL
class Exinfo_passer:
    def Passvalue_Exinfo(addr):
        addr =  DoSQL.Select_db("SELECT ...")# 選取用戶位置
        Exinfo = DoSQL().Select_db("SELECT TITLE,LOCATION,LOCATIONNAME,ENDTIME WHERE COUNTY=%S",addr)#將用戶位置與展場搭配
        return Exinfo
        
        
        