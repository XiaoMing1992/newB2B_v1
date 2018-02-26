#coding=utf-8
from account.models import record_table
import datetime
from django.views.decorators.cache import cache_control

class My_demands(object):

    def deleteMyDemand(self,record_id_delete):
        '''
        :param record_id_delete:
        :return: 正常删除，返回666；删除出错，返回0
        '''
        try:
            record_table.objects.get(id=record_id_delete).delete()
            return 666
        except:
            return 0

    def searchMyDemands(self, user_id):
        '''
        :param user_id:
        :return: 正常查询，返回以字典类型的元素的结果列表；查询出错，返回0
        '''
        demand_list=[]
        record_dict={}
        try:
            record_results = record_table.objects.filter(user_id=user_id).order_by('-time_save') #按照最新保存搜索记录的时间开始
        except:
            return 0

        for i in range(len(record_results)): #取出保存的搜索条件
            record_dict['demand_id'] = record_results[i].id #表示每条记录的id，这个为后面的编辑和删除服务

            car_type = {}
            car_type['text'] = record_results[i].car_type #车辆类型
            car_type['is_end'] = 'false' #车辆类型

            brand = {}
            brand['text'] = record_results[i].car_brand #品牌
            brand['is_end'] = 'false' #品牌

            model = {}
            model['text'] = record_results[i].car_model #车款
            model['is_end'] = 'false' #车款

            color = {}
            color['text'] = record_results[i].color #颜色
            color['is_end'] = 'false'

            delivery_type = {}
            delivery_type['text'] = record_results[i].delivery_type #货期类型
            delivery_type['is_end'] = 'false'

            pay_method = {}
            pay_method['text'] = record_results[i].pay_method #支付方式
            pay_method['is_end'] = 'false'

            sell_area = {}
            sell_area['text'] = record_results[i].sell_area #销售区域
            sell_area['is_end'] = 'false'

            method_logistics = {}
            method_logistics['text'] = record_results[i].method_logistics #物流方式
            method_logistics['is_end'] = 'false'

            record_dict['car_type'] = car_type #车辆类型

            record_dict['brand'] = brand      #品牌
            #record_dict['series'] = series    #车系
            record_dict['car_model'] = model  #车款

            record_dict['color'] = color
            record_dict['type'] = delivery_type

            record_dict['payment'] = pay_method
            record_dict['region'] = sell_area
            record_dict['logistics'] = method_logistics

            index_list = ['car_type','brand','car_model','color','type','payment','region','logistics']

            j = len(index_list)-1
            while j > -1:
                if record_dict[index_list[j]]['text'] == '' and record_dict[index_list[j-1]]['text'] != '':
                    record_dict[index_list[j-1]]['is_end'] = 'true'
                    if record_results[i].method_logistics != '':        #物流方式
                        record_dict[index_list[j-1]]['is_end'] = 'false'
                    break
                j = j - 1

            save_date = {}
            publish_time = record_results[i].time_save   #发布的日期
            save_date['year'] = publish_time.year        #发布的日期的年份
            save_date['month'] = publish_time.month      #发布的日期的月份
            save_date['day'] = publish_time.day          #发布的日期的天数

            record_dict['save_date'] = save_date #搜索记录发布日期

            expiry_date = {}
            valid_time = record_results[i].time_valid    #有效期的日期
            expiry_date['year'] = valid_time.year        #有效期的日期的年份
            expiry_date['month'] = valid_time.month      #有效期的日期的月份
            expiry_date['day'] = valid_time.day          #有效期的日期的天数

            record_dict['expiry_date'] = expiry_date     #搜索记录发布日期

            #计算有效期
            record_dict['flag_time_valid'] = False
            if record_results[i].time_valid == '永久有效':
                record_dict['time_valid'] = record_results[i].time_valid.date()  #需求有效期
            else:
                today = datetime.date.today()    #获取今天的日期
                if record_results[i].time_valid.date() < today:     #比较日期，不比较time
                    record_dict['time_valid'] = '已经失效'
                elif record_results[i].time_valid.date() == today:  #比较日期，不比较time
                    record_dict['time_valid'] = '有效期剩余0天'
                else:
                    record_dict['flag_time_valid'] = True
                    reamainingDays = (record_results[i].time_valid.date() - today).days
                    record_dict['time_valid'] = reamainingDays  #需求有效期剩余天数

            demand_list.append(record_dict)#添加一条记录

            record_dict={} #===注意
        return demand_list