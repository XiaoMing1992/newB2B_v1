#coding=utf-8
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from account.account_manage import Tools
from account.my_friends.inviteFriend import Invite_friends
from account.my_homepage.homepage import Homepage
from account.my_materials.complete_info import Complete_material
from car.car_info import Car_detail
from first_page.views import handler404
from first_page.views import handler500
import time

mComplete_material = Complete_material()
mHomepage = Homepage()
mInvite_friends = Invite_friends()
mCar_detail = Car_detail()

#邀请好友 =================================================================================================================================
@csrf_exempt
def send_invitation_code(req):
    # 状态码说明：
    # 1: 发送成功
    # 0: 发送失败

    mTools = Tools()
    user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'POST':
             #获得当前时间时间戳
             now_time = int(time.time())  #这是时间戳，即将当前时间转换为的毫秒数
             last_time = mTools.getSession(req,'last_time')
             if last_time is not None:
                  if (now_time-last_time)<(1*60*1000): #1分钟
                      req.session['last_time']=now_time
                      return HttpResponse('2')     #操作过于频繁
                  else:
                      req.session['last_time']=now_time
             else:
                 req.session['last_time']=now_time

             mobiles = req.POST.getlist("phoneNumberList[]")

             result = mInvite_friends.inviteFriend(user_id, mobiles) #调用这个函数处理当前用户输入的电话号码
             if result == 0:
                 return handler500(req) #更新或者插入邀请码出错
             else:
                success = result['success']
                fail = result['fail']
                return HttpResponse('1')

    else: #get请求
       context = {"is_login": True}
       return render(req, "sendInvitationCode.html",context)

#完善资料 =================================================================================================================================
@csrf_exempt
def complete_material(req):
    mTools=Tools()
    user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'POST':
        #在完善资料界面，点击“提交”按钮
        #获得表单数据
        user_info={}
        user_info['user_company_name'] = req.POST.get('companyName','')        #企业名称

        user_info['user_type'] = req.POST.get('merchantType','')   #企业类型


        user_info['province'] = req.POST.get('province','')                #省份
        user_info['city'] = req.POST.get('city','')                        #城市
        user_info['user_address'] = req.POST.get('province','')+' '+req.POST.get('city','') #

        user_info['user_trademark'] = req.POST.get('brandIntroduction','')     #企业品牌，即简介
        user_info['user_names'] = req.POST.getlist('contactNameList[]')               #保存联系人的姓名
        user_info['phone_numbers'] = req.POST.getlist('phoneNumberList[]')        #保存联系人的电话号码

        license_photo_name = req.POST.get('licensePhoto','')
        id_card_photo_name = req.POST.get('idCardPhoto','')

        result_code = mComplete_material.completeUserInfo(user_id, user_info) #调用这个函数来保存用户的资料
        if result_code == 0:
            return handler500(req) #完善资料插入数据库出错
        elif result_code == 666:       #完善资料插入数据库成功
            return HttpResponse('1')
    # get 请求
    else:
        context = {"is_login": True}
        return render(req, "completeMaterial.html", context)

@csrf_exempt
def complete_material_post(request):
    if request.method == "POST":
        return HttpResponse("1")
    return HttpResponse("0")


@csrf_exempt
def edit_material(req):
    mTools = Tools()
    user_id = mTools.getSession(req, 'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'GET':
        merchant_material = mComplete_material.findUserInfo(user_id) #调用这个函数来获取当前用户的资料
        if merchant_material == 0:
            return handler500(req) #编辑资料查询失败

        context = {"is_login": True,'merchant_material':merchant_material}
        return render(req, "completeMaterial.html", context)
    else:
        #在完善资料界面，点击“提交”按钮
        #获得表单数据
        user_info={}
        user_info['user_company_name'] = req.POST.get('companyName',None)        #企业名称
        user_info['user_type'] = req.POST.get('merchant_type',None)               #企业类型
        user_info['user_address'] = req.POST.get('location',None)                #选择地区
        user_info['user_trademark'] = req.POST.get('brandIntroduction',None)     #企业品牌，即简介
        user_info['user_names'] = req.POST.get('contactList',None)               #保存联系人的姓名
        user_info['phone_numbers'] = req.POST.get('phoneNumberList',None)        #保存联系人的电话号码

        #如果存在编辑操作会话，说明已经有资料了，只需要更新就可以了
        result_code = mComplete_material.editUserInfo(user_id, user_info) #调用这个函数来更新用户的新编辑资料
        if result_code == 0:
            return handler500(req) #编辑更新数据库出错
        elif result_code == 666:
            return HttpResponse('1')
            #context = {"is_login",'finish':True}
            #return render(req, "completeMaterial.html", context) ##############################################


#处理商家主页页面内容 =================================================================================================================================
@csrf_exempt
def merchant(req):
    mTools = Tools()
    user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'GET':
        merchant_id = req.GET.get('operation_id', 0) #要查看的商家的id

        all_cars_infos = mHomepage.findHomepageCar(merchant_id)  #存储所有与该商家号码相关的车的信息
        if all_cars_infos == 0:
            return handler500(req) #商家主页，查询车的信息失败
        sellerInfo = mHomepage.getSellerInfo(merchant_id) #存储所有查看的卖家相关的其他的信息
        if sellerInfo == 0:
            return handler500(req) #商家主页，查询卖家相关的信息失败
        merchant_material = sellerInfo
        publish_info = all_cars_infos

        code_collect_merchant = mCar_detail.isMerchantCollected(user_id, merchant_id) #判断该商家是否已经被收藏过
        if code_collect_merchant == 2:
            return handler500(req)
        else:
            is_merchant_collected = code_collect_merchant
        context = {"is_login": True,
               "is_merchant_collected": is_merchant_collected,
               "merchant_material": merchant_material,
               "publish_info": publish_info}
        return render(req, "merchant.html", context)
    else:
        return handler404(req) #404 请求错误

#商家收藏
@csrf_exempt
def homepage_seller_collection(req):
    mTools = Tools()
    user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'POST':
        merchantId = req.POST.get("merchantId",None)
        result_code = mCar_detail.collectSeller(user_id, merchantId)#调用这个函数来处理收藏商家操作
        if result_code == 0:
            return HttpResponse("0")
        elif result_code == 666:
            return HttpResponse("1")
    else:
        return handler404(req) #404 请求错误.
