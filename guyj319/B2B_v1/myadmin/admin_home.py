# coding=utf-8
from myadmin.models import admin_table
from user.models import user_table
import datetime

class Home(object):
     def is_super_admin(self, admin_id):
         try:
             admin = admin_table.objects.get(id=admin_id)
             if admin.is_super_admin == 0:
                 return 1
             else:
                 return 666
         except:
             return 0

     def get_new_user_num(self):
         '''
         新用户 = reg_time+7＞= now
         :return: 新用户的个数
         '''
         try:
             now_time = datetime.datetime.now()-datetime.timedelta(days=7)
             num = user_table.objects.filter(reg_time__gt=now_time).count()
             return num
         except:
             return -1