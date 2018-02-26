# coding=utf-8
from car.models import car_table
from car.models import car_table_people
from account.models import user_info_table
from account.models import collect_seller_table
from account.models import collect_car_table
from account.models import user_more_table
from account.models import message_table
import datetime

class Car_detail(object):
    def insertMessageTable(self, user_id, seller_id, car_id, car_brand, car_series, car_model, tag_type, action_type):
        '''
        :param user_id:
        :param seller_id:
        :param car_id:
        :param car_model:
        :return: 正常查询和插入，返回666；否则，返回0
        '''
        try:
           buyer = user_info_table.objects.get(user_id=user_id)
           company_name = buyer.user_company_name   #获取该买家的企业名称
        except:
           company_name = 'xxx'        #如果该买家没有完善资料，自然不会有该公司名称，赋给None

        try:                         #把浏览该卖家的买家信息写进 message_table 里面，显示到“我的消息”那里
           now_time = datetime.datetime.now()
           message_table.objects.create(seller_id=seller_id,
                                        buyer_id=user_id,
                                        company_name=company_name,
                                        car_id=car_id,
                                        car_brand=car_brand,
                                        car_series=car_series,
                                        car_model=car_model,
                                        message_time=now_time,
                                        tag_type=tag_type,
                                        action_type=action_type)
           return 666
        except:
           return 0

    def collectSeller(self, user_id, seller_id):
        '''
        :param user_id:
        :param seller_id:
        :return:收藏的商家不存在，收藏该商家成功，返回666；失败收藏，返回0
        '''
        #收藏的商家不存在，收藏该商家
        try:
           collect_seller_table.objects.create(user_id=user_id,
                                               seller_id=seller_id)
        except:
            return 0
        try:
            #收藏商家的人数更新
            user_more = user_more_table.objects.get(seller_id=seller_id) #收藏商家的人数更新
            temp = user_more.collect_people_num + 1 #收藏商家的人数增加 1
            user_more.collect_people_num = temp #保存更新后的收藏人数
            user_more.save() #保存更新后的收藏人数
        except:  #该卖家第一次被收藏
            try:
                user_more_table.objects.create(seller_id=seller_id,
                                               collect_people_num=1)
            except:
                 return 0
        return 666

    def collectCar(self, user_id, car_id):
        '''
        :param user_id:
        :param car_id:
        :return: 收藏车源信息成功，返回666；失败收藏，返回0
        '''
        try:
            collect_car_table.objects.create(user_id=user_id, car_id=car_id)
            return 666
        except:
            return 0

    def isMerchantCollected(self, user_id, seller_id):
        '''
        :param user_id:
        :param seller_id:
        :return: 如果该商家已经被收藏过，则返回 True；否则返回 False; 如果查询错误，返回 0
        '''
        try:
            #该商家已经被收藏过了，不用再收藏
            result = collect_seller_table.objects.filter(user_id=user_id,
                                                         seller_id=seller_id)
            if result:
                return True
            else:
                return False
        except:
            return 2 #注意：True是1，False是0，数据库查询出错如果返回0和查询结果为空集返回False相同，会出错，所以此处定义数据库查询出错如果返回2

    def isInfoCollected(self, user_id, car_id):
        '''
        :param current_user_phone_number:
        :param car_id:
        :return:如果该信息已经被收藏过，则返回 True；否则返回 False; 如果查询错误，返回 0
        '''
        try:
            #该商家已经被收藏过了，不用再收藏
            result = collect_car_table.objects.filter(user_id=user_id,
                                                      car_id=car_id)
            if result:
                return True
            else:
                return False
        except:
            return 2 #注意：True是1，False是0，数据库查询出错如果返回0和查询结果为空集返回False相同，会出错，所以此处定义数据库查询出错如果返回2

    def getSellerPhone(self,operation_id):
        '''
        :param operation_id:
        :return: 如果存在，则返回该车对应的电话号码；否则，返回0
        '''
        try:
            result = car_table.objects.get(id=operation_id)
            return result.user_phone
        except:
            return 0

    def getSellerId(self, user_id):
        '''
        :param user_id:
        :return: 如果存在，则返回该卖家对应的id；否返回0
        '''
        try:
            result = user_info_table.objects.get(user_id=user_id)
            return result.id
        except:
            return 0

    def getCarInfo(self, id):
        #对应的查询的车的阅读量加1
        try:
            car = car_table.objects.get(id=id) #当前用户看的车
            car.read_num = car.read_num+1 #对应的查询的车的阅读量加1
            car.save()
        except:
            return 0

        #查询车的信息
        car_id = car.id                             #车的id

        series_detail = {}
        delivery_date = {}       #交货时间
        out_date = {}            #过期
        price = {}
        source_detail_list = {}

        delivery_time = car.delivery_time             #交货时间
        delivery_date['year'] = delivery_time.year        #交货时间的年份
        delivery_date['month'] = delivery_time.month      #交货时间的月份
        delivery_date['day'] = delivery_time.day          #交货时间的天数

        out_time = car.date_valid           #车的有效期
        out_date['year'] = out_time.year        #过期的年份
        out_date['month'] = out_time.month      #过期的月份
        out_date['day'] = out_time.day          #过期的天数

        series_detail['brand'] = car.car_brand                           #品牌
        series_detail['displacement'] = car.car_series                   #车系
        series_detail['other'] = car.car_model                           #车款

        price['lowest_price'] = car.lowest_price                #最低报价
        price['highest_price'] = car.highest_price               #最高报价

        source_detail_list["id"] = car_id                                     #车的id
        source_detail_list["series_detail"] = series_detail                   #车型
        source_detail_list["price"] = price                                   #报价
        source_detail_list["delivery_date"] = delivery_date                   #交货时间
        source_detail_list["out_date"] = out_date                             #过期

        source_detail_list['carType'] = car.car_type                      #车辆类型
        source_detail_list['color'] = car.color                           #颜色
        source_detail_list['color_hex'] = car.color_hex                   #颜色的16进制，先占位
        source_detail_list['delivery_type'] = car.delivery_type           #期货类型
        source_detail_list['payType'] = car.pay_method                    #付款方式
        source_detail_list["saleRegion"] = car.sell_area                  #销售区域
        source_detail_list['logisticsType'] = car.method_logistics        #物流方式
        source_detail_list['remark'] = car.introduction                   #备注说明

        return source_detail_list   #车源信息

    def getSellerInfo(self, car_id):
        people = {}
        peoples = []
        try:
            car_people = car_table_people.objects.filter(car_id=car_id)  #根据点击“查询详情”时传进来的发布者的手机号来查询相关的完善资料的信息
        except:
            return 0
        for i in range(len(car_people)):
            people['contact_name'] = car_people[i].people_name  #联系人姓名
            people['phone_number'] = car_people[i].people_phone  #联系人电话号码
            peoples.append(people)
            people = {}

        #查询完善资料的那部分的信息
        try:
            car = car_table.objects.get(id=car_id) #当前用户看的车
            merchant_id = car.merchant_id
            user = user_info_table.objects.get(id=merchant_id)  #根据点击“查询详情”时传进来的发布者的手机号来查询相关的完善资料的信息
        except:
            return 0
        user_id = user.id  #商家id
        user_company_name = user.user_company_name  #企业名称
        user_address = user.user_address  #所在地区
        user_type = user.user_type  #企业类型
        user_trademark = user.user_trademark #企业品牌，即简介
        user_head_icon = user.head_icon_path.url #用户头像路径

        #查询完善资料的那部分的信息

        merchant_material = {}
        merchant_material['id'] = user_id  #############################???
        merchant_material['company_name'] = user_company_name
        merchant_material['location'] = user_address
        merchant_material['merchant_type'] = user_type
        merchant_material['introduction'] = user_trademark
        merchant_material['contact'] = peoples  #联系人信息
        merchant_material['image_path'] = user_head_icon

        seller_info = {}  #存储与该商家号码相关的车的信息
        seller_info['merchant_material'] = merchant_material     #卖家信息
        return seller_info

