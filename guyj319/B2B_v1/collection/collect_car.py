# coding=utf-8
from car.models import car_table
from car.models import invalid_time_car_table
from account.models import collect_car_table
import datetime

class Collect_car(object):

    #取消收藏和查询收藏车信息的表
    def cancelCollectCar(self,car_id):
        '''
        :param car_id:
        :return: 正常删除和查询，返回用户收藏的车的信息集合；删除或者查询失败，返回0
        '''
        try:
           collect_car_table.objects.get(car_id=car_id).delete()#根据id和商家电话号码来删除
           return 666
        except:
          return 0

    #查询收藏车信息的表
    def searchCollectCar(self, user_id):
        '''
        :param user_id:
        :return: 正常查询，返回用户收藏的车的信息集合；查询失败，返回0
        '''
        try:
           mycollect_records = collect_car_table.objects.filter(user_id=user_id) #收藏的车的信息的列表
           return mycollect_records
        except:
          return 0

    #查询存放发布的车信息的表
    def searchCarTable(self,mycollect_records):
          '''
          :param mycollect_records:
          :return: 正常查询，返回用户收藏的车的信息集合；查询失败，返回0
          '''
          records=[]
          for i in range(len(mycollect_records)):
               #查询完善资料的那部分的信息，是商家的信息
               #在存放有效的car_table里面先查找该车，如果没有再去存放过期的车的invalid_time_car_table里面取，如果还没有，说明数据库查询错误
               try:
                   result = car_table.objects.get(id=mycollect_records[i].car_id)  #车的id，根据该id来查询相关的车的信息
               except:
                   try:
                       result = invalid_time_car_table.objects.get(id=mycollect_records[i].car_id)  #车的id，根据该id来查询相关的车的信息
                   except:
                      return 404
                      #return 0
               records.append(result)#存放所有记录，最后一次性查找
          all_cars_infos = Collect_car.findCar(self, records) #找到车的信息
          return all_cars_infos

    #找到车的信息，并且返回
    def findCar(self, car):

        today = datetime.date.today()    #获取今天的日期

        all_cars_infos = []   #存储所有与该商家号码相关的车的信息
        if car:
           for i in range(len(car)):
               series_detail = {}
               commodity_detail = {}
               update_time = {}
               price = {}
               each_car_info = {}

               each_car_info['detail_id'] = car[i].id           #车的id

               publish_time = car[i].date_publish           #发布的日期
               update_time['year'] = publish_time.year      #发布的日期的年份
               update_time['month'] = publish_time.month    #发布的日期的月份
               update_time['day'] = publish_time.day        #发布的日期的天数

               commodity_detail['color'] = car[i].color                               #颜色
               commodity_detail['type'] = car[i].delivery_type                        #货期
               commodity_detail['style'] = car[i].car_type                           #车辆类型

               series_detail['brand'] = car[i].car_brand                           #品牌
               series_detail['displacement'] = car[i].car_series                    #车系
               series_detail['other'] = car[i].car_model                             #车款

               price['lowest_price'] = car[i].lowest_price                 #优惠的钱
               price['highest_price'] = car[i].highest_price               #报价

               each_car_info["update_time"] = update_time
               each_car_info["location"] = car[i].sell_area                        #销售区域
               each_car_info["commodity_detail"] = commodity_detail
               each_car_info["series_detail"] = series_detail
               each_car_info["price"] = price

               each_car_info["is_black"] = car[i].is_black #判断该车是否已经被拉黑

               #######
               #each_car_info['read_num'] = car[i].read_num         #阅读量

               #有效期
               expiry_date = {}
               valid_time = car[i].date_valid               #有效期的日期
               if today <= valid_time.date():  #比较日期，不比较time
                   expiry_date['year'] = valid_time.year        #有效期的日期的年份
                   expiry_date['month'] = valid_time.month      #有效期的日期的月份
                   expiry_date['day'] = valid_time.day          #有效期的日期的天数
               else:
                   expiry_date['year'] = '0'
                   expiry_date['month'] = '00'
                   expiry_date['day'] = '00'
               each_car_info['out_date'] = expiry_date

               all_cars_infos.append(each_car_info)  #添加所有该车信息

           return all_cars_infos
