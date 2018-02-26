#coding=utf-8

class LoginStatus():
    SERVER_ERROR = 0           #服务器出错
    WRONG = -1                 #返回1表示手机号或者密码有错
    ERROR_EXCEED = -404        #登录时，错误次数超过6次，锁住IP，返回404
    IS_BLACK = -999            #该账号已经被拉黑
    #SUCCESS = -999

