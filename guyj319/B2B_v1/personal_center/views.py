#coding=utf-8
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from account.account_manage import Tools
from personal_center.personalCenter import Personal_center
from first_page.views import handler500
from first_page.views import handler404

mPersonal_center = Personal_center()

@csrf_exempt
def personal_center(req):
    mTools = Tools()
    user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'GET':
        merchant_material = mPersonal_center.getMyInfo(user_id)
        if merchant_material == 0:
            return handler500(req) #查询失败
        elif merchant_material == 404:
            context = {"is_login": True}
            return render(req, 'to_completeMaterial.html', context)
            #return HttpResponseRedirect('/completeMaterial/')
        else:
            merchant_id = merchant_material.get('id')
            publish_info = valid_time_publish(req, merchant_id)
            exceed_publish = invalid_time_publish(req, merchant_id)
            context = {"is_login": True,'merchant_material':merchant_material,'publish_info':publish_info,'exceed_publish':exceed_publish}
            return render(req, 'homePage.html', context)
    else:
        return handler404(req)

@csrf_exempt
def home_page_post(request):
    mTools = Tools()
    user_id = mTools.getSession(request,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if request.method == "POST":
        collection_id = request.POST.get("collectionId",None)
        exceed_collection_id = request.POST.get("exceedCollectionId",None)

        if collection_id is not None:
            result_code = mPersonal_center.deleteValidTimeCar(collection_id, user_id)
            if result_code == 0:#有效期 -- 页面撤销失败
                return HttpResponse("0")
            elif result_code == 666:#撤销成功
                return HttpResponse("1")

        if exceed_collection_id is not None: #过期车源页面 --- 删除记录
            result_code = mPersonal_center.deleteInalidTimeCar(exceed_collection_id)
            if result_code == 0: #删除信息失败
                return HttpResponse("0")
            elif result_code == 666:
                return HttpResponse("1")

        return HttpResponse("0")
    else:
        return handler404(request)

@csrf_exempt
def valid_time_publish(req, merchant_id):
    car = mPersonal_center.findValidTimeCar(merchant_id)  #调用这个函数来查询有效期里的车源信息
    if car == 0:
        return handler500(req)  #查看有效期车源失败
    all_cars_infos = mPersonal_center.findPersonalCenterCar(car)    #存储所有与该商家号码相关的车的信息
    return all_cars_infos

@csrf_exempt
def invalid_time_publish(req, merchant_id):
    car = mPersonal_center.findInvalidTimeCar(merchant_id) #调用这个函数来查询过期里的车源信息
    if car == 0:
        return handler500(req) #查看过期车源失败
    all_cars_infos = mPersonal_center.findPersonalCenterCar(car)    #存储所有与该商家号码相关的车的信息
    return all_cars_infos

#有效期 --- 撤销发布
@csrf_exempt
def list_undo(req):
    ###########
    #用来管理页面内容，显示有效期内容还是过期内容
    ############
    mTools = Tools()
    user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'POST':
        operation_id = req.POST.get('operation_id',None)
        if operation_id is None:
            return handler404(req)
        result_code = mPersonal_center.deleteValidTimeCar(operation_id, user_id)
        if result_code == 0:#撤销失败
            return HttpResponse("0")
        elif result_code == 666:#撤销成功
            return HttpResponse("1")
    else:
        return handler404(req)  #404 请求错误

#过期车源页面 --- 删除记录
@csrf_exempt
def list_delete(req):
    ###########
    #用来管理页面内容，显示有效期内容还是过期内容
    ############
    mTools = Tools()
    user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'POST':
        operation_id = req.POST.get('operation_id',None)
        if operation_id is None:
            return handler404(req)
        #删除信息
        result_code = mPersonal_center.deleteInalidTimeCar(operation_id)
        if result_code == 0: #删除信息失败
            return HttpResponse("0")
        elif result_code == 666:
            return HttpResponse("1")
    else:
        return handler404(req)  #404 请求错误.
