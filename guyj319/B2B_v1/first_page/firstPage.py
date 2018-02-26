#coding=utf-8
from myadmin.models import manage_deal
from car.models import car_table
import datetime

class First_page(object):

    #获取发布的车的数量
    def getPublishNum(self):
        try:
            user = car_table.objects.all().order_by('-date_publish') #降序排序，提取最近发布的车
            today = datetime.date.today()    #获取今天的日期
            publish_num = 0
            for i in range(len(user)):
                if user[i].date_publish.date() == today: #比较日期，不比较time
                    publish_num = publish_num+1
                elif user[i].date_publish.date() < today: #之前发布的，接下来的都是，跳出
                    break
            return publish_num  #返回发布的车的数量
        except:
            return -1

    #获取已经成交的数量
    def getDealNum(self):
        try:
            user = manage_deal.objects.all()
            deal_num = len(user)
            return deal_num #返回成交量
        except:
            return -1
