#coding=utf-8
from django.db import models
import datetime

# Create your models here.

#  db_index=True 表示建立索引
# car_table 存储发布页面发布的除了联系人外的资料
class car_table(models.Model):
     merchant_id = models.IntegerField(default=0, db_index=True) #商家的id
     car_type = models.CharField(max_length=100, default='XXX') #车辆类型
     car_brand = models.CharField(max_length=100, default='XXX') #品牌

     car_series = models.CharField(max_length=100, default='XXX')   #车系
     car_model = models.CharField(max_length=100, default='XXX')    #车款

     color = models.CharField(max_length=200, default='XXX') #颜色
     color_hex = models.CharField(max_length=50, default='#ffffff') #颜色的16进制，先占位

     delivery_type= models.CharField(max_length=50, default='XXX') #期货类型
     delivery_time = models.DateTimeField(default=datetime.datetime.now()) #期货时间

     pay_method = models.CharField(max_length=50, default='XXX') #付款方式
     sell_area = models.CharField(max_length=200, default='XXX') #销售区域
     method_logistics = models.CharField(max_length=50, default='XXX') #物流方式

     lowest_price = models.IntegerField(default=0) #优惠的钱
     highest_price = models.IntegerField(default=0) #最高报价
     discount_rate = models.CharField(max_length=20, default='0') #优惠点数

     introduction = models.CharField(max_length=1000, default='XXX') #备注说明

     date_publish = models.DateTimeField(default=datetime.datetime.now()) #发布的日期
     date_valid = models.DateTimeField(default=datetime.datetime.now()) #有效的日期

     read_num = models.IntegerField(default=0) #阅读量createSession(req)

     province = models.CharField(max_length=50, default='')#省份
     city = models.CharField(max_length=50, default='')    #城市

     car_type_1 = models.IntegerField(default=0) #车辆类型1
     car_type_2 = models.IntegerField(default=0) #车辆类型2
     car_type_3 = models.IntegerField(default=0) #车辆类型3
     car_type_4 = models.IntegerField(default=0) #车辆类型4

     color_1 = models.IntegerField(default=0) #颜色1
     color_2 = models.IntegerField(default=0) #颜色2
     color_3 = models.IntegerField(default=0) #颜色3
     color_4 = models.IntegerField(default=0) #颜色4
     color_5 = models.IntegerField(default=0) #颜色5
     color_6 = models.IntegerField(default=0) #颜色6
     color_7 = models.IntegerField(default=0) #颜色7

     is_black = models.IntegerField(default=0) #判断商家是否已经被拉黑，1表示已经被拉黑
     black_time = models.DateTimeField(default=datetime.datetime.now()) #拉黑时间

# car_table_people 存储发布页面发布的联系人的资料，因为可以动态增加多个联系人，所以另外建一个表，将该发布者的电话号码和联系人的姓名和电话号码存储在这张表
class car_table_people(models.Model):
     car_id = models.IntegerField(default=0, db_index=True) #车的id
     people_name = models.CharField(max_length=100, default='xxx') #联系人姓名
     people_phone = models.CharField(max_length=15, default='10086') #联系人的电话号码

#没有有效期，因为过期了，要也没啥用
class invalid_time_car_table(models.Model):
     merchant_id = models.IntegerField(default=0, db_index=True) #商家的id
     car_style = models.CharField(max_length=100, default='XXX') #车辆类型

     car_brand = models.CharField(max_length=100, default='XXX') #品牌
     car_series = models.CharField(max_length=100, default='XXX')   #车系
     car_model = models.CharField(max_length=100, default='XXX')    #车款

     color = models.CharField(max_length=200, default='XXX') #颜色
     color_hex = models.CharField(max_length=50, default='#ffffff') #颜色的16进制，先占位

     delivery_type= models.CharField(max_length=50, default='XXX') #期货类型
     delivery_time = models.DateTimeField(default=datetime.datetime.now()) #期货时间

     pay_method = models.CharField(max_length=50, default='XXX') #付款方式
     sell_area = models.CharField(max_length=200,default='XXX') #销售区域
     method_logistics = models.CharField(max_length=50, default='XXX') #物流方式

     lowest_price = models.IntegerField(default=0) #最低报价
     highest_price = models.IntegerField(default=0) #最高报价
     discount_rate = models.CharField(max_length=20, default='0') #优惠点数

     introduction = models.TextField(default='XXX') #备注说明

     date_publish = models.DateTimeField(default=datetime.datetime.now()) #发布的日期
     date_valid = models.DateTimeField(default=datetime.datetime.now()) #有效的日期

     read_num = models.IntegerField(default=0) #阅读量

     province = models.CharField(max_length=50, default='')#省份
     city = models.CharField(max_length=50, default='')    #城市

     car_type_1 = models.IntegerField(default=0) #车辆类型1
     car_type_2 = models.IntegerField(default=0) #车辆类型2
     car_type_3 = models.IntegerField(default=0) #车辆类型3
     car_type_4 = models.IntegerField(default=0) #车辆类型4

     color_1 = models.IntegerField(default=0) #颜色1
     color_2 = models.IntegerField(default=0) #颜色2
     color_3 = models.IntegerField(default=0) #颜色3
     color_4 = models.IntegerField(default=0) #颜色4
     color_5 = models.IntegerField(default=0) #颜色5
     color_6 = models.IntegerField(default=0) #颜色6
     color_7 = models.IntegerField(default=0) #颜色7

     is_black = models.IntegerField(default=0) #判断商家是否已经被拉黑，1表示已经被拉黑
     black_time = models.DateTimeField(default=datetime.datetime.now()) #拉黑时间