#coding=utf-8
from account.models import user_info_table
from account.models import user_info_people
from django.db.models import Q
import datetime

class Admin_search(object):
    ONE_PAGE_OF_DATA = 5 #每页5条记录

    def searchPaging(self, users_infos, length_users_infos, curPage, allPage, pageType):
        #判断点击了【下一页】还是【上一页】
        if pageType == 'pageDown':
           curPage = curPage+1
        elif pageType == 'pageUp':
            curPage = curPage-1

        startPos = (curPage - 1) * Admin_search.ONE_PAGE_OF_DATA
        endPos = startPos + Admin_search.ONE_PAGE_OF_DATA

        if curPage == 1 and allPage == 1: #标记1
            if length_users_infos == None:
                length_users_infos = 0
            allPage = int(length_users_infos / Admin_search.ONE_PAGE_OF_DATA)
            remainPost = length_users_infos % Admin_search.ONE_PAGE_OF_DATA
            if remainPost > 0:
               allPage = allPage + 1
            if allPage == 0:
                allPage = 1

        if length_users_infos == 0:
            posts = []
        else:
            posts = (users_infos)[startPos:endPos]   ################################

        data={}
        data['allPage'] = allPage
        data['curPage'] = curPage
        data['results'] = posts
        return data

    def OneWordGetData(self, condition):
        try:
            users = user_info_table.objects.filter(Q(is_black=0),
                                            Q(user_company_name__exact=condition.get('user_company_name', None))
                                            |Q(user_type__exact=condition.get('user_type', None))
                                            |Q(user_trademark__exact=condition.get('user_trademark', None))
                                            |Q(province__exact=condition.get('province', None))
                                            |Q(city__exact=condition.get('city', None))).order_by('-add_time')
            user_id_list = []
            for i in range(len(users)):
                user_id_list.append(users[i].id)

            peoples = user_info_people.objects.filter(Q(merchant_id__in=user_id_list)
                                            |Q(user_name__exact=condition.get('user_name',None))
                                            |Q(user_phone__exact=condition.get('user_phone', None)))

            merchant_id_list = []
            for i in range(len(peoples)):
                merchant_id_list.append(peoples[i].merchant_id)
            return merchant_id_list  #返回商家的id
        except:
            return 0

    def findMerchant(self, merchant_id_list):
        try:
            user = user_info_table.objects.filter(id__in=merchant_id_list).order_by('-add_time')
            content_list = []
            for i in range(len(user)):
                content_dirct = {}
                content_dirct['company_name'] = user[i].user_company_name
                content_dirct['region'] = user[i].user_address
                content_dirct['user_trademark'] = user[i].user_trademark
                content_dirct['state'] = user[i].state
                content_dirct['id'] = user[i].id

                people = user_info_people.objects.filter(merchant_id=user[i].id)
                people_list = []
                for j in range(len(people)):
                    people_dirct = {}
                    people_dirct['name'] = people[j].user_name
                    people_dirct['phone'] = people[j].user_phone
                    people_list.append(people_dirct)

                content_dirct['peoples'] = people_list

                content_list.append(content_dirct)
            return content_list
        except:
            return 0