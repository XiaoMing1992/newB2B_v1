#coding=utf-8
from user.models import user_table
from django.contrib.auth.hashers import check_password #加密，解密用'pbkdf2_sha256'算法
import re
import os
from django.http import HttpResponse
from datetime import datetime

class Tools(object):
    '''
       工具类：（1）judgePhone（）函数是用来判断用户输入的电话号码是否符合规范，符合的话就返回True，否则返回False
               （2）getSession（）函数是用来获取会话的内容
               （3）delSession（）函数是用来删除会话
               (4) get_client_ip()使用django来获取用户访问的IP地址，如果用户是正常情况下,可以通过REMOTE_ADDR来获得用户的IP地址，
                   但是有些网站服务器会使用ngix等代理http，或者是该网站做了负载均衡，导致使用remote_addr抓取到的是1270.0.1，这时使用HTTP_X_FORWARDED_FOR才获得是用户的真实IP。
    '''
    #判断电话号码的合理性
    def judgePhone(self,phoneNum):
        if len(phoneNum) == 11 and re.match("^((13[0-9])|(15[^4,\\D])|(18[^4,\\D])|(14[5,7]))\\d{8}$", phoneNum) != None:
            return True
        return False

    #判断电话号码的合理性
    def judgeEmail(self,email):
        if len(email) > 7 and re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
        return False

    def get_client_ip(self, req):
         x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
         if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
         else:
            ip = req.META.get('REMOTE_ADDR')
         return ip

    #获取会话的内容
    def getSession(self,req,what):
        content = None
        if what in req.session :
            content = req.session[what]
        return content

    #获取会话的内容
    def newGetSession(self,req,what):
        content = ''
        if what in req.session :
            content = req.session[what]
        return content

    #删除会话
    def delSession(self,req,what):
        if what in req.session :
           del req.session[what]

    #处理用户上传营业执照和身份证的图片
    def upload_file(self,request,phone,file):
         return self.handle_uploaded_file(request.FILES[file],phone) #返回文件路径

    def handle_uploaded_file(self,f,phone):
       file_name = ""

       try:
          path = "user_picture/" +phone+"/checkUser/" #存放身份证和营业执照图片的路径
          if not os.path.exists(path):
            os.makedirs(path)
            file_name = path + f.name
            destination = open(file_name, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
          else:
            file_name = path + f.name
            destination = open(file_name, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
       except:
          return HttpResponse("Error")#异常，查看报错信息

       return file_name


       #处理用户上传的头像照片
    def upload_icon(self,request,phone,file):
         return self.handle_upload_icon(request.FILES[file],phone) #返回头像图片路径

    def  handle_upload_icon(self,f,phone):
       file_name = ""
       try:
          path = "static/images/" +phone+"/headIcon/" #存放头像图片的路径
          if not os.path.exists(path):
            os.makedirs(path)
            file_name = path + f.name
            destination = open(file_name, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
          else:#因为头像唯一一张图片，所以如果换新头像，需要把原来的头像删除，所以需要清空该手机号对应的文件的图片
            for item in os.listdir(path):
                itemsrc = os.path.join(path,item)
                if os.path.isfile(itemsrc):
                   try:
                    os.remove(itemsrc)
                   except:
                       return HttpResponse("删除图片Error")#异常，查看报错信息

            file_name = path + f.name
            destination = open(file_name, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
       except:
          return HttpResponse("上传头像照片出错")#异常，查看报错信息

       return file_name

    #获取文件夹里面的所有图片
    def getAllImages(self,folder):
       if not os.path.exists(folder):
          return None
       if not os.path.isdir(folder):
          return None
       imageList = os.listdir(folder)
       return imageList

    #获取文件夹里面的一幅图片
    def getOneImage(self,folder):
        if not os.path.exists(folder):
           return None
        if not os.path.isdir(folder):
           return None
        imageList = os.listdir(folder)
        #print(imageList)
        for item in imageList:
           itemsrc = os.path.join(folder,item)
        return itemsrc

    def calculate(self,time_a,time_b):
       #两个时间格式是%Y-%m-%d的时间字符串相减，返回相差的天数
       time_a = datetime.strptime(time_a,'%Y-%m-%d')
       time_b = datetime.strptime(time_b,'%Y-%m-%d')
       return (time_b-time_a).days   #返回相差的天数

    def calculate_time(self,time_a,time_b):
       #两个时间格式是%Y-%m-%d的时间字符串相减，返回相差的天数
       time_a = datetime.strptime(time_a,'%Y-%m-%d %H:%M:%S')
       time_b = datetime.strptime(time_b,'%Y-%m-%d %H:%M:%S')
       duration = (time_b-time_a)
       days, seconds = duration.days, duration.seconds
       hours = seconds // 3600
       minutes = (seconds % 3600) // 60
       seconds = (seconds % 60)
       string_time = "%d days %d hours %d minutes %d seconds"%(days,hours,minutes,seconds)
       return string_time #返回相差的时间

#登录
class LoginBackend(object):
    ''' 登录时用到此类
       （1）authenticate（）函数是用来判断用户输入的用户名和密码是否正确，正确的话就返回从数据库中获取到的记录，否则返回None
    '''
    def authenticate(self, user_name=None, password=None):
        try:
            #获取的表单数据与数据库进行比较
            user = user_table.objects.get(phone=user_name) #一个电话号码的记录只有一条，所以用get()
        except:
            try:
                user = user_table.objects.get(user_name=user_name) #一个用户名的记录只有一条，所以用get()
            except:
                return None
        flag = check_password(password, user.password)  #验证密码
        if flag:
            if user.is_black == 1:
                return 999
            else:
                return user
        else:
            #比较失败，还在login
            return None


    def authenticateByName(self, user_name=None, password=None):
         try:
            #获取的表单数据与数据库进行比较
            user = user_table.objects.get(user_name=user_name) #一个用户名的记录只有一条，所以用get()
            flag = check_password(password, user.password)  #验证密码
            if flag:
                return user
            else:
               #比较失败，还在login
               return None
         except:
            return None

