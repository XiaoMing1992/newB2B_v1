#coding=utf-8
from account.models import inviteCode_table
from user.models import inviteCode_error_table
import datetime

class Invite_code(object):

    #输入邀请码进行注册
    def mangageInviteCode(self,inviteCode,user_ip):
        '''
        :param req:
        :param inviteCode:
        :return: #成功，则返回符合条件的电话号码集合phones; 邀请码过期，返回1; 邀请码不存在或者有错，返回2; 数据库查询出错，返回0;锁住IP，返回404
        '''
        now_time = datetime.datetime.now()   #现在时间

        #下面是验证用户是否处于受禁状态
        try:
             #利用datetime.datetime.now()得到的当前时间是offset-naive的，而另外一个却是offset-aware的，因此我们需要将这里的dt转成与now一样的形式
             # 可以这么做： .replace(tzinfo=None)

             error = inviteCode_error_table.objects.get(IP=user_ip) #获取记录
             forbid_end_time = error.forbid_end_time.replace(tzinfo=None)
             if error.error_times > 5 and forbid_end_time > now_time: #验证无效次数连续大于5次，并且1小时还没有过去，该ip仍然处于受禁状态
                 return 404  #锁住IP，返回404
             elif error.error_times > 5 and forbid_end_time <= now_time: #该ip受禁到期，可以继续操作
                 error.error_times = 0 #重置验证无效次数为0
                 error.save()
        except inviteCode_error_table.DoesNotExist:
                 goto=True  #inviteCode_error_table中不存在该用户，说明该用户第一次输入，跳过,继续验证
        except:
                return 0

        #将获取的表单数据与数据库进行比较
        try:
            user = inviteCode_table.objects.filter(inviteCode=inviteCode)

            if user:
                goto = True
            else: #验证无效
                try:
                     error = inviteCode_error_table.objects.get(IP=user_ip) #获取记录
                     error.error_times = error.error_times+1
                     if error.error_times > 5: #验证无效次数连续大于5次
                         forbid_start_time = datetime.datetime.now()   #禁止开始的时间
                         forbid_end_time = datetime.datetime.now()+datetime.timedelta(minutes=60)  #禁止到期的时间
                         error.forbid_start_time = forbid_start_time
                         error.forbid_end_time = forbid_end_time
                     error.save()
                except:
                     try:
                         inviteCode_error_table.objects.create(IP=user_ip, error_times=1) #插入登录记录
                     except:
                         return 0
                if inviteCode == '':
                    return 3  #邀请码为空
                return 2 #邀请码不存在

             #利用datetime.datetime.now()得到的当前时间是offset-naive的，而另外一个却是offset-aware的，因此我们需要将这里的dt转成与now一样的形式
             # 可以这么做： .replace(tzinfo=None)
            t1 = datetime.datetime.now()
            phones = []
            for i in range(len(user)):
                t2 = user[i].validity_time.replace(tzinfo=None)
                if t1 <= t2:  #比较当前时间与邀请码有效期
                    phones.append(user[i].receive_phone)
            if phones:
                return phones  #成功，则返回符合条件的电话号码集合phones

            else: #验证无效
                try:
                     error = inviteCode_error_table.objects.get(IP=user_ip) #获取记录
                     error.error_times = error.error_times+1
                     if error.error_times > 5: #验证无效次数连续大于5次
                         forbid_start_time = datetime.datetime.now()  #禁止开始的时间
                         forbid_end_time = datetime.datetime.now()+datetime.timedelta(minutes=60)  #禁止到期的时间
                         error.forbid_start_time = forbid_start_time
                         error.forbid_end_time = forbid_end_time
                     error.save()
                except:
                     try:
                         inviteCode_error_table.objects.create(IP=user_ip, error_times=1) #插入登录记录
                     except:
                         return 0
                return 1    #邀请码过期，返回1
        except:
            return 0





