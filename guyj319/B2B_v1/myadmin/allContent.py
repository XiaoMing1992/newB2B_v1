#coding=utf-8
from account.models import user_info_table
from account.models import user_info_people
from car.models import car_table
from car.models import invalid_time_car_table
import datetime

class ContentHome(object):
    def content_list(self, kind=0):
        '''
        kind为0，是全部会员；为1，为认证会员；为2，为未认证会员；为3，为无效会员。
        :param kind:
        :return:
        '''
        try:
            #is_black=0，表示该会员没有被拉黑，全部会员页面显示的应该是没有被拉黑的会员
            if kind == 1:
               user = user_info_table.objects.filter(is_black=0, state=1).order_by('-add_time')
            elif kind == 2:
               user = user_info_table.objects.filter(is_black=0, state=0).order_by('-add_time')
            elif kind == 3:
               user = user_info_table.objects.filter(is_black=0, state=2).order_by('-add_time')
            else:
               user = user_info_table.objects.filter(is_black=0).order_by('-add_time')

            content_list = []
            for i in range(len(user)):
                content_dirct = {}
                content_dirct['company_name'] = user[i].user_company_name
                content_dirct['region'] = user[i].user_address
                content_dirct['brands'] = user[i].user_trademark
                content_dirct['status'] = user[i].state
                content_dirct['id'] = user[i].id

                people = user_info_people.objects.filter(merchant_id=user[i].id)
                people_list = []
                for j in range(len(people)):
                    people_dirct = {}
                    people_dirct['contact'] = people[j].user_name
                    people_dirct['phone_number'] = people[j].user_phone
                    people_list.append(people_dirct)

                content_dirct['peoples'] = people_list
                #=====================================临时===================
                content_dirct['contact'] = people[0].user_name
                content_dirct['phone_number'] = people[0].user_phone
                #=====================================临时===================
                content_list.append(content_dirct)
            return content_list
        except:
            return 0

    def modify_vip(self, operation_id):
        try:
            user = user_info_table.objects.get(id=operation_id)
            content_dirct = {}
            content_dirct['company_name'] = user.user_company_name
            content_dirct['type'] = user.user_type
            content_dirct['region'] = user.user_address
            content_dirct['brands'] = user.user_trademark
            content_dirct['status'] = user.state
            content_dirct['id'] = user.id
            content_dirct['license_image_path'] = user.license_path.url
            content_dirct['id_card_image_path'] = user.id_card_path.url

            people = user_info_people.objects.filter(merchant_id=user.id)
            people_list = []
            for j in range(len(people)):
                people_dirct = {}
                people_dirct['contact'] = people[j].user_name
                people_dirct['phone_number'] = people[j].user_phone
                people_list.append(people_dirct)

            content_dirct['peoples'] = people_list
            #=====================================临时===================
            content_dirct['contact'] = people[0].user_name
            content_dirct['phone_number'] = people[0].user_phone
            #=====================================临时===================
            return content_dirct
        except:
            return 0

    def delete_vip_one_by_one(self, merchant_id):
        '''
         一个个删除
        :param merchant_id:
        :return:
        '''
        try:
            user_info_table.objects.get(id=merchant_id).delete()
            user_info_people.objects.filter(merchant_id=merchant_id).delete()

            car_table.objects.filter(merchant_id=merchant_id).delete()
            invalid_time_car_table.objects.filter(merchant_id=merchant_id).delete()

            return 666
        except:
            return 0

    def delete_vip_some(self, merchant_id_list):
        '''
        批量删除
        :param merchant_id_list:
        :return:
        '''
        try:
            user_info_table.objects.filter(id__in=merchant_id_list).delete()
            user_info_people.objects.filter(merchant_id__in=merchant_id_list).delete()

            car_table.objects.filter(merchant_id__in=merchant_id_list).delete()
            invalid_time_car_table.objects.filter(merchant_id__in=merchant_id_list).delete()
            return 666
        except:
            return 0

    def delete_vip_all(self):
        '''
        全部删除
        :return:
        '''
        try:
            user_info_table.objects.all().delete()
            user_info_people.objects.all().delete()

            car_table.objects.all().delete()
            invalid_time_car_table.objects.all().delete()
            return 666
        except:
            return 0
