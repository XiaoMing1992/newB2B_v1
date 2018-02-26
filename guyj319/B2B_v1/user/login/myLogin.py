#coding=utf-8
from account.account_manage import LoginBackend
from user.models import activity_table, login_error_table
import datetime
from user.LoginStatus import LoginStatus

class Login(object):

    def login(self,user_ip,user_name,password):
          '''
          :param user_ip:
          :param user_name:
          :param password:
          :return: 验证成功，返回 phone; 验证失败，返回1; 数据库操作错误，返回0；锁住IP，返回404
          '''

          now_time = datetime.datetime.now()   #现在时间

          #下面是验证用户是否处于受禁状态
          try:
             #利用datetime.datetime.now()得到的当前时间是offset-naive的，而另外一个却是offset-aware的，因此我们需要将这里的dt转成与now一样的形式
             # 可以这么做： .replace(tzinfo=None)

             error = login_error_table.objects.get(IP=user_ip) #获取记录
             forbid_end_time = error.forbid_end_time.replace(tzinfo=None)
             if error.error_times > 5 and forbid_end_time > now_time: #验证无效次数连续大于5次，并且1小时还没有过去，该ip仍然处于受禁状态
                 return LoginStatus.ERROR_EXCEED  #锁住IP，返回-404
             elif error.error_times > 5 and forbid_end_time <= now_time: #该ip受禁到期，可以继续操作
                 error.error_times = 0 #重置验证无效次数为0
                 error.save()
          except login_error_table.DoesNotExist:
                 goto = True  #login_error_table中不存在该用户，说明该用户第一次登陆，跳过,继续验证
          except:
                return 0

          loginBackend = LoginBackend() #实例化
          user = loginBackend.authenticate(user_name, password) #调用其验证函数验证用户是否输入正确
          if user == 999:
              return LoginStatus.IS_BLACK
          elif user is not None:
              return user.id
          else:#验证无效
                try:
                     error = login_error_table.objects.get(IP=user_ip) #获取记录
                     error.error_times = error.error_times+1
                     if error.error_times > 5: #验证无效次数连续大于5次
                         forbid_start_time = datetime.datetime.now()   #禁止开始的时间
                         forbid_end_time = datetime.datetime.now()+datetime.timedelta(minutes=60)   #禁止到期的时间
                         error.forbid_start_time = forbid_start_time
                         error.forbid_end_time = forbid_end_time

                     error.save()
                     return -1  #验证失败，返回0
                except:
                     try:
                         login_error_table.objects.create(IP=user_ip, error_times=1) #插入登录记录
                     except:
                         return 0


    def activity_log(self, user_id, user_ip):
        '''
        :param user_id:
        :param user_ip:
        :return:
        '''
        try:
            login_time = datetime.datetime.now()   #登录的时间
            temp_user = activity_table.objects.create(user_id=user_id,
                                                      login_time=login_time,
                                                      IP=user_ip,
                                                      login_state=1,
                                                      logout_state=1) #插入登录记录
            return temp_user.id #验证成功，返回 id
        except:
            return 0
