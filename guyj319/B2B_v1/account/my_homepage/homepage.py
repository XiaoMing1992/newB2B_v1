# coding=utf-8
from car.models import car_table
from account.models import user_info_table
from account.models import user_info_people
from account.models import user_more_table
import datetime
from django.views.decorators.cache import cache_control,cache_page


#指定缓存是否需要总是检查新版本, 如果没有变化则仅传送缓存版本. (某些缓存即使服务器端页面变化也仅传递缓存版本--仅仅因为缓存拷贝尚未到期).
# 在这个例子里 cache_control 通知缓存每次检验缓存版本, 直到 600 秒到期:
#@cache_control(must_revalidate=True, max_age=600)
#@cache_page(30)

class Homepage(object):

    def getSellerPhoneInUserInfoTable(self,id):
        '''
        :param id:
        :return: 如果存在，则返回该卖家对应的user_phone_id；否返回0
        '''
        try:
            result = user_info_table.objects.get(id=id)
            return result.user_phone_id
        except:
            return 0

    #找到车的信息，并且返回
    def findHomepageCar(self, merchant_id):
        '''
        :param merchant_id:
        :return: 正常查询，返回查询到的商家发布的车的信息；查询出错，返回0
        '''
        try:
            #查询车的信息
            #根据点击“查询详情”时传进来的发布者的手机号来查询相关的车的信息
            car = car_table.objects.filter(merchant_id=merchant_id).order_by('-date_publish')
        except:
            return 0
        all_cars_infos = []   #存储所有与该商家号码相关的车的信息
        today = datetime.date.today() #比较日期就可以了
        if car:
           for i in range(len(car)):
               #下面的重新声明很重要，如果不重新声明，会造成覆盖，而不是添加
               series_detail={}
               commodity_detail = {}
               update_time = {}
               price = {}
               each_car_info = {}

               publish_time = car[i].date_publish           #发布的日期
               update_time['year'] = publish_time.year      #发布的日期的年份
               update_time['month'] = publish_time.month    #发布的日期的月份
               update_time['day'] = publish_time.day

               commodity_detail['color'] = car[i].color                               #颜色
               commodity_detail['type'] = car[i].delivery_type                        #货期
               commodity_detail['style'] = car[i].car_type                           #车辆类型

               series_detail['brand'] = car[i].car_brand                           #品牌
               series_detail['displacement'] = car[i].car_series                   #车系
               series_detail['other'] = car[i].car_model                               #车款

               price['lowest_price'] = car[i].lowest_price                #最低报价
               price['highest_price'] = car[i].highest_price               #最高报价

               each_car_info["update_time"] = update_time
               each_car_info["location"] = car[i].sell_area                        #销售区域
               each_car_info["commodity_detail"] = commodity_detail
               each_car_info["series_detail"] = series_detail
               each_car_info["price"] = price

               #因为看到的商家主页的车都是有效发布期间，所以不再判断
               #因为求的是天数，所以比较日期就可以了
               each_car_info['remaining_days'] = (car[i].date_valid.date() - today).days    #剩余天数

               each_car_info['read_num'] = car[i].read_num         #阅读量
               each_car_info['car_id'] = car[i].id               #车的id

               all_cars_infos.append(each_car_info)  #添加所有该车信息
           return all_cars_infos

    #查询完善资料的那部分的企业、地点，以及卖家头像等相关信息
    def getSellerInfo(self, merchant_id):
       '''
       :param merchant_id:
       :return:正常查询，返回查询到的商家完善资料的那部分的企业、地点，以及卖家头像等相关信息；查询出错，返回0
       '''
       try:
            seller_info = user_info_table.objects.get(id=merchant_id)  #根据点击“查询详情”时传进来的发布者的手机号来查询相关的完善资料的信息
       except:
            return 0
       user_company_name = seller_info.user_company_name  #企业名称
       user_address = seller_info.user_address  #所在地区
       user_type = seller_info.user_type  #企业类型
       user_trademark = seller_info.user_trademark #企业品牌，即简介
       user_head_icon = seller_info.head_icon_path.url #用户头像路径

       #查询完善资料的那部分的联系人的信息
       people = {}
       peoples = []
       try:
           #根据点击“查询详情”时传进来的发布者的手机号来查询相关的完善资料的信息
          result2 = user_info_people.objects.filter(merchant_id=merchant_id)
       except:
           return 0
       for i in range(len(result2)):
            people['contact_name'] = result2[i].user_name  #联系人姓名
            people['phone_number'] = result2[i].user_phone  #联系人电话号码
            peoples.append(people)
            people = {}

       try:
            #从 user_more_table 中获取下面的信息
            user_more = user_more_table.objects.get(seller_id=merchant_id)
            collect_people_num = user_more.collect_people_num #收藏该卖家的人数
            valid_publish_num = user_more.valid_publish_num   #有效发布
       except:
            collect_people_num = 0
            valid_publish_num = 0

       merchant_material = {}
       merchant_material['id'] = merchant_id
       merchant_material['company_name'] = user_company_name
       merchant_material['location'] = user_address
       merchant_material['merchant_type'] = user_type
       merchant_material['introduction'] = user_trademark

       #merchant_material['peoples'] = peoples
       merchant_material['contact_name'] = peoples[0].get('contact_name','')
       merchant_material['phone_number'] = peoples[0].get('phone_number','')

       merchant_material['collected_number'] = collect_people_num
       merchant_material['published_number'] = valid_publish_num

       merchant_material['image_path'] = user_head_icon
       return merchant_material