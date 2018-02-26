#coding=utf-8
from django.contrib.auth.hashers import make_password  #加密，解密用'pbkdf2_sha256'算法
from myadmin.models import admin_table
from myadmin.admin_tools import Admin_check
import datetime

class Set_admin(object):

    #填写注册界面，数据库插入数据
    def add_admin(self, user_name, name, password, is_super_admin=0):
        '''
        :param user_name:
        :param name:
        :param password:
        :return:成功则返回 666; 用户已经存在，返回1; 数据库插入或者查询出错，返回0
        '''
        try:
           user = admin_table.objects.filter(username=user_name)  #根据账号来查询是否已经存在该账号
           if user:
               return 1 #用户已经存在，返回1
        except:
           return 0

        try:
            #成功添加，把用户数据加密后写进数据库
            add_time = datetime.datetime.now() #注册的时间
            password_encrypt = make_password(password, None, 'pbkdf2_sha256') #加密
            admin_table.objects.create(name=name,
                                       username=user_name,
                                       password=password_encrypt,
                                       add_time=add_time,
                                       is_super_admin=is_super_admin) #保存到数据库里面

            return 666  #成功则返回 666
        except:
           return 0

    def search_admin_account(self):
        '''
        寻找的管理员为普通管理员，不是超级管理员
        :return:
        '''
        try:
            #admins = admin_table.objects.all().order_by('-add_time')

            admins = admin_table.objects.filter(is_super_admin=0).order_by('-add_time')
            admin_infos_list = []
            for i in range(len(admins)):
                admin_infos_dirct = {}
                admin_infos_dirct['id'] = admins[i].id
                admin_infos_dirct['name'] = admins[i].name
                admin_infos_dirct['account'] = admins[i].username
                admin_infos_list.append(admin_infos_dirct) #这个重要
            return admin_infos_list  #返回管理员的信息列表
        except:
            return 0

    def delete_admin(self, operation_id):
        try:
            admin_table.objects.get(id=operation_id).delete()
            return 666
        except:
            return 0

    def modify_adamin(self, username, name, oldpassword, newpassword):

        checkUser = Admin_check() #实例化
        user = checkUser.authenticate(username, oldpassword) #将用户名和旧密码进行检查，如果是对的，就把旧密码进行替换

        if user is not None:
           password_encrypt = make_password(newpassword, None, 'pbkdf2_sha256') #加密
           modify_time = datetime.datetime.now()
           #下面是更新一条记录的
           try:
              user.username = username
              user.name = name
              user.password = password_encrypt
              user.add_time = modify_time
              user.save()#保存到数据库里面
              return 666
           except:
              return 0
        else:
           return 1


    def set_super_admin(self, operation_id):
        '''
        设置超级管理员
        :param username:
        :return:
        '''
        try:
            admin = admin_table.objects.get(id=operation_id)
            admin.is_super_admin = 1
            admin.save()
            return 666
        except:
            return 0

    def find_not_super_admins(self):
        '''
        寻找普通管理员
        :param username:
        :return:
        '''
        try:
            admins = admin_table.objects.filter(is_super_admin=0).order_by('-add_time')
            admin_infos_list = []
            for i in range(len(admins)):
                admin_infos_dirct = {}
                admin_infos_dirct['id'] = admins[i].id
                admin_infos_dirct['name'] = admins[i].name
                admin_infos_dirct['username'] = admins[i].username
                admin_infos_list.append(admin_infos_dirct) #这个重要
            return admin_infos_list  #返回管理员的信息列表
        except:
            return 0