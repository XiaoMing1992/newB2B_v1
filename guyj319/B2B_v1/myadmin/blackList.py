#coding=utf-8
from account.models import user_info_table
from account.models import user_info_people
from user.models import user_table
from car.models import car_table
from car.models import invalid_time_car_table
import datetime

class BlackList(object):

    def get_black_list(self, kind=0):
        '''
        kind为0，是全部会员；为1，为认证会员；为2，为未认证会员；为3，为无效会员。
        :param kind:
        :return:
        '''
        try:
            #is_black=1，表示该会员已经被拉黑
            if kind == 1:
               user = user_info_table.objects.filter(is_black=1, state=1).order_by('-add_time')
            elif kind == 2:
               user = user_info_table.objects.filter(is_black=1, state=0).order_by('-add_time')
            elif kind == 3:
               user = user_info_table.objects.filter(is_black=1, state=2).order_by('-add_time')
            else:
               user = user_info_table.objects.filter(is_black=1).order_by('-add_time')

            black_list = []
            for i in range(len(user)):
                black_dirct = {}
                black_dirct['id'] = user[i].id
                black_dirct['company_name'] = user[i].user_company_name
                black_dirct['region'] = user[i].user_address

                freeze_date = {}
                freeze_date['year'] = user[i].black_time.year
                freeze_date['month'] = user[i].black_time.month
                freeze_date['day'] = user[i].black_time.day
                black_dirct['freeze_date'] = freeze_date

                people = user_info_people.objects.filter(merchant_id=user[i].id)
                people_list = []
                for j in range(len(people)):
                    people_dirct = {}
                    people_dirct['contact'] = people[j].user_name
                    people_dirct['phone_number'] = people[j].user_phone
                    people_list.append(people_dirct)

                black_dirct['peoples'] = people_list

                #=====================================临时===================
                black_dirct['contact'] = people[0].user_name
                black_dirct['phone_number'] = people[0].user_phone
                #=====================================临时===================

                black_list.append(black_dirct)
            return black_list
        except:
            return 0

    def delete_black_one_by_one(self, merchant_id):
        '''
        一个个更新
        :param merchant_id:
        :return:
        '''
        try:
            #恢复恢复用户信息
            user1 = user_info_table.objects.get(id=merchant_id)
            user_id = user1.user_id
            user1.is_black = 0
            #user1.black_time = datetime.datetime.now()
            user1.save()

            #恢复卖家信息
            user2 = user_table.objects.get(id=user_id)
            user2.is_black = 0
            #user2.black_time = datetime.datetime.now()
            user2.save()

            #恢复车源
            car_table.objects.filter(merchant_id=merchant_id).update(is_black=0)
            invalid_time_car_table.objects.filter(merchant_id=merchant_id).update(is_black=0)

            return 666
        except:
            return 0

    def delete_black_some(self, merchant_id_list):
        '''
        批量更新
        :param merchant_id_list:
        :return:
        '''
        try:
            #恢复恢复用户信息
            users = user_info_table.objects.filter(id__in=merchant_id_list).update(is_black=0)

            #恢复卖家信息
            user_ids = []
            for i in range(len(users)):
                user_ids.append(users[i].user_id)
            user_table.objects.filter(id__in=user_ids).update(is_black=0)

            #恢复车源
            car_table.objects.filter(merchant_id__in=merchant_id_list).update(is_black=0)
            invalid_time_car_table.objects.filter(merchant_id__in=merchant_id_list).update(is_black=0)

            return 666
        except:
            return 0

    def delete_black_all(self):
        '''
         全部更新
        :return:
        '''
        try:
            #恢复恢复用户信息
            users = user_info_table.objects.all().update(is_black=0)

            #恢复卖家信息
            user_ids = []
            car_table_merchant_ids = []
            for i in range(len(users)):
                user_ids.append(users[i].user_id)
                car_table_merchant_ids.append(users[i].id)
            user_table.objects.filter(id__in=user_ids).update(is_black=0)

            #恢复车源
            car_table.objects.filter(merchant_id__in=car_table_merchant_ids).update(is_black=0)
            invalid_time_car_table.objects.filter(merchant_id__in=car_table_merchant_ids).update(is_black=0)

            return 666
        except:
            return 0

    def get_black_list_num(self):
        try:
            num = user_info_table.objects.filter(is_black=1).count()
            return num
        except:
            return -1