# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 20:25:02 2018

@author: gaga
"""
from passlib.hash import sha256_crypt
from DBmgt import DoSQL
from flask import request
class DataToSQL():
    
    def RegisterToSQL(name, email, username, password):
        
        name = name.data
        email = email.data
        username = username.data
        password = sha256_crypt.encrypt(str(password.data))        
        DoSQL().IUD_db("INSERT INTO users(name,email,username,password) VALUES(%s, %s, %s, %s)",(name, email, username, password))
        
    
    def LoginToSQL(username,password):
        
         username = request.form[username]
         password_candidate = request.form[password]   
         result,data = DoSQL().S_db("SELECT * FROM users WHERE username = %s",[username],1)
         return result,data,username,password_candidate
        
        
    def add_articleToSQL(title,body,session_name):
        
        title = title.data
        body = body.data       
        DoSQL().IUD_db("INSERT INTO articles(title,body,author) VALUES(%s,%s,%s)",(title,body,session_name))
        
    
    def edit_articleToSQL(title,body,id):
        
        title = request.form[title]
        body = request.form[body]
        DoSQL().IUD_db("UPDATE articles SET title= %s, body=%s WHERE id=%s",(title,body,id))    
        
    
    def recommand_ToSQL(title,location,locationName,endTime):
        return True
        

    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    