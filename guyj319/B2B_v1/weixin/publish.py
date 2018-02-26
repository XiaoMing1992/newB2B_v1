#coding=utf-8
from car.models import car_table
from car.models import invalid_time_car_table
from car.models import car_table_people
import datetime
from account.models import user_more_table
from account.models import user_info_table
from account.models import user_info_people

class Publish_car(object):

    #删除有效期车源
    def deletePublishValidTimeCar(self,operation_id,current_user_phone_number):
         '''
         :param operation_id:
         :param current_user_phone_number:
         :return: 正常删除，返回666；删除出错，返回0
         '''
         try:
             car_table.objects.get(id=operation_id,
                                   user_phone=current_user_phone_number).delete() #根据车的id和用户的电话号码，来删除显示的车
             return 666
         except:
             return 0

    #删除过期车源信息
    def deletePublishInalidTimeCar(self, operation_id):
        '''
        :param operation_id:
        :return:正常删除，返回666；删除出错，返回0
        '''
        try:
            invalid_time_car_table.objects.get(id=operation_id).delete() #根据车的id和用户的电话号码，来删除显示的车
            return 666
        except:
            return 0

    def againPublish(self, operation_id):
        '''
        :param operation_id:
        :return: 在存放过期的车的表里面，正常获取到信息，返回该信息；找不到，返回0
        '''
        try:
            modify_info = invalid_time_car_table.objects.get(id=operation_id) #根据车的id和用户的电话号码，获取显示的车
            return modify_info
        except:
            return 0

    def modifyPublish(self, operation_id):
        '''
        :param operation_id:
        :return: 在存放有效期的车的表里面，正常获取到信息，返回该信息；找不到，返回0
        '''
        try:
             modify_info = car_table.objects.get(id=operation_id) #根据车的id和用户的电话号码，获取显示的车
             return modify_info
        except:
            return 0

    #找到车的信息，并且返回
    def getPublishInfo(self, user_id, car):
        '''
        :param user_id:
        :param car:
        :return: 正常获取发布的信息，返回该信息；查询出错，返回0
        '''

        car_info = {} #保存发布的car的信息
        if car:
            car_info['style'] = car.car_type                       #车辆类型

            car_info['brand'] = car.car_brand                       #品牌
            car_info['displacement'] = car.car_series               #车系
            car_info['other'] = car.car_model                        #车款

            car_info['color'] = car.color                           #颜色
            car_info['delivery_type'] = car.delivery_type           #期货类型
            car_info['delivery_time'] = car.delivery_time           #期货时间
            car_info['pay_method'] = car.pay_method                 #付款方式
            car_info['sell_area'] = car.sell_area                   #销售区域
            car_info['method_logistics'] = car.method_logistics     #物流方式

            car_info['lowest_price'] = car.lowest_price             #优惠的钱
            car_info['highest_price'] = car.highest_price           #最高报价
            car_info['discount_rate'] = car.discount_rate             #优惠点数

            car_info['introduction'] = car.introduction             #备注说明
            car_info['valid_time'] = car.date_valid                 #有效的日期

            #查询完善资料的那部分的信息
            people = {}
            peoples = []
            try:
                user = user_info_table.objects.get(user_id=user_id)
                merchant_id = user.id
                result = car_table_people.objects.filter(merchant_id=merchant_id)  #根据点击“查询详情”时传进来的发布者的手机号来查询相关的完善资料的信息
            except:
                return 0
            for i in range(len(result)):
                people['name'] = result[i].people_name    #联系人姓名
                people['phone'] = result[i].people_phone   #联系人电话号码
                peoples.append(people)
                people = {}

            car_info['peoples'] = peoples               #联系人
            return car_info


    def updateData(self, car_id, car_info):
         '''
         :param car_id:
         :param car_info:
         :return: 正常插入或者更新数据，返回666；插入发布信息数据或者更新数据失败，返回0
         '''
         date_publish = datetime.datetime.now()     #发布的日期

         car_type = car_info.get('style',None)                       #车辆类型

         car_brand = car_info.get('brand',None)                           #品牌
         car_series = car_info.get('displacement',None)                   #车系
         car_model = car_info.get('other',None)                           #车款

         color = car_info.get('color',None)                           #颜色

         delivery_time = car_info.get('delivery_time',None)           #期货时间
         delivery_type = car_info.get('delivery_type',None)           #期货类型
         pay_method = car_info.get('pay_method',None)                 #付款方式
         sell_area = car_info.get('sell_area',None)                   #销售区域
         method_logistics = car_info.get('method_logistics',None)     #物流方式

         lowest_price = car_info.get('lowest_price',None)             #最低报价
         highest_price = car_info.get('highest_price',None)           #最高报价
         discount_rate = car_info.get('discount_rate',None)             #优惠点数

         introduction = car_info.get('introduction',None)             #备注说明
         valid_time = car_info.get('valid_time',None)                 #有效的日期

         user_names = car_info.get('user_names',None)                 #联系人姓名
         phone_numbers = car_info.get('phone_numbers',None)           #联系人电话

         try:
             car_peoples = car_table_people.objects.filter(car_id=car_id)
             for i in range(len(user_names)):
                car_peoples[i].people_name = user_names[i]
                car_peoples[i].people_phone = phone_numbers[i]

             car = car_table.objects.get(id=car_id)
             car.car_type = car_type

             car.car_brand = car_brand
             car.car_series = car_series
             car.car_model = car_model

             car.color = color
             car.delivery_type = delivery_type
             car.delivery_time = delivery_time
             car.pay_method = pay_method
             car.sell_area = sell_area
             car.method_logistics = method_logistics
             car.lowest_price = lowest_price
             car.highest_price = highest_price
             car.discount_rate = discount_rate
             car.introduction = introduction
             car.date_publish = date_publish
             car.date_valid = valid_time
             car.read_num = 0

             car.save()
             car_peoples.save()
         except:
             return 0

    def firstPublishInsertData(self,  user_id, car_info):
         '''
         :param user_id:
         :param car_info:
         :return: 正常插入或者更新数据，返回666；插入发布信息数据或者更新数据失败，返回0
         '''

         date_publish = datetime.datetime.now()   #发布的日期

         car_type = car_info.get('carType')                       #车辆类型
         car_type = (' ').join(car_type) #将列表转变为字符串，这里以空格隔开

         car_brand = car_info.get('car_brand')                     #品牌
         car_series = car_info.get('car_series')                   #车系
         car_model = car_info.get('car_model')                     #车款

         color = car_info.get('color')                           #颜色
         color = (' ').join(color) #将列表转变为字符串，这里以空格隔开

         delivery_type = car_info.get('delivery_type')           #期货类型
         pay_method = car_info.get('pay_method')                 #付款方式
         sell_area = car_info.get('sell_area')                   #销售区域
         method_logistics = car_info.get('method_logistics')     #物流方式

         lowest_price = car_info.get('lowest_price')             #最低报价
         highest_price = car_info.get('highest_price')           #最高报价
         discount_rate = car_info.get('discount_rate')             #优惠点数

         introduction = car_info.get('introduction')             #备注说明

         try:
             # datetime数据是整型的
             delivery_date = car_info.get('delivery_date')           #期货时间
             delivery_date = datetime.datetime(int(delivery_date.get('year')), int(delivery_date.get('month')), int(delivery_date.get('day')),0,0,0)

             out_date = car_info.get('out_date')                 #有效的日期
             date_valid = datetime.datetime(int(out_date.get('year')), int(out_date.get('month')), int(out_date.get('day')),0,0,0)

             user = user_info_table.objects.get(user_id=user_id)
             merchant_id = user.id
             car = car_table.objects.create(merchant_id=merchant_id,
                                            car_type=car_type,
                                            car_brand=car_brand,
                                            car_series=car_series,
                                            car_model=car_model,
                                            color=color,
                                            delivery_type=delivery_type,
                                            delivery_time=delivery_date,
                                            date_valid=date_valid,
                                            pay_method=pay_method,
                                            sell_area=sell_area,
                                            method_logistics=method_logistics,
                                            lowest_price=lowest_price,
                                            highest_price=highest_price,
                                            discount_rate=discount_rate,
                                            introduction=introduction,
                                            date_publish=date_publish,
                                            read_num=0)
             car_id = car.id

             user_names = car_info.get('user_names')                 #联系人姓名
             phone_numbers = car_info.get('phone_numbers')           #联系人电话

             for i in range(len(user_names)):
                 car_table_people.objects.create(car_id=car_id,
                                                 people_name=user_names[i],
                                                 people_phone=phone_numbers[i])
         except:
            return 0

         try:
            user_more = user_more_table.objects.get(seller_id=merchant_id)
            temp = user_more.valid_publish_num+1
            user_more.valid_publish_num = temp
            user_more.save() #保存
         except:
            try:
                user_more_table.objects.create(seller_id=merchant_id,
                                               collect_people_num=0,
                                               valid_publish_num=1) #第一次发布
            except:
                return 0
         return 666

    def getPublishPeople(self, user_id):
        try:
            user = user_info_table.objects.get(user_id=user_id)
            merchant_id = user.id

            #查询完善资料的那部分的联系人的信息
            people_info = user_info_people.objects.filter(merchant_id=merchant_id)  #根据点击“查询详情”时传进来的发布者的手机号来查询相关的完善资料的信息
            people = {}
            peoples = []
            for i in range(len(people_info)):
                people['contact_name'] = people_info[i].user_name  #联系人姓名
                people['phone_number'] = people_info[i].user_phone  #联系人电话号码
                peoples.append(people)
                people = {}
            return peoples
        except:
            return 0