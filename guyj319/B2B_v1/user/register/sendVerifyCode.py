# -*- coding: utf-8 -*-
import random
import urllib
import urllib.request

user_name = 'dxwpanxl6'
password = '383327083D8885F263CED4C33681'

class Send_verify_code(object):
    #获取验证码的值
    def initVerifyCodeVal(self,length=4):
        codes = ['0','1','2','3','4','5','6','7','8','9']
        code_str = ''

        for i in range(0,length):
            temp = codes[random.randint(0,9)]  #random.randint()的函数原型为：random.randint(a, b)，用于生成一个指定范围内的整数。其中参数a是下限，参数b是上限，生成的随机数n: a <= n <= b
            code_str += temp
        return {'cstr':code_str}

    #获取校验码，并返回给浏览器
    def getVerifyCode(self):

        #验证码的长度
        length = 4
        #获取到验证码的值
        code_dict = Send_verify_code.initVerifyCodeVal(length)
        #取出字符串类型的验证码值
        rand_str = code_dict['cstr']
        return rand_str #返回验证码

    # 在Python 3.X中，urllib2 用 urllib.request表示，urllib2 和 urllib 合并成 urllib

    #发送验证码
    def sendVerifyCode(self,phone_number,verifyCode):

        prefix = urllib.parse.quote('【车栈网】您的验证码为：')
        suffix = urllib.parse.quote(',请勿转发给其他人。')

        url = 'http://web.duanxinwang.cc/asmx/smsservice.aspx?name=' + user_name\
              + '&pwd=' + password + '&content='\
              + prefix + verifyCode + suffix+\
              '&mobile=' + phone_number + '&stime=&sign=&type=pt&extno='
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        content = resp.read()
        if(content):
             print(content)
             return True
        return False

