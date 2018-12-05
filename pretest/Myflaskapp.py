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
from sklearn.model_selection import train_test_split
from Validate import Preprocess
import time
#from DBmgt import db, DoSQL
from DBmgt import DoSQL
from formclass import RegisterForm,Titanic_ml,ArticleForm
import DataToSQL
import ML

app = Flask(__name__)
app.secret_key='secret123'

# Config MySQL
app.config['MYSQL_HOST'] = '35.196.78.102'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'th850413'
app.config['MYSQL_DB'] = 'flasktest'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
#db.init_app(app)
#mysql = MySQL(app)

# 主畫面
@app.route('/')
def index():
    return render_template('index.html')

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
    
# 鐵達尼號機器學習預測存活死亡
@app.route('/Titanic_ML',methods=['GET','POST'])
@is_logged_in
def Titanic_ML():
    form = Titanic_ml(request.form)
    if request.method =='POST' and form.validate():
        
        Pclass,Sex,Age,Fare,Embarked,Title,IsAlone,AgePclass = DataToSQL.Titanic_MLTOSQL(form.Pclass,form.Sex,form.Age,form.Fare,form.Embarked,form.Title,form.IsAlone)
                  
        # Loaded model which is already pretrain  
        clf = classifier()
        loaded_model = clf.modelload('Titanic_model/model_v2.pk')
      
        parm = np.array([int(Pclass), int(Sex) , int(Age), int(Fare), int(Embarked), int(Title), int(IsAlone), int(AgePclass)]).reshape(1,-1)
        prediction = loaded_model.predict(parm) # result
        
        if prediction[0] == 0:
            ans = 'Wasted , R.I.P '
        else:
            ans = 'Lucky you are !!'

        return render_template('titanic_ml_ans.html',ans=ans)
    return render_template('titanic_ml.html',form = form)    


# Help you train
@app.route('/dataload')
@is_logged_in
def dataload():
    return render_template('dataload.html')

# 讀取資料及驗證資料是否可存取
@app.route('/comfirm', methods=["POST"])
def comfirm():
    
    global f_name
    filename , data_col =  ML.read_userfile('data_file',session['username'])
    f_name = filename
    return render_template('comfirm.html',data_col=data_col)

# 選擇 features & label 欄位
@app.route('/select',methods=['POST'])
def select():
    
    global train_cols 
    global label_cols 
    train_cols = request.form.getlist('checking') # error for choose none
    label_cols = request.form.getlist('selecting') # error for choose none
      
    # Models可供 User 選擇
    clf = classifier()
    models_name =  clf.models_name
    
    return render_template('split.html',models_name = models_name)


# 選擇 training的參數及做 training的動作和存取 Model
@app.route('/split',methods=['POST'])
def split():
    
    
    test_size = float(request.form['test_size'])
    random_state = int(request.form['random_state'])
    model_name = request.form['model_name']
    model_select = request.form.getlist('model_select')
    
    col_choosed = ','.join(train_cols)
    
    datset_path = 'User_dataset/' + session['username'] +'/' + f_name+'.csv' # read data 
    train_set = pd.read_csv(datset_path)
    y = train_set[label_cols]
    X = train_set[train_cols]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    #print(type(model_select))
    clf = classifier()
    
    start_time = time.time()
    
    model = getattr(clf, model_select[0])(X_train,y_train)
    
    training_time = time.time() - start_time
    
    model_path = 'User_dataset/'  + session['username'] +'/' + model_name+'.pickle' 
    clf.modelsave(model_path,model)
    #print(model.predict(X_test))
    acc_log = round(model.score(X_test,y_test)*100,2)
    
    
    DoSQL().IUD_db("INSERT INTO HelpUTrainlog(username,training_time,dataset_name,model_name,model_choosed,col_choosed,test_size,random_state,val_acc) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
              (session['username'],training_time,f_name,model_name,model_select[0],col_choosed,test_size,random_state,acc_log))  
    flash('Training success','success')
    
    return render_template('dataload.html')

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
def county_detail():   
    
    
    if method == 'POST':
         """click which show"""
         """insert usertable """
    
    """ 選桃園 """
    if county = county : data = value_passer().Passvalue_pm25()
    data2 = value_passer().Passvalue_show()
    

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
    


if __name__ == '__main__':
    """scrapy sleep.."""
    app.run(host='127.0.0.1',port=81,debug=False)
    
    
    
    
    
    
    
    
    
    
    
    