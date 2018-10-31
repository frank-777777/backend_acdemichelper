#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-
import os
#导入数据库模块
import pymysql
#导入Flask框架，这个框架可以快捷地实现了一个WSGI应用 
from flask import Flask
#默认情况下，flask在程序文件夹中的templates子文件夹中寻找模块
from flask import render_template
#导入前台请求的request模块
from flask import request   
import traceback  

import re

#传递根目录
app = Flask(__name__)


@app.route('/log', methods = ['POST'])
def log():

    db = pymysql.connect(host="localhost",
                         user="root",
                         password="7777777",
                         db="TESTDB")

    try:
        with db.cursor() as cursor:

            sql = "SELECT * from `users` WHERE username=%s AND password=%s"
            cursor.execute(sql, (request.json['userName'], request.json['userPassword']))
            result = cursor.fetchall() #返回匹配的多组
            print(result)

            if len(result) == 1:
                return 'Login succeed'
            else:
                print(result)
                return 'Username or password is incorrect'
            db.commit()
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
        return 'System error, try again'
    # 关闭数据库连接
    finally:
        db.close()


@app.route('/reg', methods=['POST'])
def reg():
    db = pymysql.connect(host="localhost",
                         user="root",
                         password="7777777",
                         db="TESTDB")
 
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO `users` (`username`, `email`, `password`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (request.json['userName'], request.json['userEmail'], request.json['userPassword'] ))
            db.commit()
            return 'reg succeed'

    except pymysql.err.IntegrityError as error:
        traceback.print_exc()
        db.rollback()

        if re.match(r"Duplicate entry '\S+' for key 'username'", str(error.args[1])) != None:
            return 'Username already exists'
        elif re.match(r"Duplicate entry '\S+' for key 'email'", str(error.args[1])) != None:
            return 'Email already exists'
        else:
            return 'Try again'

    except:
        traceback.print_exc()
        db.rollback()
        return 'System error, reg fail'

    finally:
        db.close()

@app.route('/test')
def test():
    return 'Hello'


if __name__ == '__main__':
    app.run(debug=True,host='192.168.100.7',port=5000)
