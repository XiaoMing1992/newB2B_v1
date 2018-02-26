from django.db import models
import datetime

# Create your models here.
class collect_seller_table(models.Model):
     user_id = models.IntegerField(default=0, db_index=True) #当前用户的id
     seller_id = models.IntegerField(default=0) #要收藏的商家的id

class collect_car_table(models.Model):
     user_id = models.IntegerField(default=0, db_index=True) #当前用户的id
     car_id = models.IntegerField(default=0) #要收藏的车的id

#存放邀请码的表
class inviteCode_table(models.Model):
     user_id = models.IntegerField(default=0, db_index=True) #当前用户的id
     receive_phone = models.CharField(max_length=15, default='10086')       #接受邀请的电话号码
     inviteCode = models.CharField(max_length=50, default='xxxxxx', db_index=True)  #邀请码，并且作为索引

     validity_time = models.DateTimeField(default=datetime.datetime.now())  #邀请码的有效期
     send_time = models.DateTimeField(default=datetime.datetime.now())      #发送邀请码的时间

#存储我的信息，这里面的信息需要在其他地方对应插入
class message_table(models.Model):
     seller_id = models.CharField(max_length=15, default='10086') #卖家的电话号码
     buyer_id = models.CharField(max_length=15, default='10086') #买家的电话号码
     buyer_search_record_id = models.IntegerField(default=0) #买家的搜索条件的id

     company_name = models.CharField(max_length=200, default='xxx') #买家的企业名称，与“完善资料”里面的企业名称对应
     car_id = models.IntegerField(default=0) #车的id

     car_brand = models.CharField(max_length=100, default='XXX')      #品牌
     car_series = models.CharField(max_length=50, default='XXX')      #车系
     car_model = models.CharField(max_length=100, default='XXX')      #车款

     message_time = models.DateTimeField(default=datetime.datetime.now()) #消息时间

     tag_type = models.IntegerField(default=3) #tag_type为0，表示 ‘发布了求购信息’；1表示‘浏览了您的信息’；2表示‘发布了符合您需求的车源’
     action_type = models.IntegerField(default=2) #action_type为0，表示 [发布车源]；为1，表示[寻找车源]

     class Meta:
         ordering = ['-message_time'] #根据最新时间进行降序排序

class record_table(models.Model):
     user_id = models.IntegerField(default=0, db_index=True)         #当前用户的id
     car_type = models.CharField(max_length=100, default='')          #车辆类型
     car_brand = models.CharField(max_length=100, default='')          #品牌

     car_series = models.CharField(max_length=50, default='')          #车系
     car_model = models.CharField(max_length=100, default='')          #车款

     color = models.CharField(max_length=200, default='')              #颜色
     color_hex = models.CharField(max_length=50, default='')           #颜色的16进制，先占位
     delivery_type = models.CharField(max_length=50, default='')        #期货类型

     pay_method = models.CharField(max_length=50, default='')         #付款方式
     sell_area = models.CharField(max_length=100, default='')          #销售区域
     method_logistics = models.CharField(max_length=50, default='')   #物流方式

     time_save = models.DateTimeField(default=datetime.datetime.now())      #保存搜索条件的时间
     time_valid = models.DateTimeField(default=datetime.datetime.now())     #有效期

     province = models.CharField(max_length=50, default='')#省份
     city = models.CharField(max_length=50, default='')    #城市

class user_info_table(models.Model):
     user_id = models.IntegerField(default=0, db_index=True) #当前用户的id
     user_company_name = models.CharField(max_length=200, default='xxx') #企业名称
     user_type = models.CharField(max_length=50, default='xxx') #企业类型
     user_address = models.CharField(max_length=50, default='xxx')#选择地区
     user_trademark = models.TextField(default='xxx') #企业品牌，即简介

     license_path = models.ImageField(upload_to='license/', default='temp/5.jpg') #营业执照图片路径
     id_card_path = models.ImageField(upload_to='id_card/', default='temp/5.jpg') #身份证图片路径
     head_icon_path = models.ImageField(upload_to='head_icon/', default='temp/5.jpg') #头像图片路径

     province = models.CharField(max_length=50, default='')#省份
     city = models.CharField(max_length=50, default='')    #城市

     is_black = models.IntegerField(default=0) #判断商家是否已经被拉黑，1表示已经被拉黑
     black_time = models.DateTimeField(default=datetime.datetime.now()) #拉黑时间

     add_time = models.DateTimeField(default=datetime.datetime.now()) #添加会员的时间
     state = models.IntegerField(default=0) #判断商家是否已经被认证，0表示待审，1表示认证通过，2表示未通过

class user_info_people(models.Model):
     merchant_id = models.IntegerField(default=0) #商家的id
     user_name = models.CharField(max_length=100, default='xxx') #联系人姓名
     user_phone = models.CharField(max_length=15, default='10086') #联系人电话号码

class user_more_table(models.Model):
     seller_id = models.IntegerField(default=0, db_index=True) #卖家的id
     collect_people_num = models.IntegerField(default=0) #收藏人数
     valid_publish_num = models.IntegerField(default=0) #有效发布次数


