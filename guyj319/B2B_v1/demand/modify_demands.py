#coding=utf-8
from account.models import record_table #保存我的需求
import datetime

class Modify_demands(object):

    #获取记录
    def getRecord(self,record_id, user_id):
        '''
        :param record_id:
        :param user_id:
        :return:正常查询，返回该条记录；查询出错，返回0
        '''
        try:
            record_result = record_table.objects.get(id=record_id, user_id=user_id)
            record_str_list = []
            record_str_list.append(record_result.car_style)
            record_str_list.append(record_result.car_brand)
            record_str_list.append(record_result.displacement)
            record_str_list.append(record_result.other)
            record_str_list.append(record_result.color)
            record_str_list.append(record_result.color_hex)
            record_str_list.append(record_result.delivery_type)
            record_str_list.append(record_result.delivery_time)
            record_str_list.append(record_result.pay_method)
            record_str_list.append(record_result.sell_area)
            record_str_list.append(record_result.method_logistics)
            #record_dict['search_detail'] = record_str_list #搜索记录
            return record_str_list
        except:
            return 0

    #更新记录
    def updateRecord(self, user_id, condition):
        try:
            record_id = condition.get('demand_id','')
            record_result = record_table.objects.get(id=record_id,user_id=user_id)
            record_result.car_type = condition.get('car_type','')    #车辆类型

            record_result.car_brand = condition.get('car_brand','')   #品牌
            record_result.car_series = condition.get('car_series','')  #车系
            record_result.car_model = condition.get('car_model','')   #车款

            record_result.color = condition.get('color','')
            #record_result.color_hex = condition.get('color_hex','')
            record_result.delivery_type = condition.get('delivery_type','')
            #record_result.delivery_time = condition.get('delivery_time','')

            #record_result.lowest_price = condition.get('lowest_price','')
            #record_result.highest_price = condition.get('highest_price','')

            record_result.pay_method = condition.get('pay_method','')
            record_result.sell_area = condition.get('sell_area','')
            record_result.method_logistics = condition.get('method_logistics','')

            #更新更新保存的时间
            record_result.time_save = datetime.datetime.now()
            if condition['expiry_date[year]'] != '' and condition['expiry_date[month]'] != '' and condition['expiry_date[day]'] != '':
                #更新有效期
                # datetime数据是整型的
                record_result.time_valid = datetime.datetime(int(condition['expiry_date[year]']), int(condition['expiry_date[month]']), int(condition['expiry_date[day]']),0,0,0)
                #record_result.time_valid.year = condition['expiry_date[year]']
                #record_result.time_valid.month = condition['expiry_date[month]']
                #record_result.time_valid.day = condition['expiry_date[day]']

                #record_result.time_valid = condition['expiry_date[year]']+'-'+condition['expiry_date[month]']+'-'+condition['expiry_date[day]']
                #record_result.time_valid = condition.get('time_valid','0-00-00')   #更新有效期

            record_result.save() #保存

            return 666
        except:
            return 0

    #更新记录
    def updateRecord_2(self,record_id,user_id,update_record_list):
        try:
            record_result = record_table.objects.get(id=record_id, user_id=user_id)
            record_result.car_style = update_record_list[0]
            record_result.car_brand = update_record_list[1]
            record_result.displacement = update_record_list[2]
            record_result.other = update_record_list[3]
            record_result.color = update_record_list[4]
            record_result.color_hex = update_record_list[5]
            record_result.delivery_type = update_record_list[6]
            record_result.delivery_time = update_record_list[7]
            record_result.pay_method = update_record_list[8]
            record_result.sell_area = update_record_list[9]
            record_result.method_logistics = update_record_list[10]
            record_result.time_valid = update_record_list[11]   #更新有效期
            record_result.save() #保存
            return 666
        except:
            return 0