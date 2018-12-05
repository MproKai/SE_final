# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 16:34:09 2018

@author: gaga
"""
import pymysql.cursors
# doing sql

#db = pymysql()
#connect to db
config = {
'host':'127.0.0.1',
'port':3306,
'user':'root',
'password':'123456',
'db':'test',
'charset':'utf8',
'cursorclass':pymysql.cursors.DictCursor,
}

connection = pymysql.connect(**config)
connection.autocommit(1)
cursor = connection.cursor()

class DoSQL():
    def Select_db(self,sql,params,fetch):
        result = cursor.execute(sql,(params))
        
        # if result > 0 #
    
        # fetch one or all
        if fetch>0:
            content = cursor.fetchone()
            #data = cursor.fetchone()
        else:
            content = cursor.fetchall()
            
        #content = list(content)
            
        #close cursor    
        #db.close()
        cursor.close()
            
        return result,content
    
    # Insert , Update , Delete
    def IUD_db(self,sql,params):
        cursor.execute(sql,(params))
        cursor.close()
        
    def I_executmany(self,sql,params):
        cursor.executemany(sql,params)
        cursor.close()
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    