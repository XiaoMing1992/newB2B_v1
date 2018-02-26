#coding=utf-8
from car.models import car_table
from account.models import record_table
from django.db.models import Q
import datetime

class Keyword_search(object):
    ONE_PAGE_OF_DATA = 5 #每页5条记录

    def searchPaging(self,cars_infos,length_cars_infos,curPage,allPage,pageType):
        #判断点击了【下一页】还是【上一页】
        if pageType == 'pageDown':
           curPage = curPage+1
        elif pageType == 'pageUp':
            curPage = curPage-1

        startPos = (curPage - 1) * Keyword_search.ONE_PAGE_OF_DATA
        endPos = startPos + Keyword_search.ONE_PAGE_OF_DATA

        if curPage == 1 and allPage == 1: #标记1
            if length_cars_infos == None:
                length_cars_infos = 0
            allPage = int(length_cars_infos / Keyword_search.ONE_PAGE_OF_DATA)
            remainPost = length_cars_infos % Keyword_search.ONE_PAGE_OF_DATA
            if remainPost > 0:
               allPage = allPage + 1
            if allPage == 0:
                allPage = 1

        if length_cars_infos == 0:
            posts = []
        else:
            posts = (cars_infos)[startPos:endPos]   ################################

        data={}
        data['allPage'] = allPage
        data['curPage'] = curPage
        data['results'] = posts
        return data

    #保存搜索条件
    def saveSearchRecord(self, user_id, condition):
         '''
         :param user_id:
         :param condition:
         :return: 正常插入数据库返回666；插入数据库出错返回0
         '''

         time_save = datetime.datetime.now() #保存搜索条件的时间
         try:
            record_table.objects.create(user_id=user_id,
                                        car_type=condition.get('car_type','').split('\n')[0],
                                        car_brand=condition.get('car_brand','').split('\n')[0],
                                        car_series=condition.get('car_series','').split('\n')[0],
                                        car_model=condition.get('car_model','').split('\n')[0],
                                        color=condition.get('color','').split('\n')[0],
                                        delivery_type=condition.get('delivery_type','').split('\n')[0],
                                        pay_method=condition.get('pay_method','').split('\n')[0],
                                        sell_area=condition.get('province','').split('\n')[0]+' '+condition.get('city','').split('\n')[0],#condition.get('sell_area','').split('\n')[0],
                                        province=condition.get('province','').split('\n')[0],
                                        city=condition.get('city','').split('\n')[0],
                                        method_logistics=condition.get('method_logistics','').split('\n')[0],
                                        time_save=time_save)
            return 666
         except:
            return 0

    def OneWordGetData(self, condition):
        try:
            lowest_price = condition.get('lowest_price', None)
            highest_price = condition.get('highest_price', None)

            cars = car_table.objects.filter(Q(is_black=0),
                                            Q(car_type__exact=condition.get('car_type',None))
                                            |Q(car_brand__exact=condition.get('car_brand',None))
                                            |Q(car_series__exact=condition.get('car_series',None))
                                            |Q(car_model__exact=condition.get('car_model',None))
                                            |Q(color__exact=condition.get('color',None))
                                            |Q(delivery_type__exact=condition.get('delivery_type',None))
                                            |Q(pay_method__exact=condition.get('pay_method',None))
                                            |Q(sell_area__exact=condition.get('sell_area',None))
                                            |Q(province__exact=condition.get('province',None))
                                            |Q(city__exact=condition.get('city',None))
                                            |Q(highest_price__range=(lowest_price,highest_price))
                                            |Q(method_logistics__exact=condition.get('method_logistics',None))).order_by('-date_publish').values_list()
            if cars:
               goto = True
            else:
                cars = car_table.objects.filter(is_black=0).order_by('-date_publish').values_list()   # #按最近发布日期显示

            cars = list(cars)  #返回的cars像 [(1, 'ba', 18, 'm'), (2, 'ba', 18, 'm'), (3, 'a', 18, 'm')] 这样的列表，方便排序
                            # cars.sort(key=lambda x:x[0]) 是按照id来排序，在(1, 'ba', 18, 'm')里面，每个元素对应于一个字段，所以这里有id,name,age,sex 4个字段
            return cars
        except:
            return 0


    def firstPageSort(self, car_brand, car_series):
         try:
            car_is_exist = car_table.objects.filter(Q(is_black=0),
                                                    Q(car_brand__exact=car_brand)
                                                    |Q(car_series__exact=car_series)).order_by('-date_publish').values_list() #按最近发布日期显示
            #print(car_is_exist)
            try:
               car_is_exist = list(car_is_exist)
            except:
                car_is_exist = car_table.objects.filter(is_black=0).order_by('-date_publish').values_list() #按最近发布日期显示
                try:
                    car_is_exist = list(car_is_exist)
                except:
                    return []
            #if car_is_exist:
            #    print('hello1')
            #    goto = True
            #else:
            #    print('hello2')
            #    car_is_exist = car_table.objects.filter(is_black=0).order_by('-date_publish').values_list() #按最近发布日期显示

            return car_is_exist
         except:
            return 0

    def keyWordGetDataOederByPrice(self, lowest_price, highest_price):
        try:
            car_is_exist = car_table.objects.filter(is_black=0,
                                                    highest_price__range=(lowest_price, highest_price)).order_by('price').values_list() #按最少价格显示
            if car_is_exist:
               car_is_exist = car_table.objects.filter(is_black=0).order_by('price').values_list() #按最少价格显示
            car_is_exist = list(car_is_exist)
            return car_is_exist
        except:
            return 0

    #从‘我的需求’那里传递过来的（也就是说从记录我的需求的记录表里面获取的）
    def getDataFromMyDemands(self, record_id, user_id):
        '''
        :param record_id:
        :param user_id:
        :return: 正常返回查询到的数据；查询数据库出错，返回0
        '''

        try:
            result_record = record_table.objects.get(id=record_id, user_id=user_id)#根据‘我的需求’那里搜索条件的id来寻找相应的记录
            condition = {}
            condition['car_type'] = result_record.car_type

            condition['car_brand'] = result_record.car_brand
            condition['car_model'] = result_record.car_model
            condition['car_series'] = result_record.car_series

            condition['province'] = result_record.province
            condition['city'] = result_record.city
            condition['sell_area'] = result_record.sell_area

            condition['pay_method'] = result_record.pay_method
            condition['delivery_type'] = result_record.delivery_type
            condition['color'] = result_record.color

            condition['method_logistics'] = result_record.method_logistics
            return condition
        except:
            return 0

    def keyWordIntersection(self,condition):
        try:
            lowest_price = condition.get('lowest_price',None)
            highest_price = condition.get('highest_price',None)

            delivery_type = condition.get('delivery_type',None)
            color = condition.get('color',None)
            car_type = condition.get('car_type',None)

            car_brand = condition.get('car_brand',None)
            car_series = condition.get('car_series',None)
            car_model = condition.get('car_model',None)

            pay_method = condition.get('pay_method',None)
            sell_area = condition.get('sell_area',None)
            province = condition.get('province',None)
            city = condition.get('city',None)
            method_logistics = condition.get('method_logistics',None)


            cars = car_table.objects.filter(is_black=0).order_by('-date_publish').values_list()   # #按最近发布日期显示
            list_intersection = list(cars)

            if delivery_type is not None:
               cars = car_table.objects.filter(is_black=0, delivery_type__exact=delivery_type).order_by('-date_publish').values_list()
               cars = list(cars)
               list_intersection = [val for val in cars if val in list_intersection] #交集

            if car_type is not None:
               cars = car_table.objects.filter(is_black=0, car_type__exact=car_type).order_by('-date_publish').values_list()
               cars = list(cars)
               list_intersection = [val for val in cars if val in list_intersection] #交集

            if car_brand is not None:
               cars = car_table.objects.filter(is_black=0, car_brand__exact=car_brand).order_by('-date_publish').values_list()
               cars = list(cars)
               list_intersection = [val for val in cars if val in list_intersection] #交集

            if car_series is not None:
               cars = car_table.objects.filter(is_black=0, car_series__exact=car_series).order_by('-date_publish').values_list()
               cars = list(cars)
               list_intersection = [val for val in cars if val in list_intersection] #交集

            if car_model is not None:
               cars = car_table.objects.filter(is_black=0, car_model__exact=car_model).order_by('-date_publish').values_list()
               cars = list(cars)
               list_intersection = [val for val in cars if val in list_intersection] #交集

            if pay_method is not None:
               cars = car_table.objects.filter(is_black=0, pay_method__exact=pay_method).order_by('-date_publish').values_list()
               cars = list(cars)
               list_intersection = [val for val in cars if val in list_intersection] #交集

            if color is not None:
               cars = car_table.objects.filter(is_black=0, color__exact=color).order_by('-date_publish').values_list()
               cars = list(cars)
               list_intersection = [val for val in cars if val in list_intersection] #交集

            if sell_area is not None:
               cars = car_table.objects.filter(is_black=0, sell_area__exact=sell_area).order_by('-date_publish').values_list()
               cars = list(cars)
               list_intersection = [val for val in cars if val in list_intersection] #交集

            if province is not None:
               cars = car_table.objects.filter(is_black=0, province__exact=province).order_by('-date_publish').values_list()
               cars = list(cars)
               list_intersection = [val for val in cars if val in list_intersection] #交集

            if city is not None:
               cars = car_table.objects.filter(is_black=0, city__exact=city).order_by('-date_publish').values_list()
               cars = list(cars)
               list_intersection = [val for val in cars if val in list_intersection] #交集

            if method_logistics is not None:
               cars = car_table.objects.filter(is_black=0, method_logistics__exact=method_logistics).order_by('-date_publish').values_list()
               cars = list(cars)
               list_intersection = [val for val in cars if val in list_intersection] #交集

            if highest_price is not None and lowest_price is not None and lowest_price<=highest_price:
               cars = car_table.objects.filter(is_black=0, highest_price__range=(lowest_price, highest_price)).order_by('-date_publish').values_list()
               cars = list(cars)
               list_intersection = [val for val in cars if val in list_intersection] #交集

            #返回的cars像 [(1, 'ba', 18, 'm'), (2, 'ba', 18, 'm'), (3, 'a', 18, 'm')] 这样的列表，方便排序
            # cars.sort(key=lambda x:x[0]) 是按照id来排序，在(1, 'ba', 18, 'm')里面，每个元素对应于一个字段，所以这里有id,name,age,sex 4个字段
            return list_intersection
        except:
            return 0

    #找到车的信息，并且返回
    def keyWordFindCar(self,car):
        '''
        :param car:
        :return: 返回关于找到的车的信息
        '''

        dict={}             #存储与该商家号码相关的车的信息
        all_cars_infos=[]   #存储所有与该商家号码相关的车的信息

        if car:
           for i in range(len(car)):
               dict['detail_id'] = car[i].id
               dict['series'] = car[i].car_brand+' '+car[i].car_series+' '+car[i].car_model
               dict['region'] = car[i].sell_area

               price = {}
               price['origin_price'] = car[i].highest_price
               price['discount_amount'] = car[i].lowest_price
               dict['price'] = price

               dict['detail']=car[i].color+' | '+car[i].delivery_type+' | '+car[i].car_type
               dict['update_time']=car[i].date_publish              #车的id
               all_cars_infos.append(dict)
               dict={}

           return all_cars_infos

    #找到车的信息，并且返回
    def getCarDataInArray(self,car):
        '''
        :param car:
        :return: 返回关于找到的车的信息
        '''

        dict={}             #存储与该商家号码相关的车的信息
        all_cars_infos=[]   #存储所有与该商家号码相关的车的信息

        if car:
           for i in range(len(car)):
               #dict['detail_id'] = car[i].id
               dict['detail_id'] = car[i][0]

               #dict['series'] = car[i].car_brand+' '+car[i].car_series+' '+car[i].car_model
               dict['series'] = car[i][3]+' '+car[i][4]+' '+car[i][5]

               #dict['region'] = car[i].sell_area
               dict['region'] = car[i][11]

               price = {}
               #price['origin_price'] = car[i].highest_price
               price['origin_price'] = car[i][14]
               #price['discount_amount'] = car[i].lowest_price
               price['discount_amount'] = car[i][13]
               dict['price'] = price

               #dict['detail']=car[i].color+'|'+car[i].delivery_type+'|'+car[i].car_type
               dict['detail']=car[i][6]+'   |   '+car[i][8]+'   |   '+car[i][2]
               if car[i][8] == '期货':
                   dict['is_future'] = True
               else:
                   dict['is_future'] = False

               #dict['update_time']=car[i].date_publish
               #dict['update_time']=car[i][17]
               update_time = {}
               publish_time = car[i][17]      #发布的日期
               update_time['year'] = publish_time.year      #发布的日期的年份
               update_time['month'] = publish_time.month      #发布的日期的月份
               update_time['day'] = publish_time.day  #发布的日期的天数
               dict['update_time'] = update_time

               all_cars_infos.append(dict)
               dict={}

           return all_cars_infos
