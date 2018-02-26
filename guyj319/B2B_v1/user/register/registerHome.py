#coding=utf-8
from django.contrib.auth.hashers import make_password  #加密，解密用'pbkdf2_sha256'算法
from user.models import user_table
from user.models import activity_table
import datetime

class Register(object):

    #填写注册界面，数据库插入数据
    def register(self, user_name, phone, password, user_ip):
        '''
        :param user_name:
        :param phone:
        :param password:
        :param user_ip:
        :return: 成功则返回用户的id; 用户已经存在，返回1; 数据库插入或者查询出错，返回0
        '''
        try:
           user = user_table.objects.filter(phone=phone)  #根据手机号来查询是否已经存在该手机号
           if user:
               return -1 #用户已经存在，返回1
           user = user_table.objects.filter(user_name=user_name) #根据用户名来查询是否已经存在该用户名
           if user:
               return -1 #用户已经存在，返回1
        except:
           return 0

        try:
            #成功注册，把用户数据加密后写进数据库
            reg_time = datetime.datetime.now() #注册的时间
            password_encrypt = make_password(password, None, 'pbkdf2_sha256') #加密
            user = user_table.objects.create(user_name=user_name,
                                      phone=phone,
                                      password=password_encrypt,
                                      IP=user_ip,
                                      reg_time=reg_time) #保存到数据库里面
            return user.id  #成功则返回 用户的id
        except:
           return 0

    def finishRegister(self, user_ip, user_id):
        '''
        :param user_ip:
        :param user_id:
        :return:数据库操作失败，返回0；注册成功，返回 temp_user.id
        '''
        try:
            login_time = datetime.datetime.now()  #登录的时间
            temp_user = activity_table.objects.create(user_id=user_id,
                                                      login_time=login_time,
                                                      IP=user_ip,
                                                      login_state=1,
                                                      logout_state=1) #插入登录记录
            return temp_user.id #注册成功，返回 temp_user.id
        except:
            return 0
