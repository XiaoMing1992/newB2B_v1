from django.db import models
import datetime

# Create your models here..
class admin_table(models.Model):
     name = models.CharField(max_length=200, default='admin')#管理员的姓名
     username = models.CharField(max_length=50, db_index=True) #账号
     password = models.CharField(max_length=200)
     add_time = models.DateTimeField(default=datetime.datetime.now()) #添加管理员的时间
     is_super_admin = models.IntegerField(default=0) #是否是超级管理员，0表示不是，1表示是

#管理成交
class manage_deal(models.Model):
    buyer_merchant_id = models.IntegerField(default=0, db_index=True) #买家公司id
    seller_merchant_id = models.IntegerField(default=0, db_index=True) #卖家公司id
    car_id = models.IntegerField(default=0) #车的id
    deal_price = models.FloatField(default=0.0) #成交价格
    deal_time = models.DateTimeField(default=datetime.datetime.now()) #成交时间

#黑名单
class black_list(models.Model):
    seller_id = models.IntegerField(default=0) #被拉黑的商家的id
    black_time = models.DateTimeField(default=datetime.datetime.now()) #拉黑时间

class activity_table(models.Model):
     admin_id = models.IntegerField(default=0, db_index=True) #登录的管理员的id
     login_time = models.DateTimeField(default=datetime.datetime.now())  #登录的时间
     IP = models.GenericIPAddressField(max_length=100, default='xxx') #登录的IP
     logout_time = models.DateTimeField(default=datetime.datetime.now())  #退出的时间

     activity_time = models.CharField(max_length=50, default='xx(h)xx(m)xx(s) ')  #活跃的时间

     login_state = models.IntegerField(default=0)  #登录的状态，0为失败，1为成功
     logout_state = models.IntegerField(default=0)  #退出的状态，0为没有登录，1为没有退出，2为正常退出，3为超时退出

     class Meta:
         ordering = ['-login_time'] #根据最新登录时间进行降序排序

class login_error_table(models.Model):
     IP = models.GenericIPAddressField(default='xxx', db_index=True) #登录的IP
     error_times = models.IntegerField(default=0)  #登录验证无效的次数
     forbid_start_time = models.DateTimeField(default=datetime.datetime.now())  #禁止开始的时间
     forbid_end_time = models.DateTimeField(default=datetime.datetime.now())  #禁止到期的时间