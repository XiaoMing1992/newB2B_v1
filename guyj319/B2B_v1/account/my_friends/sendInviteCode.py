# -*- coding: utf-8 -*-
import random
import urllib
import urllib.request

user_name = 'dxwpanxl6'
password = '383327083D8885F263CED4C33681'

class Send_invite_code(object):

    #邀请码生成
    def initInviteCodeVal(self,length=6):
        codes = ['0','1','2','3','4','5','6','7','8','9',
        'a','b','c','d','e','f','g','h','i','j',
        'k','m','n','o','p','q','r','s','t','u',
        'v','w','x','y','z','A','B','C','D','E',
        'F','G','H','I','J','K','L','M','N','O',
        'P','Q','R','S','T','U','V','W','X','Y',
        'Z']
        code_str = ''

        for i in range(0,length):
            temp = codes[random.randint(0,60)]  #random.randint()的函数原型为：random.randint(a, b)，用于生成一个指定范围内的整数。其中参数a是下限，参数b是上限，生成的随机数n: a <= n <= b
            code_str += temp
        return {'cstr':code_str}

    #获取邀请码，并返回给浏览器
    def getInviteCode(self):

        #邀请码的长度
        length = 6
        #获取到验证码的值
        code_dict = Send_invite_code.initInviteCodeVal(length)
        #取出字符串类型的验证码值
        rand_str = code_dict['cstr']
        return rand_str

    #发送邀请码
    def sendInviteCode(self,phone_number,invitation_code):

        prefix = urllib.parse.quote('【车栈网】您的邀请码为：')
        suffix = urllib.parse.quote(',请勿转发给其他人。')

        url = 'http://web.duanxinwang.cc/asmx/smsservice.aspx?name=' + user_name\
              + '&pwd=' + password + '&content='\
              + prefix + invitation_code + suffix+\
              '&mobile=' + phone_number + '&stime=&sign=&type=pt&extno='
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        content = resp.read()
        if(content):
             return True
        return False