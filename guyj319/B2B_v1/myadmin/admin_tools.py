#coding=utf-8
from .models import admin_table
from django.contrib.auth.hashers import check_password #加密，解密用'pbkdf2_sha256'算法

#登录
class Admin_check(object):
    ''' 登录时用到此类
       （1）authenticate（）函数是用来判断用户输入的用户名和密码是否正确，正确的话就返回从数据库中获取到的记录，否则返回None
    '''

    def authenticate(self, username=None, password=None):
         try:
            #获取的表单数据与数据库进行比较
            user = admin_table.objects.get(username=username) #一个电话号码的记录只有一条，所以用get()
            flag = check_password(password, user.password)  #验证密码
            if flag:
                return user
            else:
                return None
         except:
            return None


class Admin_tools(object):

    #获取会话
    def getSession(self, req, what):
        username = None
        if what in req.session:
            username = req.session[what]
        return username

    #删除会话
    def delSession(self,req,what):
        if what in req.session:
           del req.session[what]

    def get_client_ip(self,req):
         x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
         if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
         else:
            ip = req.META.get('REMOTE_ADDR')
         return ip


