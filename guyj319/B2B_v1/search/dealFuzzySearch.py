#! -*- coding:utf-8 -*-
import jieba
import re
from car.models import car_table

class Fuzzy_search(object):
    ONE_PAGE_OF_DATA = 5 #每页条数

    def divideWords(self, searchString):
        seg_list = list(jieba.cut(searchString))
        return seg_list

    def fuzzySearchPaging(self, cars_infos, length_cars_infos, curPage, allPage, pageType):

        #判断点击了【下一页】还是【上一页】
        if pageType == 'pageDown':
            curPage = curPage+1
        elif pageType == 'pageUp':
            curPage = curPage-1

        startPos = (curPage - 1) * Fuzzy_search.ONE_PAGE_OF_DATA
        endPos = startPos + Fuzzy_search.ONE_PAGE_OF_DATA

        if curPage == 1 and allPage == 1: #标记1
            if length_cars_infos == None:
                length_cars_infos = 0
            allPage = int(length_cars_infos / Fuzzy_search.ONE_PAGE_OF_DATA)
            remainPost = length_cars_infos % Fuzzy_search.ONE_PAGE_OF_DATA
            if remainPost > 0:
               allPage =allPage+1
            if allPage == 0:
                allPage = 1

        if length_cars_infos == 0:
            posts = []
        else:
            posts = (cars_infos)[startPos:endPos]   ################################

        data={}
        data['allPage']=allPage
        data['curPage']=curPage
        data['results']=posts
        return data

    def fuzzyFinderGetList(self):
        lists = []
        try:
           sets = car_table.objects.filter(is_black=0)
        except:
            return 0
        for each in sets:
             myStr = str(each.id)+','+each.car_type+','+each.car_brand+','+each.car_series+','+each.car_model+','+each.color+','+each.delivery_type+','+each.pay_method+','+each.sell_area+','+each.method_logistics  #注意地方
             lists.append(myStr)
        return lists

    def fuzzyFinderGetData(self, req, user_input, length, count):
        '''
        :param user_input:
        :param length:
        :param count:
        :return: 返回模糊查询的没有按照时间和价格排序的
        '''
        id_lists = Fuzzy_search.fuzzyFinderGetList(self)

        return Fuzzy_search.fuzzyFinder(self, req, user_input, id_lists, length, count)


    def fuzzyFinder(self,req,user_input,collection,length,count):
         '''
         :param user_input:
         :param collection:
         :param length:
         :param count:
         :return: 返回一个列表集合
         '''
         if length <= count:
             my_id_lists=[]
             for each in collection:
                   my_id_lists.append(int(each.split(',')[0])) #获取传递进来的id，此处用int()是将字符串 id 变成 数字 id

             try:
                 cars = car_table.objects.filter(id__in=my_id_lists).values_list()
                 cars = list(cars)  #返回的cars像 [(1, 'ba', 18, 'm'), (2, 'ba', 18, 'm'), (3, 'a', 18, 'm')] 这样的列表，方便排序
                            # cars.sort(key=lambda x:x[0]) 是按照id来排序，在(1, 'ba', 18, 'm')里面，每个元素对应于一个字段，所以这里有id,name,age,sex 4个字段
                 length_cars = len(cars)


                 req.session['search_datas'] = cars
                 req.session['length_search_datas'] = length_cars              ################################
                 return 666

             except:
                 return 0

         else:
              suggestions = []
              pattern = '.*?'.join(user_input[count])    # Converts 'djm' to 'd.*?j.*?m'
              regex = re.compile(pattern)         # Compiles a regex.
              for item in collection:
                   match = regex.search(item)      # Checks if the current item matches the regex.
                   if match:
                       suggestions.append((len(match.group()), match.start(), item))
              sets = [x for _, _, x in sorted(suggestions)]

              count = count+1
              Fuzzy_search.fuzzyFinder(self, req, user_input, sets, length, count)  #递归完筛选条件
