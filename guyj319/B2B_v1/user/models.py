from django.db import models
import datetime

# Create your models here.
class user_table(models.Model):
     user_name = models.CharField(max_length=100, default='xxx')          #用户名
     phone = models.CharField(max_length=15, db_index=True) #phone_number
     password = models.CharField(max_length=500)
     email = models.EmailField(default='xxxx@xx.com')
     reg_time = models.DateTimeField(default=datetime.datetime.now())  #注册的时间
     IP = models.GenericIPAddressField(max_length=100, default='xxx') #注册的IP

     is_vip = models.IntegerField(default=0) #判断用户是否会员，1表示是会员，0表示不是会员
     is_black = models.IntegerField(default=0) #判断商家是否已经被拉黑，1表示已经被拉黑
     black_time = models.DateTimeField(default=datetime.datetime.now()) #拉黑时间

class activity_table(models.Model):
     user_id = models.IntegerField(default=0, db_index=True) #当前用户的id
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

#处理邀请码输入错误，防攻击
class inviteCode_error_table(models.Model):
     IP = models.GenericIPAddressField(default='xxx', db_index=True) #登录的IP
     error_times = models.IntegerField(default=0)  #登录验证无效的次数
     forbid_start_time = models.DateTimeField(default=datetime.datetime.now())  #禁止开始的时间
     forbid_end_time = models.DateTimeField(default=datetime.datetime.now())  #禁止到期的时间