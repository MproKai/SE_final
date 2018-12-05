# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
from flask import Flask , render_template,flash,redirect,url_for,session,request
from passlib.hash import sha256_crypt
from functools import wraps
from classifier import classifier
import json
import numpy as np
import pandas as pd
import dill as pickle
from Validate import Preprocess
import time
#from DBmgt import db, DoSQL
from DBmgt import DoSQL
import DataToSQL


app = Flask(__name__)
app.secret_key='secret123'

@app.route('/main',methods=['POST'])
def main():
    
    if method == 'POST':
        """click which county"""
        """return render_template('recommand.html',data = county)"""
    """return render_template('home_page.html',data = value_passer().Passvalue_pm25())"""
    

@app.route('/recommand',methods=['POST'])
def recommand():   
    
    if method == 'POST':
         """click which show"""
         """insert usertable """
    
    """選最小pm25的縣市(高雄、台北、新竹)"""
    """ logic for recommand"""    
    min_pm25  = select county from PM25 where pm25 = min(3)
    if data2.county == min_pm25:
        recommand_show = select title,locationname... from show



@app.route('/county_detail',methods=['POST'])
@is_logged_in
def county_detail():
    username = session['username']      
    addr = session['addr']
    if method == 'POST':
         """click which show"""
         """insert usertable """
    
    """ 選桃園 """
    if county = county : data = value_passer().Passvalue_pm25()
    countyExinfo = value_passer().Passvalue_Exinfo(#用戶居住地)
    

    """桃園全部show"""
    """ logic for same show """
    if data2 != recommand_show ... =  data3
    
    return render_template('recommand.html',pm25 = data , recommand = recommand_show , all_show = data3 )
    
    
@app.route('/favorite',methods=['POST'])
def favorite():   
    """ if session.username == usertable"""
    """data = select ...."""
    
    if method == 'POST':
         """click which show"""
         """delete usertable """
# 關於頁面
@app.route('/about')
def about():
    return render_template('about.html')

# 總文章頁面
@app.route('/articles')
def articles():
    
    result , articles =  DoSQL().S_db("SELECT * FROM articles",None,0)
    #print(articles)
    #listarticles
    
    #for article in articles:
        
    
    if result > 0:
        return render_template('articles.html',articles = articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html',msg = msg)
    

# 撰寫單一文章
@app.route('/article/<string:id>/')
def article(id): 
    result , article =  DoSQL().S_db("SELECT * FROM articles WHERE id=%s",[id],1)  
    return render_template('article.html', article = article)


# 使用者註冊
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method =='POST' and form.validate():
        
        DataToSQL.RegisterToSQL(form.name, form.email, form.username, form.password)   
        
        """create user table id show_column"""
        flash('You are now registered and can login','success')     
        return redirect(url_for('login'))   
    
    return render_template('register.html',form = form)    
        

# 使用者登入
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method =='POST':
        
        result,data,username,password_candidate = DataToSQL.LoginToSQL('username','password')
        if result > 0 :
            # Get stored hash
            password = data['password']
            
            # Compare Passwords
            if sha256_crypt.verify(password_candidate,password):
                # Passed
                session['login_in'] = True
                session['username'] = username
                
                flash('You are now logged in','success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html',error = error)
        else:
            error = 'Username not found'
            return render_template('login.html',error = error)
            
        
    return render_template('login.html')

# Check 使用者是否有登入
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'login_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized,Please log in','danger')
            return redirect(url_for('login'))
    return wrap


# 登出
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    
    result,articles = DoSQL().S_db("SELECT * FROM articles",None,0)

    if result > 0:
        return render_template('dashboard.html',articles = articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html',msg = msg)
    
# 加入文章
@app.route('/add_article',methods=['GET','POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method =='POST' and form.validate(): 
        
        DataToSQL.add_articleToSQL(form.title,form.body,session['username'])      
        flash('Article Created','success')   
        return redirect(url_for('dashboard'))
    
    return render_template('add_article.html',form=form)


# 編輯文章
@app.route('/edit_article/<string:id>',methods=['GET','POST'])
@is_logged_in
def edit_article(id):
    
    result , article = DoSQL().S_db("SELECT * FROM articles WHERE id = %s",[id],1)
    
    # Get form
    form = ArticleForm(request.form)
    
    # Populate article form fields
    form.title.data = article['title']
    form.body.data = article['body']
    
    if request.method =='POST' and form.validate():
        
        DataToSQL.edit_articleToSQL('title','body',id)
        flash('Article Updated','success')
        return redirect(url_for('dashboard'))  
    return render_template('edit_article.html',form=form)
    

# 刪除文章
@app.route('/delete_article/<string:id>',methods=['POST'])
@is_logged_in
def delete_article(id):
      
    DoSQL().IUD_db("DELETE FROM articles WHERE id = %s",[id])     
    flash('Article Deleted','success')       
    return redirect(url_for('dashboard'))
    




if __name__ == '__main__':
    """scrapy sleep.."""
    app.run(host='127.0.0.1',port=81,debug=False)
    
    
    
    
    
    
    
    
    
    
    
    