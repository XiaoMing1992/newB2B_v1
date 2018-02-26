# coding=utf-8
from car.models import car_table
from car.models import invalid_time_car_table
from account.models import user_info_table
from account.models import user_info_people
from account.models import user_more_table
import datetime

class Personal_center(object):

    #撤销有效期车源
    def deleteValidTimeCar(self, operation_id, user_id):
         '''
         :param operation_id:
         :param current_user_phone_number:
         :return: 正常删除和更新，返回666；删除或者更新出错，返回0
         '''
         try:
             car_table.objects.get(id=operation_id).delete() #根据车的id和用户的电话号码，来删除显示的车
             user = user_more_table.objects.get(seller_id=user_id) #更新有效发布次数
             user.valid_publish_num = user.valid_publish_num-1  #有效发布次数-1
             user.save() #更新有效发布次数
             return 666
         except:
             return 0

    #删除过期车源信息
    def deleteInalidTimeCar(self, operation_id):
        '''
        :param operation_id:
        :return:正常删除，返回666；删除出错，返回0
        '''
        try:
            invalid_time_car_table.objects.get(id=operation_id).delete() #根据车的id和用户的电话号码，来删除显示的车
            return 666
        except:
            return 0

    #查看有效期里面的信息
    def findValidTimeCar(self, merchant_id):
        '''
        :param merchant_id:
        :return: 正常查询返回有效期里的车源信息；失败查询，返回0
        '''
        try:
            #查询车的信息
            car = car_table.objects.filter(merchant_id=merchant_id).order_by('-date_publish')  #根据点击“查询详情”时传进来的发布者的手机号来查询相关的车的信息
            return car
        except:
            return 0

    #查看过期里面的信息
    def findInvalidTimeCar(self, merchant_id):
        '''
        :param merchant_id:
        :return: 正常查询返回过期里的车源信息；失败查询，返回0
        '''
        try:
            #查询车的信息
            car = invalid_time_car_table.objects.filter(merchant_id=merchant_id).order_by('-date_publish')  #根据点击“查询详情”时传进来的发布者的手机号来查询相关的车的信息
            return car
        except:
            return 0

    #找到车的信息，并且返回
    def findPersonalCenterCar(self, car):
        '''
        :param mTools:
        :param car:
        :return:返回找到车的信息
        '''
        all_cars_infos = []   #存储所有与该商家号码相关的车的信息
        today = datetime.date.today() #比较日期就可以了
        if car:
           for i in range(len(car)):
               #下面的重新声明很重要，如果不重新声明，会造成覆盖，而不是添加
               series_detail = {}
               commodity_detail = {}
               publish_time = {}
               price = {}
               each_car_info = {}

               temp_publish_time = car[i].date_publish      #发布的日期
               publish_time['year'] = temp_publish_time.year      #发布的日期的年份
               publish_time['month'] = temp_publish_time.month      #发布的日期的月份
               publish_time['day'] = temp_publish_time.day         #发布的日期的天数

               commodity_detail['color'] = car[i].color                               #颜色
               commodity_detail['type'] = car[i].delivery_type                        #货期
               commodity_detail['style'] = car[i].car_type                           #车辆类型

               each_car_info["series_detail"] = car[i].car_brand+'/'+car[i].car_series+'/'+car[i].car_model

               #series_detail['brand'] = car[i].car_brand                           #车型
               #series_detail['displacement'] = car[i].car_series                 #配置
               #series_detail['other'] = car[i].car_model                               #其他

               price['discount_amount'] = car[i].lowest_price                #优惠的钱
               price['market_price'] = car[i].highest_price                  #报价

               each_car_info["publish_time"] = publish_time
               each_car_info["location"] = car[i].sell_area                        #销售区域
               each_car_info["commodity_detail"] = commodity_detail
               #each_car_info["series_detail"] = series_detail


               each_car_info["price"] = price
               #######
               #因为求的是天数，所以比较日期就可以了
               each_car_info['remaining_days'] = (car[i].date_valid.date() - today).days    #剩余天数

               each_car_info['visit_amount'] = car[i].read_num         #阅读量
               each_car_info['collect_id'] = car[i].id               #车的id
               each_car_info['exceed_collect_id'] = car[i].id        #车的id

               all_cars_infos.append(each_car_info)  #添加所有该车信息
        return all_cars_infos

    #查询完善资料的那部分的企业、地点，以及当前用户头像等相关信息
    def getMyInfo(self, user_id):
       '''
       :param user_id:
       :return:正常查询，返回查询到的商家完善资料的那部分的企业、地点，以及卖家头像等相关信息；查询出错，返回0
       '''

       result1 = None
       try:
            result1 = user_info_table.objects.get(user_id=user_id)  #根据点击“查询详情”时传进来的发布者的手机号来查询相关的完善资料的信息
       except:
            if result1 == None:
                return 404
            else:
                return 0
       merchant_id = result1.id #商家 id
       user_company_name = result1.user_company_name  #企业名称
       user_address = result1.user_address  #所在地区
       user_type = result1.user_type  #企业类型
       user_trademark = result1.user_trademark #企业品牌，即简介
       user_head_icon = result1.head_icon_path.url #用户头像路径

       #查询完善资料的那部分的联系人的信息
       people = {}
       peoples = []
       try:
          result2 = user_info_people.objects.filter(merchant_id=merchant_id)  #根据点击“查询详情”时传进来的发布者的手机号来查询相关的完善资料的信息
       except:
           return 0
       for i in range(len(result2)):
            people['contact_name'] = result2[i].user_name  #联系人姓名
            people['phone_number'] = result2[i].user_phone  #联系人电话号码
            peoples.append(people)
            people = {}

       try:
            user_more = user_more_table.objects.get(seller_id=merchant_id) #从 user_more_table 中获取下面的信息
            collect_people_num = user_more.collect_people_num #收藏该卖家的人数
            valid_publish_num = user_more.valid_publish_num   #有效发布
       except:
            collect_people_num = 0
            valid_publish_num = 0

       merchant_material = {}
       merchant_material['id'] = user_id
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