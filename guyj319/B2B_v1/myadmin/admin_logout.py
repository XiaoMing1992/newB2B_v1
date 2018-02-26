#coding=utf-8
from myadmin.models import activity_table
import datetime

class Logout(object):

    def logout(self, login_id, admin_id):
        '''
        :param login_id:
        :param admin_id:
        :return: 正常更新，返回666；更新出错，返回0
        '''
        try:
            user = activity_table.objects.get(id=login_id, admin_id=admin_id)

            exit_time = datetime.datetime.now()
            user.logout_time = exit_time   #登录退出的时间

            #计算活动时间
            #利用datetime.datetime.now()得到的当前时间是offset-naive的，而另外一个却是offset-aware的，因此我们需要将这里的dt转成与now一样的形式
            # 可以这么做： .replace(tzinfo=None)
            login_time = user.login_time.replace(tzinfo=None)
            time_delta = (exit_time - login_time)
            hour = int(time_delta.seconds/3600)
            minute = int((time_delta.seconds - hour*3600)/60)
            second = time_delta.seconds%60
            user.activity_time = str(hour)+'(h)'+str(minute)+'(m)'+str(second)+'(s)'  #用户活跃的时间

            user.logout_state = 2 #正常退出
            user.save()
            return 666
        except:
            return 0
