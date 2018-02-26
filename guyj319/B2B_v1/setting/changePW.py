#coding=utf-8
from django.contrib.auth.hashers import make_password #加密，解密用'pbkdf2_sha256'算法
from django.contrib.auth.hashers import check_password #加密，解密用'pbkdf2_sha256'算法
from account.account_manage import LoginBackend
from user.models import user_table

class Change_password(object):

    def changePassword(self, user_id, newpassword,email = ''):
           try:
                #获取的表单数据与数据库进行比较
                user = user_table.objects.get(id=user_id) #一个电话号码的记录只有一条，所以用get()
           except:
                return 0
           password_encrypt = make_password(newpassword, None, 'pbkdf2_sha256') #加密
           #下面是更新一条记录的
           try:
              user.password = password_encrypt
              user.email = email
              user.save()#保存到数据库里面
              return 666
           except:
              return 0

    def checkPassword(self, user_id, oldpassword):
        try:
           user = user_table.objects.get(id=user_id)
           flag = check_password(oldpassword, user.password)  #验证密码
           if flag:
               return 666
           else:
               return 1
        except:
            return 0

    def changePassword2(self,current_user_phone_number,oldpassword,newpassword,email):
        '''
        :param current_user_phone_number:
        :param oldpassword:
        :param newpassword:
        :return: 修改密码成功返回666；更新数据库出错，返回0；用户不存在，返回1
        '''

        checkUser = LoginBackend() #实例化
        user = checkUser.authenticate(current_user_phone_number, oldpassword) #将用户名和旧密码进行检查，如果是对的，就把旧密码进行替换

        if user is not None:
           password_encrypt = make_password(newpassword, None, 'pbkdf2_sha256') #加密
           #下面是更新一条记录的
           try:
              user.password = password_encrypt
              user.email = email
              user.save()#保存到数据库里面
              return 666
           except:
              return 0
        return 1
