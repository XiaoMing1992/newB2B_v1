#coding=utf-8
from account.models import user_info_people,user_info_table
from django.views.decorators.cache import cache_control

#指定缓存是否需要总是检查新版本, 如果没有变化则仅传送缓存版本. (某些缓存即使服务器端页面变化也仅传递缓存版本--仅仅因为缓存拷贝尚未到期).
# 在这个例子里 cache_control 通知缓存每次检验缓存版本, 直到 600 秒到期:
#private=True声明该页面的缓存是 "私密的"
#@cache_control(private=True,must_revalidate=True, max_age=600)

class Complete_material(object):

    #完善资料
    def completeUserInfo(self, user_id, user_info):
        '''
        :param user_id:
        :param user_info:
        :return: 正常插入，返回666；更新失败，返回0
        '''
        try:
           #获取用户信息
           license_path = user_info.get('license_path','') #营业执照路径
           id_card_path = user_info.get('id_card_path','') #身份证路径
           user_company_name = user_info.get('user_company_name','') #企业名称
           user_type = user_info.get('user_type','')   #用户类型

           user_address = user_info.get('user_address','')  #用户地址
           province = user_info.get('province','')          #省份
           city = user_info.get('city','')                  #城市

           user_trademark = user_info.get('user_trademark','')  #企业简介

           user_names = user_info.get('user_names','') #用户姓名
           phone_numbers = user_info.get('phone_numbers','') #用户电话号码

           #保存到数据库user_info_table表里面
           user = user_info_table.objects.create(user_id=user_id,
                                                 user_company_name=user_company_name,
                                                 user_type=user_type,
                                                 user_address=user_address,
                                                 user_trademark=user_trademark,
                                                 license_path=license_path,
                                                 id_card_path=id_card_path,
                                                 province=province,
                                                 city=city)
           #保存到数据库user_info_people表里面
           for i in range(len(phone_numbers)):
              user_info_people.objects.create(merchant_id=user.id,
                                              user_name=user_names[i],
                                              user_phone=phone_numbers[i])
           return 666
        except:
            return 0

    def editUserInfo(self, user_id, user_info):
        '''
        :param user_id:
        :param user_info:
        :return: 正常更新，返回666；更新失败，返回0
        '''
        user_company_name = user_info.get('user_company_name','') #企业名称
        user_type = user_info.get('user_type','')   #用户类型
        user_address = user_info.get('user_address','')  #用户地址
        user_trademark = user_info.get('user_trademark','')  #企业简介

        user_names = user_info.get('user_names','') #用户姓名
        phone_numbers = user_info.get('phone_numbers','') #用户电话号码

        try:
            user = user_info_table.objects.get(user_id=user_id)
            merchant_id = user.id
            user.user_company_name = user_company_name #企业名称更新
            user.user_type = user_type   #用户类型更新
            user.user_address = user_address  #用户地址更新
            user.user_trademark = user_trademark #企业品牌更新
            user.save()#保存更新

            people = user_info_people.objects.get(merchant_id=merchant_id)
            for i in range(len(phone_numbers)):
                people[i].user_name = user_names[i]
                people[i].user_phone = phone_numbers[i]
                people.save() #保存更新用户名和电话号码
            return 666
        except:
            return 0

    #获取用户的资料
    def findUserInfo(self, user_id):
        '''
        :param user_id:
        :return: 正常查询，返回查询的信息字典；查询出错，返回0
        '''
        #查询完善资料的那部分的企业、地点等相关信息
        try:
            base_info = user_info_table.objects.get(user_id=user_id)  #根据点击“查询详情”时传进来的发布者的手机号来查询相关的完善资料的信息
            merchant_id = base_info.id

            #查询完善资料的那部分的联系人的信息
            people = {}
            peoples = []
            people_info = user_info_people.objects.filter(merchant_id=merchant_id)  #根据点击“查询详情”时传进来的发布者的手机号来查询相关的完善资料的信息
            for i in range(len(people_info)):
                people['user_name'] = people_info[i].user_name  #联系人姓名
                people['user_phone'] = people_info[i].user_phone  #联系人电话号码
                peoples.append(people)
                people = {}

            merchant_material = {}  #存储卖家资料
            merchant_material['company_name'] = base_info.user_company_name     #企业名称
            merchant_material['location'] = base_info.user_address              #所在地区
            merchant_material['merchant_type'] = base_info.user_type            #企业类型
            merchant_material['introduction'] = base_info.user_trademark        #企业简介

            merchant_material['peoples'] = peoples                              #联系人的信息

            return merchant_material
        except:
             return 0