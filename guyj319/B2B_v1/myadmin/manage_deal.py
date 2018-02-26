#coding=utf-8
from myadmin.models import manage_deal
from car.models import car_table
from car.models import car_table_people
from account.models import user_info_table
from account.models import user_info_people
import datetime

class Deal(object):
    def get_all_deal_records(self):
        try:
            records = manage_deal.objects.all().order_by("-deal_time")
            records_list = []
            for i in range(len(records)):
                records_dirct = {}
                records_dirct['buyer_merchant_id'] = records[i].buyer_merchant_id
                records_dirct['seller_merchant_id'] = records[i].seller_merchant_id
                records_dirct['deal_price'] = records[i].deal_price

                time = {}
                time['year'] = records[i].deal_time.year
                time['month'] = records[i].deal_time.month
                time['day'] = records[i].deal_time.day
                time['hour'] = records[i].deal_time.hour
                time['minute'] = records[i].deal_time.minute
                time['second'] = records[i].deal_time.second
                records_dirct['deal_time'] = time


                series_detail = {}
                delivery_date = {}       #交货时间
                out_date = {}            #过期
                price = {}
                source_detail_list = {}

                car = car_table.objects.get(id=records[i].car_id)
                delivery_time = car.delivery_time             #交货时间
                delivery_date['year'] = delivery_time.year        #交货时间的年份
                delivery_date['month'] = delivery_time.month      #交货时间的月份
                delivery_date['day'] = delivery_time.day          #交货时间的天数

                out_time = car.date_valid           #车的有效期
                out_date['year'] = out_time.year        #过期的年份
                out_date['month'] = out_time.month      #过期的月份
                out_date['day'] = out_time.day          #过期的天数

                price['lowest_price'] = car.lowest_price                #最低报价
                price['highest_price'] = car.highest_price               #最高报价

                source_detail_list["series_detail"] = series_detail                   #车型
                source_detail_list["price"] = price                                   #报价
                source_detail_list["delivery_date"] = delivery_date                   #交货时间
                source_detail_list["out_date"] = out_date                             #过期

                series_detail['brand'] = car.car_brand                            #品牌
                series_detail['displacement'] = car.car_series                    #车系
                series_detail['other'] = car.car_model                            #车款

                source_detail_list["id"] = car.id                                 #车的id
                source_detail_list['carType'] = car.car_type                      #车辆类型
                source_detail_list['color'] = car.color                           #颜色
                source_detail_list['color_hex'] = car.color_hex                   #颜色的16进制，先占位
                source_detail_list['delivery_type'] = car.delivery_type           #期货类型
                source_detail_list['payType'] = car.pay_method                    #付款方式
                source_detail_list["saleRegion"] = car.sell_area                  #销售区域
                source_detail_list['logisticsType'] = car.method_logistics        #物流方式
                source_detail_list['remark'] = car.introduction                   #备注说明

                people = car_table_people.objects.filter(car_id=records[i].car_id)
                people_list = []
                for j in range(len(people)):
                    people_dirct = {}
                    people_dirct['name'] = people[j].people_name
                    people_dirct['phone'] = people[j].people_phone
                    people_list.append(people_dirct)

                source_detail_list['peoples'] = people_list
                records_dirct['source_detail_list'] = source_detail_list

                records_list.append(records_dirct)
            return records
        except:
            return 0

    def get_all_user_info_list(self):
        try:
            #is_black=0，表示该会员没有被拉黑，全部会员页面显示的应该是没有被拉黑的会员
            user = user_info_table.objects.filter(is_black=0).order_by('-add_time')
            user_info_list = []
            for i in range(len(user)):
                user_info_dirct = {}
                user_info_dirct['company_name'] = user[i].user_company_name
                user_info_dirct['region'] = user[i].user_address
                user_info_dirct['user_trademark'] = user[i].user_trademark
                user_info_dirct['state'] = user[i].state
                user_info_dirct['id'] = user[i].id

                people = user_info_people.objects.filter(merchant_id=user[i].id)
                people_list = []
                for j in range(len(people)):
                    people_dirct = {}
                    people_dirct['name'] = people[j].user_name
                    people_dirct['phone'] = people[j].user_phone
                    people_list.append(people_dirct)

                user_info_dirct['peoples'] = people_list

                user_info_list.append(user_info_dirct)
            return user_info_list
        except:
            return 0


    def get_each_user_info_list(self, merchant_id):
        try:
            user = user_info_table.objects.get(id=merchant_id)

            merchant_dirct = {}
            merchant_dirct['id'] = user.id
            merchant_dirct['company_name'] = user.user_company_name
            merchant_dirct['region'] = user.user_address
            merchant_dirct['user_trademark'] = user.user_trademark

            people = user_info_people.objects.filter(merchant_id=merchant_id)
            people_list = []
            for j in range(len(people)):
                people_dirct = {}
                people_dirct['name'] = people[j].user_name
                people_dirct['phone'] = people[j].user_phone
                people_list.append(people_dirct)

            merchant_dirct['peoples'] = people_list
            return merchant_dirct
        except:
            return 0

    def insert_deal_table(self, seller_merchant_id, buyer_merchant_id, car_id, deal_price):
        try:
            deal_time = datetime.datetime.now()
            manage_deal.objects.create(seller_merchant_id=seller_merchant_id, buyer_merchant_id=buyer_merchant_id, car_id=car_id, deal_price=deal_price, deal_time=deal_time)
            return 666
        except:
            return 0

    def delete_deal_record_one_by_one(self, operation_id):
        '''
        一个个删除
        :param operation_id:
        :return:
        '''
        try:
            manage_deal.objects.get(id=operation_id).delete()
            return 666
        except:
            return 0

    def delete_deal_record_some(self, operation_id_list):
        '''
        批量删除
        :param operation_id_list:
        :return:
        '''
        try:
            manage_deal.objects.filter(id__in=operation_id_list).delete()
            return 666
        except:
            return 0

    def delete_deal_record_all(self):
        '''
         全部删除
        :return:
        '''
        try:
            manage_deal.objects.all().delete()
            return 666
        except:
            return 0

    def get_user_list(self):
        try:
            #is_black=0，表示该会员没有被拉黑，全部会员页面显示的应该是没有被拉黑的会员
            user = user_info_table.objects.filter(is_black=0).order_by('-add_time')
            user_list = []
            for i in range(len(user)):
                user_dirct = {}
                user_dirct['company_name'] = user[i].user_company_name
                user_dirct['region'] = user[i].user_address
                user_dirct['user_trademark'] = user[i].user_trademark
                user_dirct['state'] = user[i].state
                user_dirct['id'] = user[i].id

                people = user_info_people.objects.filter(merchant_id=user[i].id)
                people_list = []
                for j in range(len(people)):
                    people_dirct = {}
                    people_dirct['name'] = people[j].user_name
                    people_dirct['phone'] = people[j].user_phone
                    people_list.append(people_dirct)

                user_dirct['peoples'] = people_list

                user_list.append(user_dirct)
            return user_list
        except:
            return 0
