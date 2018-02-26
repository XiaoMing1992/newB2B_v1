#coding=utf-8
from django.contrib.auth.hashers import make_password #加密，解密用'pbkdf2_sha256'算法
from myadmin.admin_tools import Admin_check
from myadmin.models import admin_table

class Set_account(object):

    def checkPassword(self,username,oldpassword):
        checkUser = Admin_check() #实例化
        user = checkUser.authenticate(username, oldpassword) #将用户名和旧密码进行检查，如果是对的，就把旧密码进行替换

        if user is not None:
           return 666
        else:
           return 1

    def getUsername(self, admin_id):
        '''
        :param admin_id:
        :return: 返回用户名
        '''
        try:
            user = admin_table.objects.get(id=admin_id)
            return user.username
        except:
            return 0

    def setAccount(self, username, name, newpassword):
           try:
                #获取的表单数据与数据库进行比较
                user = admin_table.objects.get(username=username) #一个电话号码的记录只有一条，所以用get()
           except:
                return 0
           password_encrypt = make_password(newpassword, None, 'pbkdf2_sha256') #加密
           #下面是更新一条记录的
           try:
              user.password = password_encrypt
              user.name = name
              user.save()#保存到数据库里面
              return 666
           except:
              return 0

    def setAccount2(self, username, name, oldpassword, newpassword):
        '''
        :param username:
        :param name:
        :param oldpassword:
        :param newpassword:
        :return: 修改密码成功返回666；更新数据库出错，返回0；用户不存在，返回1
        '''

        checkUser = Admin_check() #实例化
        user = checkUser.authenticate(username, oldpassword) #将用户名和旧密码进行检查，如果是对的，就把旧密码进行替换

        if user is not None:
           password_encrypt = make_password(newpassword, None, 'pbkdf2_sha256') #加密
           #下面是更新一条记录的
           try:
              user.password = password_encrypt
              user.name = name
              user.save()#保存到数据库里面
              return 666
           except:
              return 0
        else:
           return 1

