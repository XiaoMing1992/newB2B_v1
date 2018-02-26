#coding=utf-8
import pymysql
pymysql.install_as_MySQLdb()

import time
import os, sys, string
def CallProc(id,onlinetime):
    '''调用存储过程，
    输入参数：编号，在线时间，输出：帐号，密码;
    使用输出参数方式'''
    accname=''
    accpwd=''
    conn=pymysql.Connect(db='b2b_v1',user='root',password='12353051',host='localhost',port=3308)
    cur =conn.cursor()
    cur.callproc('proctest',(id,onlinetime,accname,accpwd))
    cur.execute('select @_proctest_2,@_proctest_3')
    data=cur.fetchall()
    if data:
       for rec in data:
           accname=rec[0]
           accpwd=rec[1]
       cur.close()
       conn.close()
    return accname,accpwd

def InviteCode(invitecode):
    '''调用存储过程，
    输入参数：编号，在线时间，输出：帐号，密码;
    使用输出参数方式'''
    accname=''
    accpwd=''
    conn=pymysql.Connect(db='b2b_v1',user='root',password='12353051',host='localhost',port=3308)
    cur =conn.cursor()
    cur.callproc('invite_code',(invitecode,accname,accpwd))
    cur.execute('select @_invite_code_1,@_invite_code_2')
    data=cur.fetchall()
    list=[]
    if data:
       for rec in data:
           accname=rec[0]
           accpwd=rec[1]
           list.append(accname)
           list.append(accpwd)
       cur.close()
       conn.close()
    return list

def Proc_Login(username):
    '''调用存储过程，
    输入参数：编号，在线时间，输出：帐号，密码;
    使用输出参数方式'''
    accname=''
    pw=''
    conn=pymysql.Connect(db='b2b_v1',user='root',password='12353051',host='localhost',port=3308)
    cur =conn.cursor()
    cur.callproc('login',(username,pw))
    cur.execute('select @_login_1')
    data=cur.fetchall()
    if data:
       for rec in data:
           pw=rec[0]
       cur.close()
       conn.close()
    return pw

if __name__ == '__main__':
    name,pw=CallProc(1,0)
    print(name,pw)
    pw=Proc_Login(13631257700)
    print(pw)
    list=InviteCode('')
    print(list)
