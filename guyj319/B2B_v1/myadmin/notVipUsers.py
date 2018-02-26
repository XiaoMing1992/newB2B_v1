#coding=utf-8
from account.models import user_info_table
from account.models import user_info_people
from user.models import user_table
from car.models import car_table
from car.models import invalid_time_car_table
import datetime

class NotVipUsers(object):
    def get_not_vip_users(self):
        try:
            #is_black=0，表示该该用户没有被拉黑，全部会员页面显示的应该是没有被拉黑的会员
            user = user_table.objects.filter(is_black=0, is_vip=0).order_by('-reg_time')
            users_list = []
            for i in range(len(user)):
                users_dirct = {}
                users_dirct['user_name'] = user[i].user_name
                users_dirct['phone'] = user[i].phone
                users_dirct['email'] = user[i].email
                users_dirct['reg_time'] = user[i].reg_time
                users_dirct['IP'] = user[i].IP
                users_dirct['id'] = user[i].id

                users_list.append(users_dirct)
            return users_list
        except:
            return 0

    def delete_user_one_by_one(self, user_id):
        '''
        一个个删除
        :param user_id:
        :return:
        '''
        try:
            user_table.objects.get(id=user_id).delete()
            return 666
        except:
            return 0

    def delete_user_some(self, user_id_list):
        '''
        批量删除
        :param user_id_list:
        :return:
        '''
        try:
            user_table.objects.filter(id__in=user_id_list).delete()
            return 666
        except:
            return 0

    def delete_user_all(self):
        '''
         全部删除
        :return:
        '''
        try:
            user_info_table.objects.filter(is_vip=0).delete()
            #user_info_table.objects.filter(is_vip__ne=1).delete() #ne 表示不等于
            return 666
        except:
            return 0

    def black_user(self, user_id):
        '''
        拉黑用户
        :param user_id:
        :return:
        '''
        try:
            user = user_table.objects.get(id=user_id)
            user.is_black = 1
            user.black_time = datetime.datetime.now()
            user.save()

            return 666
        except:
            return 0

    def remove_black(self, user_id):
        '''
        移除拉黑
        :param user_id:
        :return:
        '''
        try:
            user = user_table.objects.get(id=user_id)
            user.is_black = 0
            user.black_time = datetime.datetime.now()
            user.save()

            return 666
        except:
            return 0