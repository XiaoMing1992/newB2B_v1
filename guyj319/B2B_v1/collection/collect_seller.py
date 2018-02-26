# coding=utf-8
from account.models import user_info_table
from account.models import user_info_people
from account.models import user_more_table
from account.models import collect_seller_table

class Collect_seller(object):
    def searchCollectSeller(self, user_id):
        '''
        :param user_id:
        :return: 正常查询，返回查询集合；查询出错，返回0
        '''
        try:
            mycollect_records = collect_seller_table.objects.filter(user_id=user_id) #收藏的商家的电话号码的列表
            return mycollect_records
        except:
           return 0

    #删除商家
    def deleteSeller(self,seller_id):
        '''
        :param seller_id:
        :return:正常查询和删除，返回查询集合；删除或者查询出错，返回0
        '''
        try:
            collect_seller_table.objects.get(seller_id=seller_id).delete()#根据id和商家电话号码来删除

            user_more = user_more_table.objects.get(seller_id=seller_id) #更新 user_more_table
            user_more.collect_people_num = user_more.collect_people_num -1 #收藏该卖家的人数减少1
            user_more.save()
            return 666
        except:
            return 0

    #查询信息
    def getInFo(self, mycollect_records):
          '''
          :param mycollect_records:
          :return: 正常查询，返回查询到的以字典为元素的信息列表；数据库查询出错，返回0
          '''
          collect_list = []
          list_content = []
          dirct_content = {}
          for i in range(len(mycollect_records)):
              #查询完善资料的那部分的信息，是商家的信息
              try:
                 result1 = user_info_table.objects.get(user_id=mycollect_records[i].user_id)  #商家的电话号码，根据该号码来查询商家信息
              except:
                 return 0
              merchant_id = result1.id
              seller_company_name = result1.user_company_name  #企业名称
              seller_address = result1.user_address  #所在地区
              seller_type = result1.user_type  #企业类型
              seller_trademark = result1.user_trademark #企业品牌，即简介
              user_head_icon = result1.head_icon_path.url #用户头像路径
              is_black = result1.is_black #该卖家是否已经被拉黑

              #查询完善资料的那部分的信息，商家所在的公司的联系人
              people = {}
              peoples = []
              try:
                 result2 = user_info_people.objects.filter(merchant_id=merchant_id)  #根据点击“查询详情”时传进来的发布者的手机号来查询相关的完善资料的信息
              except:
                  return 0

              for j in range(len(result2)):
                  people['contact_name'] = result2[j].user_name  #联系人姓名
                  people['phone_number'] = result2[j].user_phone  #联系人电话号码
                  peoples.append(people)
                  people={}#必须重新定义

              #把商家的信息
              dirct_content['company_name'] = seller_company_name
              dirct_content['location'] = seller_address
              dirct_content['merchant_type'] = seller_type
              dirct_content['introduction'] = seller_trademark

              #dirct_content['peoples'] = peoples #妙，在字典里面value值可以赋值为一个列表
              dirct_content['contact_name'] = peoples[0].get('contact_name','')
              dirct_content['phone_number'] = peoples[0].get('phone_number','')

              #返回在收藏表里面对应的商家的id，为了在删除时，找到对应的 id 的商家进行删除，因为一个用户可以收藏很多相同的商家，
              #所以一个收藏表里面存在很多用户电话号码和手机号码重复的记录，但是id却是唯一的
              dirct_content['merchant_id'] = merchant_id

              dirct_content['image_path'] = user_head_icon

              dirct_content["is_black"] = is_black  #判断该收藏的卖家是否已经被拉黑

              list_content.append(dirct_content)

              dirct_content={}#必须重新定义
              if (i+1) % 3 == 0:
                  collect_list.append(list_content)
                  list_content = []
              else:
                  if i == len(mycollect_records)-1:
                     collect_list.append(list_content)
                     list_content = []

          return collect_list