#coding=utf-8
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from account.account_manage import Tools
from collection.collect_car import Collect_car
from collection.collect_seller import Collect_seller
from first_page.views import handler500
from first_page.views import handler404

mCollect_car = Collect_car()
mCollect_seller = Collect_seller()

@csrf_exempt
def collection(req):
  mTools = Tools()
  user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
  if user_id is None:
     return HttpResponseRedirect('/sessionExceedTime/')

  if req.method == 'GET':
        mycollect_records = mCollect_car.searchCollectCar(user_id)#调用这个函数来查询用户收藏的车的信息
        if mycollect_records == 0:
            return handler500(req) #查询失败
        all_cars_infos = mCollect_car.searchCarTable(mycollect_records) #调用这个函数来找到收藏的车的信息
        if all_cars_infos == 404:
           return HttpResponse("一些车在测试中删除了，请程序员检查数据库，修改相应数据")
           #return handler500(req) #数据库查询出错

        mycollect_records = mCollect_seller.searchCollectSeller(user_id) #调用这个函数来查询收藏的商家
        if mycollect_records == 0:
            return handler500(req) #查询失败
        merchant_material = mCollect_seller.getInFo(mycollect_records)#调用这个函数来处理用户的收藏的商家的信息
        if merchant_material == 0:
            return handler500(req) #查询失败

        context = {"is_login": True,'publish_info':all_cars_infos,'merchant_material':merchant_material}
        return render(req, "collection.html", context)
  else:
        return handler404(req) #404 请求错误

@csrf_exempt
def collection_post(req):
  mTools = Tools()
  user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
  if user_id is None:
     return HttpResponseRedirect('/sessionExceedTime/')

  if req.method == 'POST':
        merchantId = req.POST.get('merchantId',None)
        detailId = req.POST.get('detailId',None)
        if merchantId is not None:
           return cancel_seller_collection(req,merchantId)
        if detailId is not None:
            return cancel_car_collection(req,detailId)
        return handler404(req) #404 请求错误
  else:
      return handler404(req) #404 请求错误

#车源收藏 --- 取消收藏
@csrf_exempt
def cancel_car_collection(req,operation_id):
    if req.method == 'POST':
        mycollect_records = mCollect_car.cancelCollectCar(operation_id)#调用这个函数来根据卖家的手机号来取消收藏和查询用户收藏的车的信息
        if mycollect_records == 0: #取消收藏失败
            return HttpResponse("0")
        else:
            return HttpResponse("1")
    else:
        return handler404(req) #404 请求错误

#商家收藏 --- 取消收藏
@csrf_exempt
def cancel_seller_collection(req,operation_id):
    if req.method == 'POST':
        #删除信息
        result_code = mCollect_seller.deleteSeller(operation_id) #调用这个函数来取消商家的收藏
        if result_code == 0: #取消收藏失败
            return HttpResponse("0")
        elif result_code == 666:
            return HttpResponse("1")
    else:
        return handler404(req) #404 请求错误.


#处理商家收藏界面 =================================================================================================================================
@csrf_exempt
def collect_seller(req):
  mTools = Tools()
  user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
  if user_id is None:
     return HttpResponseRedirect('/sessionExceedTime/')

  if req.method == 'GET':
        mycollect_records = mCollect_seller.searchCollectSeller(user_id) #调用这个函数来查询收藏的商家
        if mycollect_records == 0:
            return handler500(req) #查询失败
        list_content = mCollect_seller.getInFo(mycollect_records)#调用这个函数来处理用户的收藏的商家的信息
        if list_content == 0:
            return handler500(req) #查询失败

        context = {"is_login": True,'list_content':list_content}
        return render(req, "collection.html", context)
  else:
     return handler404(req) #404 请求错误
