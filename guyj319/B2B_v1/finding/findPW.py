#coding=utf-8
from user.models import user_table
from django.contrib.auth.hashers import make_password#加密，解密用'pbkdf2_sha256'算法

class Find_password(object):

    def phoneIsExist(self, phone):
        '''
        :param phone:
        :return: 如果电话号码不存在，返回0；否则，返回666
        '''
        try:
            #获取的表单数据与数据库进行比较
            user = user_table.objects.get(phone=phone) #一个电话号码的记录只有一条，所以用get()
            if user.is_black == 0:
                return 666 #已经存在
            else:
                return 999 #已经被拉黑
        except:
            return 0 #不存在

    def findPWByPhone(self, phone, newpassword):
        '''
        :param phone:
        :param newpassword:
        :return: 修改密码成功返回666；更新数据库出错，返回0
        '''
        try:
            user = user_table.objects.get(phone=phone)
            password_encrypt = make_password(newpassword, None, 'pbkdf2_sha256') #加密
            user.password = password_encrypt
            user.save()#保存到数据库里面
            return 666
        except:
            return 0

    def findPWByEmail(self,email,newpassword):
        '''
        :param email:
        :param newpassword:
        :return: 修改密码成功返回666；更新数据库出错，返回0
        '''
        try:
            user = user_table.objects.get(email=email)
            password_encrypt = make_password(newpassword, None, 'pbkdf2_sha256') #加密
            user.password = password_encrypt
            user.save()#保存到数据库里面
            return 666
        except:
            return 0



