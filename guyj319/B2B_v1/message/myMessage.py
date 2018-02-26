# coding=utf-8
from account.models import message_table

class My_message(object):

    def DeleteMyMessage(self,record_id):
        '''
        :param record_id:
        :return: 成功删除，返回666；失败删除，返回0
        '''
        try:
            message_table.objects.get(id=record_id).delete()
            return 666
        except:
            return 0

    #取出 message_table 里面的信息
    def manage_message(self, user_id):
        '''
        :return: 正常查询，返回结果字典；失败查询，返回0
        '''
        try:
            results = message_table.objects.filter(seller_id=user_id)[:100]#按照发布的日期降序排序
        except:
            return 0

        #取出 message_table 里面的信息
        message_dirct = {}
        message_list = []

        date_list = []
        date_dirct = {}
        moment_list = []
        moment_dirct = {}
        day_dirct = {}

        for i in range(len(results)): #取出保存的搜索条件
             if i > 0:
                if results[i].message_time.date() != results[i-1].message_time.date():#两个日期已经不同
                   temp_date = results[i-1].message_time
                   day_dirct['year'] = temp_date.year
                   day_dirct['month'] = temp_date.month
                   day_dirct['day'] = temp_date.day

                   date_dirct['day'] = day_dirct
                   date_dirct['moment_list'] = moment_list
                   date_list.append(date_dirct)
                   date_dirct = {}
                   day_dirct = {}
                   moment_list = []

                   #占位字典，为了配合前端的样式
                   other_dirct = {}
                   other_dirct['id'] = "blank"
                   message_list.append(other_dirct) #添加到消息列表里面，控制样式，此id不涉及数据库

                   #第二个日期的第一个time要记得加上
                   temp_moment = results[i].message_time
                   moment_dirct['hour'] = temp_moment.hour
                   moment_dirct['minute'] = temp_moment.minute
                   moment_dirct['second'] = temp_moment.second

                   moment_dirct['id'] = results[i].id
                   moment_list.append(moment_dirct)
                   moment_dirct = {}

                else:
                   temp_moment = results[i].message_time
                   moment_dirct['hour'] = temp_moment.hour
                   moment_dirct['minute'] = temp_moment.minute
                   moment_dirct['second'] = temp_moment.second

                   moment_dirct['id'] = results[i].id
                   moment_list.append(moment_dirct)
                   moment_dirct = {}
                   if i == len(results)-1:
                     temp_date = results[i-1].message_time
                     day_dirct['year'] = temp_date.year
                     day_dirct['month'] = temp_date.month
                     day_dirct['day'] = temp_date.day

                     date_dirct['day'] = day_dirct
                     date_dirct['moment_list'] = moment_list
                     date_list.append(date_dirct)
                     date_dirct = {}
                     day_dirct = {}
                     moment_list = []
             else:
                   temp_moment = results[i].message_time
                   moment_dirct['hour'] = temp_moment.hour
                   moment_dirct['minute'] = temp_moment.minute
                   moment_dirct['second'] = temp_moment.second

                   moment_dirct['id'] = results[i].id
                   moment_list.append(moment_dirct)
                   moment_dirct = {}

                   if i == len(results)-1:
                     temp_date = results[i].message_time
                     day_dirct['year'] = temp_date.year
                     day_dirct['month'] = temp_date.month
                     day_dirct['day'] = temp_date.day

                     date_dirct['day'] = day_dirct
                     date_dirct['moment_list'] = moment_list
                     date_list.append(date_dirct)
                     date_dirct = {}
                     day_dirct = {}
                     moment_list = []

             message_dirct['id'] = results[i].id      #信息的id，用来删除
             message_dirct['seller_phone'] = results[i].seller_phone
             message_dirct['buyer_phone'] = results[i].buyer_phone
             message_dirct['buyer_search_record_id'] = results[i].buyer_search_record_id
             message_dirct['company_name'] = results[i].company_name
             message_dirct['car_id'] = results[i].car_id
             message_dirct['detail'] = results[i].car_brand+' '+results[i].car_series+' '+results[i].car_model
             message_dirct['tag_type'] = results[i].tag_type
             message_dirct['action_type'] = results[i].action_type
             message_list.append(message_dirct)

             message_dirct = {} #需要重新声明，否则遇到同样的key时，只是在更新value值，而不是添加一条 同样的key、不同的value值的记录

        record_dirct = {}
        record_dirct['message_list'] = message_list
        record_dirct['date_list'] = date_list

        return record_dirct
